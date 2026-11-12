"""
app/ai/config_manager.py

Thread-safe configuration manager for the AI Provider Layer.
Precedence policy:
  1. Environment variables (AI_PROVIDER, AI_FALLBACK_PROVIDER, AI_ENABLE_MOCK_FALLBACK,
     GROQ_MODEL, GEMINI_MODEL, CLINICAL_LLM_*) govern deployment defaults on startup.
  2. Runtime updates via PUT /api/ai/config update in-memory preferences (and persist
     non-secret settings to ai_config.json), without ever storing API keys.
"""

from __future__ import annotations

import json
import logging
import os
import threading
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).resolve().parent / "ai_config.json"
ALLOWED_PROVIDERS = {"groq", "gemini", "openai", "ollama", "lmstudio", "mock"}


def _parse_bool(raw: str | None, default: bool = False) -> bool:
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _default_model_for(provider: str) -> str:
    p = provider.lower()
    if p == "groq":
        return os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    if p == "gemini":
        return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    if p == "openai":
        return os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    if p == "ollama":
        return os.getenv("OLLAMA_MODEL", "llama3")
    if p == "lmstudio":
        return os.getenv("LMSTUDIO_MODEL", "local-model")
    return "mock-model"


class AIConfigManager:
    """
    Manages non-secret AI settings (provider, fallback_provider, model, temperature, etc.).
    Never reads or writes API keys to disk.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """
        Load settings with environment variables taking precedence over stale ai_config.json.
        """
        with self._lock:
            file_cfg: Dict[str, Any] = {}
            if CONFIG_PATH.exists():
                try:
                    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                        loaded = json.load(f)
                        if isinstance(loaded, dict):
                            file_cfg = loaded
                except Exception as e:
                    logger.warning("[AIConfigManager] Failed to read config file: %s", e)

            env_provider = os.getenv("AI_PROVIDER") or os.getenv("CLINICAL_LLM_PROVIDER")
            if env_provider:
                provider = env_provider.strip().lower()
            else:
                # Default to groq if GROQ_API_KEY is present, else respect non-stale file_cfg or groq
                file_provider = str(file_cfg.get("provider") or "").strip().lower()
                if file_provider in ALLOWED_PROVIDERS and not (
                    file_provider == "ollama" and file_cfg.get("model") == "mock-model"
                ):
                    provider = file_provider
                else:
                    provider = "groq"

            if provider not in ALLOWED_PROVIDERS:
                logger.warning("[AIConfigManager] Unknown provider '%s'; defaulting to 'groq'.", provider)
                provider = "groq"

            env_fallback = os.getenv("AI_FALLBACK_PROVIDER")
            fallback_provider = (
                env_fallback.strip().lower()
                if env_fallback is not None
                else str(file_cfg.get("fallback_provider") or ("gemini" if provider != "gemini" else "")).strip().lower()
            )
            if fallback_provider and fallback_provider not in ALLOWED_PROVIDERS:
                fallback_provider = "gemini"

            enable_mock = _parse_bool(
                os.getenv("AI_ENABLE_MOCK_FALLBACK"),
                default=bool(file_cfg.get("enable_mock_fallback", False)),
            )

            env_model = os.getenv("CLINICAL_LLM_MODEL")
            if env_model and env_model != "mock-model":
                model = env_model.strip()
            else:
                model = _default_model_for(provider)

            temp_raw = os.getenv("CLINICAL_LLM_TEMPERATURE")
            max_tok_raw = os.getenv("CLINICAL_LLM_MAX_TOKENS")
            stream_raw = os.getenv("CLINICAL_LLM_STREAMING")

            self._config = {
                "provider": provider,
                "fallback_provider": fallback_provider,
                "enable_mock_fallback": enable_mock,
                "model": model,
                "temperature": max(0.0, min(2.0, float(temp_raw if temp_raw is not None else file_cfg.get("temperature", 0.2)))),
                "max_tokens": max(1, int(max_tok_raw if max_tok_raw is not None else file_cfg.get("max_tokens", 1024))),
                "streaming": _parse_bool(stream_raw, default=bool(file_cfg.get("streaming", True))),
            }

    def save_config(self) -> None:
        """Persist non-secret configuration to disk (explicitly strips any secret-like keys)."""
        with self._lock:
            safe_cfg = {
                k: v
                for k, v in self._config.items()
                if "key" not in k.lower() and "secret" not in k.lower() and "token" not in k.lower() or k == "max_tokens"
            }
            try:
                with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                    json.dump(safe_cfg, f, indent=2)
            except Exception as e:
                logger.warning("[AIConfigManager] Failed to write config file: %s", e)

    def get_all(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._config)

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._config.get(key, default)

    def update(self, updates: Dict[str, Any]) -> None:
        """Validate and apply runtime configuration updates."""
        with self._lock:
            if "provider" in updates and updates["provider"] is not None:
                p = str(updates["provider"]).strip().lower()
                if p not in ALLOWED_PROVIDERS:
                    raise ValueError(f"Unsupported provider '{p}'. Allowed: {sorted(ALLOWED_PROVIDERS)}")
                self._config["provider"] = p
                if "model" not in updates or updates["model"] is None:
                    self._config["model"] = _default_model_for(p)
            if "fallback_provider" in updates and updates["fallback_provider"] is not None:
                fp = str(updates["fallback_provider"]).strip().lower()
                if fp and fp not in ALLOWED_PROVIDERS:
                    raise ValueError(f"Unsupported fallback_provider '{fp}'. Allowed: {sorted(ALLOWED_PROVIDERS)}")
                self._config["fallback_provider"] = fp
            if "enable_mock_fallback" in updates and updates["enable_mock_fallback"] is not None:
                self._config["enable_mock_fallback"] = bool(updates["enable_mock_fallback"])
            if "model" in updates and updates["model"] is not None:
                self._config["model"] = str(updates["model"]).strip()
            if "temperature" in updates and updates["temperature"] is not None:
                self._config["temperature"] = max(0.0, min(2.0, float(updates["temperature"])))
            if "max_tokens" in updates and updates["max_tokens"] is not None:
                self._config["max_tokens"] = max(1, int(updates["max_tokens"]))
            if "streaming" in updates and updates["streaming"] is not None:
                self._config["streaming"] = bool(updates["streaming"])

            self.save_config()


ai_config = AIConfigManager()
