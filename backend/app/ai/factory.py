"""
Clinical LLM Provider Factory.
Returns the centralized ProviderOrchestrator (Groq -> Gemini -> Optional Mock).
"""

from __future__ import annotations

from app.ai.orchestrator import ProviderOrchestrator
from app.ai.providers.base import BaseLLMProvider


def get_llm_provider() -> BaseLLMProvider:
    """
    Returns the centralized ProviderOrchestrator configured via environment & ai_config.
    """
    return ProviderOrchestrator()
