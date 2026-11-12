"""
Groq LLM Provider.
Integrates Groq's OpenAI-compatible Chat Completions API with structured JSON,
streaming, timeouts, sanitized logging, and typed exception mapping.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, Generator, List, Optional

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

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"


class GroqLLMProvider(BaseLLMProvider):
    """Primary clinical LLM provider backed by Groq."""

    provider_name = "groq"

    def __init__(self, client: Any = None) -> None:
        self.api_key = (os.getenv("GROQ_API_KEY") or "").strip()
        self.default_model = (os.getenv("GROQ_MODEL") or DEFAULT_GROQ_MODEL).strip()
        self.timeout = float(os.getenv("GROQ_TIMEOUT_SECONDS", "30.0"))
        self.client = client
        self._sdk_error: Optional[str] = None

        if self.client is None and self.api_key:
            try:
                from openai import OpenAI

                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=GROQ_BASE_URL,
                    timeout=self.timeout,
                    max_retries=1,
                )
            except ImportError:
                logger.warning("[GroqProvider] openai SDK is not installed.")
                self._sdk_error = "openai SDK is not installed."
                self.client = None

    @property
    def credentials_configured(self) -> bool:
        return bool(self.api_key or self.client is not None)

    def _resolve_model(self) -> str:
        configured = ai_config.get("model")
        active_provider = (ai_config.get("provider") or "").lower()
        if active_provider == "groq" and configured and configured != "mock-model":
            return str(configured)
        return self.default_model

    def _build_messages(self, question: str, context: Dict[str, Any], require_json: bool = True) -> List[Dict[str, str]]:
        history = context.get("conversation_history")
        if isinstance(history, list) and history:
            messages = [dict(m) for m in history]
            if require_json:
                has_json_word = any("json" in str(m.get("content", "")).lower() for m in messages)
                if not has_json_word:
                    if messages[0].get("role") == "system":
                        messages[0]["content"] = f"{CLINICAL_SYSTEM_PROMPT}\n\n{messages[0]['content']}"
                    else:
                        messages.insert(0, {"role": "system", "content": CLINICAL_SYSTEM_PROMPT})
            return messages

        user_content = (
            f"Patient Clinical Context:\n{json.dumps(context, indent=2, default=str)}\n\n"
            f"Question:\n{question}"
        )
        sys_prompt = CLINICAL_SYSTEM_PROMPT if require_json else (
            "You are an expert ICU Clinical Decision Support AI. Answer clearly and concisely based on the provided context."
        )
        return [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_content},
        ]

    def _effective_max_tokens(self) -> int:
        configured = int(ai_config.get("max_tokens", 2048))
        # Reasoning models like openai/gpt-oss-120b consume reasoning + output tokens;
        # ensure at least 2048 tokens for structured JSON responses to avoid mid-JSON truncation.
        return max(configured, 2048)

    def _map_exception(self, exc: Exception) -> LLMProviderError:
        if isinstance(exc, LLMProviderError):
            return exc
        status = getattr(exc, "status_code", None)
        msg = sanitize_error_message(exc)
        low = msg.lower()

        if status in (401, 403) or "invalid api key" in low or "authentication" in low or "unauthorized" in low:
            return LLMAuthenticationError(f"Groq authentication failed: {msg}", provider="groq", status_code=status or 401)
        if status == 429 or "rate limit" in low or "quota" in low:
            return LLMRateLimitError(f"Groq rate limit exceeded: {msg}", provider="groq", status_code=429)
        if status == 404 or "model" in low and ("not found" in low or "does not exist" in low):
            return LLMModelNotFoundError(f"Groq model unavailable: {msg}", provider="groq", status_code=404)
        if "timeout" in low or "timed out" in low or exc.__class__.__name__.lower().endswith("timeouterror"):
            return LLMTimeoutError(f"Groq request timed out: {msg}", provider="groq")
        return LLMNetworkError(f"Groq request failed: {msg}", provider="groq", status_code=status or 502)

    def _require_client(self) -> Any:
        if self.client is None:
            if getattr(self, "_sdk_error", None):
                raise LLMProviderError(self._sdk_error, provider="groq", status_code=500)
            raise LLMAuthenticationError(
                "GROQ_API_KEY is not configured.",
                provider="groq",
                status_code=401,
            )
        return self.client

    def generate(self, question: str, context: Dict[str, Any]) -> Dict[str, Any]:
        client = self._require_client()
        model = self._resolve_model()
        temperature = float(ai_config.get("temperature", 0.2))
        max_tokens = self._effective_max_tokens()
        require_json = bool(context.get("require_json", True))
        messages = self._build_messages(question, context, require_json=require_json)

        try:
            kwargs: Dict[str, Any] = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            if require_json:
                kwargs["response_format"] = {"type": "json_object"}
            response = client.chat.completions.create(**kwargs)
            raw_text = response.choices[0].message.content or ""
        except Exception as exc:
            mapped = self._map_exception(exc)
            logger.error("[GroqProvider] generate failed (%s): %s", mapped.__class__.__name__, mapped.sanitized_message)
            raise mapped from exc

        if not require_json:
            return normalize_clinical_response(
                {"reasoning": raw_text},
                provider="groq",
                model=model,
                fallback_used=False,
                simulated=False,
            )

        try:
            parsed = extract_json_object(raw_text)
        except Exception as exc:
            logger.error("[GroqProvider] malformed JSON response from model=%s", model)
            raise LLMInvalidResponseError(
                f"Groq returned malformed JSON: {sanitize_error_message(exc)}",
                provider="groq",
            ) from exc

        return normalize_clinical_response(parsed, provider="groq", model=model, fallback_used=False, simulated=False)

    def generate_stream(self, question: str, context: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        client = self._require_client()
        model = self._resolve_model()
        temperature = float(ai_config.get("temperature", 0.2))
        max_tokens = self._effective_max_tokens()
        require_json = bool(context.get("require_json", True))
        messages = self._build_messages(question, context, require_json=require_json)

        try:
            kwargs: Dict[str, Any] = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True,
            }
            if require_json:
                kwargs["response_format"] = {"type": "json_object"}
            stream = client.chat.completions.create(**kwargs)
        except Exception as exc:
            mapped = self._map_exception(exc)
            logger.error("[GroqProvider] stream init failed (%s): %s", mapped.__class__.__name__, mapped.sanitized_message)
            raise mapped from exc

        accumulated_text = ""
        finish_reason = None
        try:
            for chunk in stream:
                choices = getattr(chunk, "choices", None) or []
                if not choices:
                    continue
                choice = choices[0]
                if getattr(choice, "finish_reason", None):
                    finish_reason = choice.finish_reason
                delta = getattr(choice, "delta", None)
                token = getattr(delta, "content", None) if delta is not None else None
                if token:
                    accumulated_text += token
                    yield {"type": "token", "content": token}
        except Exception as exc:
            mapped = self._map_exception(exc)
            logger.error("[GroqProvider] stream interrupted (%s): %s", mapped.__class__.__name__, mapped.sanitized_message)
            raise mapped from exc

        if not accumulated_text.strip():
            raise LLMInvalidResponseError(
                f"Groq stream completed with empty content (finish_reason={finish_reason}).",
                provider="groq",
            )

        if not require_json:
            yield {
                "type": "final",
                "content": normalize_clinical_response(
                    {"reasoning": accumulated_text},
                    provider="groq",
                    model=model,
                    fallback_used=False,
                    simulated=False,
                ),
            }
            return

        try:
            parsed = extract_json_object(accumulated_text)
        except Exception as exc:
            raise LLMInvalidResponseError(
                f"Groq stream produced malformed JSON (finish_reason={finish_reason}): {sanitize_error_message(exc)}",
                provider="groq",
            ) from exc

        yield {
            "type": "final",
            "content": normalize_clinical_response(
                parsed,
                provider="groq",
                model=model,
                fallback_used=False,
                simulated=False,
            ),
        }

    def health_check(self, live: bool = False) -> Dict[str, Any]:
        model = self._resolve_model()
        if not self.credentials_configured:
            return {
                "provider": "groq",
                "model": model,
                "credentials_configured": False,
                "live_check_performed": False,
                "healthy": False,
                "status": "unconfigured",
                "details": "GROQ_API_KEY is not set.",
            }
        if getattr(self, "_sdk_error", None):
            return {
                "provider": "groq",
                "model": model,
                "credentials_configured": True,
                "live_check_performed": False,
                "healthy": False,
                "status": "sdk_missing",
                "details": self._sdk_error,
            }
        if not live:
            return {
                "provider": "groq",
                "model": model,
                "credentials_configured": True,
                "live_check_performed": False,
                "healthy": True,
                "status": "configured",
                "details": "Credentials configured (live API check not performed).",
            }
        try:
            models_resp = self.client.models.list()
            available_ids = [getattr(m, "id", "") for m in getattr(models_resp, "data", [])]
            model_available = (model in available_ids) if available_ids else True
            return {
                "provider": "groq",
                "model": model,
                "credentials_configured": True,
                "live_check_performed": True,
                "healthy": model_available,
                "status": "healthy" if model_available else "model_unavailable",
                "details": (
                    f"Connected to Groq API; model '{model}' available."
                    if model_available
                    else f"Connected to Groq API, but model '{model}' was not listed."
                ),
            }
        except Exception as exc:
            mapped = self._map_exception(exc)
            return {
                "provider": "groq",
                "model": model,
                "credentials_configured": True,
                "live_check_performed": True,
                "healthy": False,
                "status": "unhealthy",
                "details": mapped.sanitized_message,
            }
