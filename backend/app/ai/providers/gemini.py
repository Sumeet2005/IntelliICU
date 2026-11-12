"""
Google Gemini LLM Provider (Modernized for official google-genai SDK).
Supports structured JSON output, streaming, timeouts, and typed error mapping.
"""

from __future__ import annotations

import json
import logging
import os
import random
import time
from typing import Any, Callable, Dict, Generator, Optional, TypeVar

from app.ai.config_manager import ai_config
from app.ai.providers.base import (
    CLINICAL_SYSTEM_PROMPT,
    BaseLLMProvider,
    extract_json_object,
    normalize_clinical_response,
    sanitize_error_message,
)
from app.ai.providers.exceptions import (
    LLMAuthenticationError,
    LLMInvalidResponseError,
    LLMModelNotFoundError,
    LLMNetworkError,
    LLMProviderError,
    LLMRateLimitError,
    LLMTimeoutError,
)

logger = logging.getLogger(__name__)

DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


class GeminiLLMProvider(BaseLLMProvider):
    """Fallback clinical LLM provider backed by Google Gemini."""

    provider_name = "gemini"

    def __init__(self, client: Any = None) -> None:
        self.api_key = (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()
        self.default_model = (os.getenv("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL).strip()
        self.timeout = float(os.getenv("GEMINI_TIMEOUT_SECONDS", "30.0"))
        self.client = client
        self._sdk_mode = "google-genai"

        if self.client is None and self.api_key:
            try:
                from google import genai

                self.client = genai.Client(api_key=self.api_key)
                self._sdk_mode = "google-genai"
            except ImportError:
                try:
                    import google.generativeai as legacy_genai

                    legacy_genai.configure(api_key=self.api_key)
                    self.client = legacy_genai
                    self._sdk_mode = "google-generativeai-legacy"
                    logger.warning("[GeminiProvider] Using legacy google-generativeai SDK; upgrade to google-genai.")
                except ImportError:
                    logger.warning("[GeminiProvider] Neither google-genai nor google-generativeai is installed.")
                    self.client = None

    @property
    def credentials_configured(self) -> bool:
        return bool(self.api_key or self.client is not None)

    def _resolve_model(self) -> str:
        configured = ai_config.get("model")
        active_provider = (ai_config.get("provider") or "").lower()
        if active_provider == "gemini" and configured and configured != "mock-model":
            return str(configured)
        return self.default_model

    def _build_prompt(self, question: str, context: Dict[str, Any]) -> str:
        return (
            f"{CLINICAL_SYSTEM_PROMPT}\n\n"
            f"Patient Clinical Context:\n{json.dumps(context, indent=2, default=str)}\n\n"
            f"Question:\n{question}"
        )

    def _map_exception(self, exc: Exception) -> LLMProviderError:
        if isinstance(exc, LLMProviderError):
            return exc
        status = getattr(exc, "status_code", None) or getattr(exc, "code", None)
        msg = sanitize_error_message(exc)
        low = msg.lower()

        if status in (401, 403) or "api key" in low or "permission" in low or "unauthenticated" in low:
            return LLMAuthenticationError(f"Gemini authentication failed: {msg}", provider="gemini", status_code=401)
        if status == 429 or "quota" in low or "rate limit" in low or "resource_exhausted" in low:
            return LLMRateLimitError(f"Gemini quota/rate limit exceeded: {msg}", provider="gemini", status_code=429)
        if status == 404 or ("not found" in low and "model" in low):
            return LLMModelNotFoundError(f"Gemini model unavailable: {msg}", provider="gemini", status_code=404)
        if "timeout" in low or "deadline" in low or "timed out" in low:
            return LLMTimeoutError(f"Gemini request timed out: {msg}", provider="gemini")
        if status in (500, 502, 503) or "503" in low or "unavailable" in low or "high demand" in low:
            return LLMNetworkError(f"Gemini transient service error ({status or 503}): {msg}", provider="gemini", status_code=status or 503)
        return LLMNetworkError(f"Gemini request failed: {msg}", provider="gemini", status_code=502)

    def _execute_with_retry(self, fn: Callable[[], Any], max_retries: int = 2) -> Any:
        last_err: Optional[LLMProviderError] = None
        for attempt in range(max_retries + 1):
            try:
                return fn()
            except Exception as exc:
                mapped = self._map_exception(exc)
                last_err = mapped
                if not mapped.retryable or attempt >= max_retries:
                    raise mapped from exc
                delay = (0.8 * (2 ** attempt)) + random.uniform(0.0, 0.3)
                logger.warning(
                    "[GeminiProvider] Transient error (%s) on attempt %d/%d; retrying in %.2fs",
                    mapped.__class__.__name__,
                    attempt + 1,
                    max_retries + 1,
                    delay,
                )
                time.sleep(delay)
        assert last_err is not None
        raise last_err

    def _require_client(self) -> Any:
        if self.client is None:
            raise LLMAuthenticationError(
                "GEMINI_API_KEY is not configured or Gemini SDK is not installed.",
                provider="gemini",
                status_code=401,
            )
        return self.client

    def generate(self, question: str, context: Dict[str, Any]) -> Dict[str, Any]:
        client = self._require_client()
        model = self._resolve_model()
        temperature = float(ai_config.get("temperature", 0.2))
        max_tokens = max(int(ai_config.get("max_tokens", 2048)), 2048)
        prompt = self._build_prompt(question, context)

        def _call() -> str:
            if self._sdk_mode == "google-genai":
                try:
                    from google.genai import types

                    config: Any = types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                        response_mime_type="application/json",
                    )
                except ImportError:
                    config = {
                        "temperature": temperature,
                        "max_output_tokens": max_tokens,
                        "response_mime_type": "application/json",
                    }
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config,
                )
                return getattr(response, "text", "") or ""
            gen_model = client.GenerativeModel(model)
            response = gen_model.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                    "response_mime_type": "application/json",
                },
            )
            return getattr(response, "text", "") or ""

        try:
            raw_text = self._execute_with_retry(_call)
        except LLMProviderError as mapped:
            logger.error("[GeminiProvider] generate failed (%s): %s", mapped.__class__.__name__, mapped.sanitized_message)
            raise

        try:
            parsed = extract_json_object(raw_text)
        except Exception as exc:
            raise LLMInvalidResponseError(
                f"Gemini returned malformed JSON: {sanitize_error_message(exc)}",
                provider="gemini",
            ) from exc

        return normalize_clinical_response(parsed, provider="gemini", model=model, fallback_used=False, simulated=False)

    def generate_stream(self, question: str, context: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        client = self._require_client()
        model = self._resolve_model()
        temperature = float(ai_config.get("temperature", 0.2))
        max_tokens = max(int(ai_config.get("max_tokens", 2048)), 2048)
        prompt = self._build_prompt(question, context)

        def _open_stream() -> Any:
            if self._sdk_mode == "google-genai":
                try:
                    from google.genai import types

                    config: Any = types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                        response_mime_type="application/json",
                    )
                except ImportError:
                    config = {
                        "temperature": temperature,
                        "max_output_tokens": max_tokens,
                        "response_mime_type": "application/json",
                    }
                return client.models.generate_content_stream(
                    model=model,
                    contents=prompt,
                    config=config,
                )
            gen_model = client.GenerativeModel(model)
            return gen_model.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                    "response_mime_type": "application/json",
                },
                stream=True,
            )

        try:
            stream = self._execute_with_retry(_open_stream)
        except LLMProviderError as mapped:
            logger.error("[GeminiProvider] stream init failed (%s): %s", mapped.__class__.__name__, mapped.sanitized_message)
            raise

        accumulated_text = ""
        try:
            for chunk in stream:
                txt = getattr(chunk, "text", None)
                if txt:
                    accumulated_text += txt
                    yield {"type": "token", "content": txt}
        except Exception as exc:
            mapped = self._map_exception(exc)
            logger.error("[GeminiProvider] stream interrupted (%s): %s", mapped.__class__.__name__, mapped.sanitized_message)
            raise mapped from exc

        try:
            parsed = extract_json_object(accumulated_text)
        except Exception as exc:
            raise LLMInvalidResponseError(
                f"Gemini stream produced malformed JSON: {sanitize_error_message(exc)}",
                provider="gemini",
            ) from exc

        yield {
            "type": "final",
            "content": normalize_clinical_response(
                parsed,
                provider="gemini",
                model=model,
                fallback_used=False,
                simulated=False,
            ),
        }

    def health_check(self, live: bool = False) -> Dict[str, Any]:
        model = self._resolve_model()
        if not self.credentials_configured:
            return {
                "provider": "gemini",
                "model": model,
                "sdk": self._sdk_mode,
                "credentials_configured": False,
                "live_check_performed": False,
                "healthy": False,
                "status": "unconfigured",
                "details": "GEMINI_API_KEY is not set.",
            }
        if not live:
            return {
                "provider": "gemini",
                "model": model,
                "sdk": self._sdk_mode,
                "credentials_configured": True,
                "live_check_performed": False,
                "healthy": True,
                "status": "configured",
                "details": "Credentials configured (live API check not performed).",
            }
        try:
            if self._sdk_mode == "google-genai":
                models = list(self.client.models.list())
                names = [getattr(m, "name", "") for m in models]
                found = any(model in n for n in names) if names else True
            else:
                models = list(self.client.list_models())
                names = [getattr(m, "name", "") for m in models]
                found = any(model in n for n in names) if names else True
            return {
                "provider": "gemini",
                "model": model,
                "sdk": self._sdk_mode,
                "credentials_configured": True,
                "live_check_performed": True,
                "healthy": found,
                "status": "healthy" if found else "model_unavailable",
                "details": (
                    f"Connected to Gemini API; model '{model}' available."
                    if found
                    else f"Connected to Gemini API, but model '{model}' was not found."
                ),
            }
        except Exception as exc:
            mapped = self._map_exception(exc)
            return {
                "provider": "gemini",
                "model": model,
                "sdk": self._sdk_mode,
                "credentials_configured": True,
                "live_check_performed": True,
                "healthy": False,
                "status": "unhealthy",
                "details": mapped.sanitized_message,
            }
