"""
Structured exception hierarchy for IntelliICU LLM providers.
All messages must remain sanitized and never include API keys or patient PII.
"""

from __future__ import annotations

from typing import Optional


class LLMProviderError(Exception):
    """Base exception for LLM provider failures."""

    def __init__(
        self,
        message: str,
        *,
        provider: str = "unknown",
        status_code: Optional[int] = None,
        retryable: bool = False,
    ) -> None:
        super().__init__(message)
        self.provider = provider
        self.status_code = status_code
        self.retryable = retryable
        self.sanitized_message = message


class LLMAuthenticationError(LLMProviderError):
    """Raised when provider API credentials are missing, invalid, or rejected."""

    def __init__(self, message: str, *, provider: str = "unknown", status_code: Optional[int] = 401) -> None:
        super().__init__(message, provider=provider, status_code=status_code, retryable=False)


class LLMRateLimitError(LLMProviderError):
    """Raised when provider rate limits or quotas are exceeded."""

    def __init__(self, message: str, *, provider: str = "unknown", status_code: Optional[int] = 429) -> None:
        super().__init__(message, provider=provider, status_code=status_code, retryable=True)


class LLMModelNotFoundError(LLMProviderError):
    """Raised when the configured model is unavailable or unsupported."""

    def __init__(self, message: str, *, provider: str = "unknown", status_code: Optional[int] = 404) -> None:
        super().__init__(message, provider=provider, status_code=status_code, retryable=False)


class LLMTimeoutError(LLMProviderError):
    """Raised when a provider request exceeds the configured timeout."""

    def __init__(self, message: str, *, provider: str = "unknown", status_code: Optional[int] = 504) -> None:
        super().__init__(message, provider=provider, status_code=status_code, retryable=True)


class LLMNetworkError(LLMProviderError):
    """Raised on network or transport failures communicating with a provider."""

    def __init__(self, message: str, *, provider: str = "unknown", status_code: Optional[int] = 502) -> None:
        super().__init__(message, provider=provider, status_code=status_code, retryable=True)


class LLMInvalidResponseError(LLMProviderError):
    """Raised when a provider returns malformed or non-JSON clinical output."""

    def __init__(self, message: str, *, provider: str = "unknown", status_code: Optional[int] = 502) -> None:
        super().__init__(message, provider=provider, status_code=status_code, retryable=False)


class LLMUnavailableError(LLMProviderError):
    """Raised when both primary and fallback LLM providers fail."""

    def __init__(self, message: str, *, provider: str = "orchestrator", status_code: Optional[int] = 503) -> None:
        super().__init__(message, provider=provider, status_code=status_code, retryable=False)
