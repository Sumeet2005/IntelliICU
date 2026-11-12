"""
Centralized LLM Provider Orchestrator.
Implements Groq (primary) -> Gemini (fallback) -> Explicit Mock (dev-only when enabled).
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Generator, Optional

from app.ai.config_manager import ai_config
from app.ai.providers.base import BaseLLMProvider, sanitize_error_message
from app.ai.providers.exceptions import LLMProviderError, LLMUnavailableError
from app.ai.providers.gemini import GeminiLLMProvider
from app.ai.providers.groq import GroqLLMProvider
from app.ai.providers.lmstudio import LMStudioLLMProvider
from app.ai.providers.mock import MockLLMProvider
from app.ai.providers.ollama import OllamaLLMProvider
from app.ai.providers.openai_provider import OpenAILLMProvider

logger = logging.getLogger(__name__)


class ProviderOrchestrator(BaseLLMProvider):
    """
    Coordinates primary and fallback LLM providers with explicit failure handling.
    Never silently substitutes MockLLMProvider unless AI_ENABLE_MOCK_FALLBACK=true
    or provider=='mock' is explicitly configured.
    """

    provider_name = "orchestrator"
    _last_error: Optional[str] = None
    _last_effective_provider: Optional[str] = None

    def __init__(
        self,
        primary_provider: Optional[BaseLLMProvider] = None,
        fallback_provider: Optional[BaseLLMProvider] = None,
        mock_provider: Optional[BaseLLMProvider] = None,
    ) -> None:
        self._custom_primary = primary_provider
        self._custom_fallback = fallback_provider
        self._custom_mock = mock_provider

    @staticmethod
    def _build_provider(name: str) -> BaseLLMProvider:
        p = (name or "").strip().lower()
        if p == "groq":
            return GroqLLMProvider()
        if p == "gemini":
            return GeminiLLMProvider()
        if p == "openai":
            return OpenAILLMProvider()
        if p == "ollama":
            return OllamaLLMProvider()
        if p == "lmstudio":
            return LMStudioLLMProvider()
        if p == "mock":
            return MockLLMProvider()
        raise LLMUnavailableError(f"Unknown LLM provider '{name}'.")

    def _primary_name(self) -> str:
        return (ai_config.get("provider") or os.getenv("AI_PROVIDER") or "groq").strip().lower()

    def _fallback_name(self) -> str:
        return (ai_config.get("fallback_provider") or os.getenv("AI_FALLBACK_PROVIDER") or "").strip().lower()

    def _mock_enabled(self) -> bool:
        return bool(ai_config.get("enable_mock_fallback", False))

    def _get_primary(self) -> BaseLLMProvider:
        if self._custom_primary is not None:
            return self._custom_primary
        return self._build_provider(self._primary_name())

    def _get_fallback(self) -> Optional[BaseLLMProvider]:
        if self._custom_fallback is not None:
            return self._custom_fallback
        fb_name = self._fallback_name()
        if not fb_name or fb_name == self._primary_name():
            return None
        return self._build_provider(fb_name)

    def _get_mock(self) -> MockLLMProvider:
        if self._custom_mock is not None:
            return self._custom_mock  # type: ignore[return-value]
        return MockLLMProvider()

    @staticmethod
    def _mark_mock_response(resp: Dict[str, Any]) -> Dict[str, Any]:
        meta = dict(resp.get("provider_metadata") or {})
        meta.update({"provider": "mock", "model": "mock-model", "simulated": True})
        resp["provider_metadata"] = meta
        resp["simulated"] = True
        return resp

    def generate(self, question: str, context: Dict[str, Any]) -> Dict[str, Any]:
        primary_name = self._primary_name()

        # Explicit mock mode (development/testing only)
        if primary_name == "mock":
            ProviderOrchestrator._last_effective_provider = "mock"
            return self._mark_mock_response(self._get_mock().generate(question, context))

        primary = self._get_primary()
        primary_err: Optional[str] = None

        try:
            result = primary.generate(question, context)
            ProviderOrchestrator._last_error = None
            ProviderOrchestrator._last_effective_provider = getattr(primary, "provider_name", primary_name)
            return result
        except Exception as exc:
            primary_err = sanitize_error_message(exc)
            ProviderOrchestrator._last_error = f"{primary_name}: {primary_err}"
            logger.warning("[Orchestrator] Primary provider '%s' failed: %s", primary_name, primary_err)

        # Attempt configured fallback provider (e.g., Gemini)
        fallback = self._get_fallback()
        fallback_name = getattr(fallback, "provider_name", self._fallback_name()) if fallback else ""
        if fallback is not None and fallback_name != "mock":
            try:
                result = fallback.generate(question, context)
                meta = dict(result.get("provider_metadata") or {})
                meta["fallback_used"] = True
                meta["primary_provider"] = primary_name
                meta["primary_error"] = primary_err
                result["provider_metadata"] = meta
                ProviderOrchestrator._last_effective_provider = fallback_name
                logger.info("[Orchestrator] Fallback provider '%s' succeeded.", fallback_name)
                return result
            except Exception as fb_exc:
                fb_err = sanitize_error_message(fb_exc)
                ProviderOrchestrator._last_error = f"{primary_name}: {primary_err} | {fallback_name}: {fb_err}"
                logger.error("[Orchestrator] Fallback provider '%s' failed: %s", fallback_name, fb_err)

        # Explicitly configured development mock fallback
        if self._mock_enabled():
            logger.warning("[Orchestrator] Using explicitly enabled MockLLMProvider after provider failures.")
            ProviderOrchestrator._last_effective_provider = "mock"
            resp = self._mark_mock_response(self._get_mock().generate(question, context))
            resp["provider_metadata"]["fallback_used"] = True
            resp["provider_metadata"]["primary_error"] = primary_err
            return resp

        raise LLMUnavailableError(
            f"All configured clinical LLM providers failed ({ProviderOrchestrator._last_error}).",
            provider="orchestrator",
            status_code=503,
        )

    def generate_stream(self, question: str, context: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        primary_name = self._primary_name()

        if primary_name == "mock":
            ProviderOrchestrator._last_effective_provider = "mock"
            for chunk in self._get_mock().generate_stream(question, context):
                if chunk.get("type") == "final" and isinstance(chunk.get("content"), dict):
                    chunk["content"] = self._mark_mock_response(chunk["content"])
                yield chunk
            return

        primary = self._get_primary()
        emitted_tokens = False
        primary_err: Optional[str] = None

        try:
            for chunk in primary.generate_stream(question, context):
                if chunk.get("type") == "token":
                    emitted_tokens = True
                yield chunk
            ProviderOrchestrator._last_error = None
            ProviderOrchestrator._last_effective_provider = getattr(primary, "provider_name", primary_name)
            return
        except Exception as exc:
            primary_err = sanitize_error_message(exc)
            ProviderOrchestrator._last_error = f"{primary_name}: {primary_err}"
            if emitted_tokens:
                # Never restart another provider mid-stream after tokens have been emitted
                logger.error("[Orchestrator] Primary '%s' failed mid-stream: %s", primary_name, primary_err)
                yield {
                    "type": "error",
                    "error": f"Stream interrupted on {primary_name}: {primary_err}",
                    "provider": primary_name,
                }
                return
            logger.warning("[Orchestrator] Primary '%s' failed before first token: %s", primary_name, primary_err)

        # Pre-token failover to fallback provider
        fallback = self._get_fallback()
        fallback_name = getattr(fallback, "provider_name", self._fallback_name()) if fallback else ""
        if fallback is not None and fallback_name != "mock":
            fb_emitted = False
            try:
                for chunk in fallback.generate_stream(question, context):
                    if chunk.get("type") == "token":
                        fb_emitted = True
                    elif chunk.get("type") == "final" and isinstance(chunk.get("content"), dict):
                        meta = dict(chunk["content"].get("provider_metadata") or {})
                        meta["fallback_used"] = True
                        meta["primary_provider"] = primary_name
                        meta["primary_error"] = primary_err
                        chunk["content"]["provider_metadata"] = meta
                    yield chunk
                ProviderOrchestrator._last_effective_provider = fallback_name
                return
            except Exception as fb_exc:
                fb_err = sanitize_error_message(fb_exc)
                ProviderOrchestrator._last_error = f"{primary_name}: {primary_err} | {fallback_name}: {fb_err}"
                logger.error("[Orchestrator] Fallback '%s' stream failed: %s", fallback_name, fb_err)
                if fb_emitted:
                    yield {
                        "type": "error",
                        "error": f"Stream interrupted on fallback {fallback_name}: {fb_err}",
                        "provider": fallback_name,
                    }
                    return

        if self._mock_enabled():
            ProviderOrchestrator._last_effective_provider = "mock"
            for chunk in self._get_mock().generate_stream(question, context):
                if chunk.get("type") == "final" and isinstance(chunk.get("content"), dict):
                    chunk["content"] = self._mark_mock_response(chunk["content"])
                    chunk["content"]["provider_metadata"]["fallback_used"] = True
                yield chunk
            return

        yield {
            "type": "error",
            "error": f"All configured clinical LLM providers failed ({ProviderOrchestrator._last_error}).",
            "provider": "orchestrator",
        }
