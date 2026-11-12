"""
app/api/ai.py

FastAPI API Router for IntelliICU Multi-Provider AI Platform.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.rbac import require_permission
from app.models.user import User
from app.ai.config_manager import ALLOWED_PROVIDERS, ai_config
from app.ai.orchestrator import ProviderOrchestrator
from app.ai.providers.groq import GroqLLMProvider
from app.ai.providers.gemini import GeminiLLMProvider
from app.ai.providers.ollama import OllamaLLMProvider
from app.ai.providers.openai_provider import OpenAILLMProvider
from app.ai.providers.mock import MockLLMProvider
from app.ai.providers.lmstudio import LMStudioLLMProvider

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ai",
    tags=["Local & Cloud AI Platform"],
    dependencies=[Depends(get_current_user)],
)


class AIConfigUpdateRequest(BaseModel):
    provider: Optional[str] = Field(default=None, description="Primary AI Provider (groq, gemini, openai, ollama, lmstudio, mock)")
    fallback_provider: Optional[str] = Field(default=None, description="Fallback AI Provider (e.g., gemini)")
    enable_mock_fallback: Optional[bool] = Field(default=None, description="Explicit dev-only mock fallback toggle")
    model: Optional[str] = Field(default=None, description="Model identifier")
    temperature: Optional[float] = Field(default=None, description="Sampling temperature (0.0 to 2.0)")
    max_tokens: Optional[int] = Field(default=None, description="Max response tokens")
    streaming: Optional[bool] = Field(default=None, description="Enable response token streaming")


def _provider_health(name: str, live: bool = False) -> Dict[str, Any]:
    p = (name or "").strip().lower()
    if not p:
        return {"provider": None, "credentials_configured": False, "live_check_performed": False, "healthy": False, "status": "none"}
    if p == "groq":
        return GroqLLMProvider().health_check(live=live)
    if p == "gemini":
        return GeminiLLMProvider().health_check(live=live)
    if p == "mock":
        return {
            "provider": "mock",
            "model": "mock-model",
            "credentials_configured": True,
            "live_check_performed": False,
            "healthy": True,
            "status": "simulated",
            "details": "Development-only MockLLMProvider.",
        }
    if p == "ollama":
        ok = OllamaLLMProvider().health_check() if live else False
        return {
            "provider": "ollama",
            "credentials_configured": True,
            "live_check_performed": live,
            "healthy": ok,
            "status": "healthy" if ok else ("configured" if not live else "unhealthy"),
            "details": "Ollama reachable." if ok else "Ollama server check not passed.",
        }
    if p == "openai":
        has_client = getattr(OpenAILLMProvider(), "client", None) is not None
        return {
            "provider": "openai",
            "credentials_configured": has_client,
            "live_check_performed": False,
            "healthy": False,
            "status": "configured" if has_client else "unconfigured",
            "details": "OPENAI_API_KEY configured." if has_client else "OPENAI_API_KEY not set.",
        }
    if p == "lmstudio":
        model = LMStudioLLMProvider()._detect_model() if live else None
        return {
            "provider": "lmstudio",
            "credentials_configured": True,
            "live_check_performed": live,
            "healthy": model is not None,
            "status": "healthy" if model else "configured",
            "details": f"LM Studio model: {model}" if model else "LM Studio check not run or offline.",
        }
    return {"provider": p, "credentials_configured": False, "live_check_performed": False, "healthy": False, "status": "unknown"}


@router.get("/providers", summary="List Supported Providers")
def get_providers():
    """List all supported AI model providers."""
    return {
        "status": "success",
        "providers": [
            {"id": "groq", "name": "Groq Cloud (Primary)", "local": False},
            {"id": "gemini", "name": "Google Gemini (Fallback)", "local": False},
            {"id": "openai", "name": "OpenAI (GPT-4o)", "local": False},
            {"id": "ollama", "name": "Ollama (Local Llama/Qwen)", "local": True},
            {"id": "lmstudio", "name": "LM Studio (Local Server)", "local": True},
            {"id": "mock", "name": "Mock Clinical Provider (Dev Only)", "local": True},
        ],
    }


@router.get("/models", summary="List Available Models")
def get_models():
    """Report configured models for the active provider honestly."""
    provider_name = ai_config.get("provider", "groq")
    if provider_name == "groq":
        return {"provider": "groq", "models": ["openai/gpt-oss-120b", "llama-3.3-70b-versatile", "llama-3.1-8b-instant"]}
    if provider_name == "gemini":
        return {"provider": "gemini", "models": ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]}
    if provider_name == "ollama":
        models = OllamaLLMProvider().list_installed_models() or ["llama3", "qwen2.5", "mistral"]
        return {"provider": "ollama", "models": models}
    if provider_name == "openai":
        return {"provider": "openai", "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"]}
    if provider_name == "lmstudio":
        return {"provider": "lmstudio", "models": ["meta-llama-3-8b-instruct", "local-model"]}
    return {"provider": "mock", "models": ["mock-model"]}


@router.get("/config", summary="Get AI Settings")
def get_config():
    """Fetch non-secret runtime AI configuration settings."""
    return {
        "status": "success",
        "config": ai_config.get_all(),
    }


@router.put("/config", summary="Update AI Settings")
def update_config(
    request: AIConfigUpdateRequest,
    current_user: User = Depends(require_permission("Settings")),
):
    """Update runtime AI configurations (provider, model, temperature, etc.) immediately."""
    try:
        updates = {k: v for k, v in request.model_dump().items() if v is not None}
        if "provider" in updates and updates["provider"].lower() not in ALLOWED_PROVIDERS:
            raise HTTPException(status_code=400, detail=f"Unsupported provider '{updates['provider']}'.")
        if "fallback_provider" in updates and updates["fallback_provider"] and updates["fallback_provider"].lower() not in ALLOWED_PROVIDERS:
            raise HTTPException(status_code=400, detail=f"Unsupported fallback_provider '{updates['fallback_provider']}'.")
        ai_config.update(updates)
        logger.info("[AUDIT] AI config updated by user=%s role=%s keys=%s", current_user.username, current_user.role, list(updates.keys()))
        return {
            "status": "success",
            "message": "AI settings updated successfully",
            "config": ai_config.get_all(),
        }
    except HTTPException:
        raise
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as e:
        logger.error("[AI API] Failed to update config: %s", e)
        raise HTTPException(status_code=500, detail="Failed to update AI settings.")


@router.get("/health", summary="Provider Orchestrator Health Check")
def get_health(live: bool = Query(default=False, description="Perform live API connectivity check")):
    """
    Report truthful, separate statuses for primary, fallback, and effective providers.
    """
    primary_name = ai_config.get("provider", "groq")
    fallback_name = ai_config.get("fallback_provider", "gemini")

    primary_status = _provider_health(primary_name, live=live)
    fallback_status = _provider_health(fallback_name, live=live) if fallback_name else None

    effective = ProviderOrchestrator._last_effective_provider
    if not effective:
        if primary_status.get("healthy"):
            effective = primary_name
        elif fallback_status and fallback_status.get("healthy"):
            effective = fallback_name
        elif ai_config.get("enable_mock_fallback"):
            effective = "mock"
        else:
            effective = "unavailable"

    overall_healthy = bool(primary_status.get("healthy") or (fallback_status and fallback_status.get("healthy")))
    return {
        "provider": primary_name,
        "healthy": overall_healthy,
        "status": primary_status.get("status"),
        "details": primary_status.get("details"),
        "primary_provider": primary_status,
        "fallback_provider": fallback_status,
        "effective_provider": effective,
        "mock_fallback_enabled": bool(ai_config.get("enable_mock_fallback", False)),
        "live_check_performed": live,
        "last_error": ProviderOrchestrator._last_error,
    }
