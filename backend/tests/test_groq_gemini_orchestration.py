"""
Comprehensive Unit & Integration Tests for Groq (Primary) -> Gemini (Fallback) -> Explicit Mock
Orchestration, Streaming Failover, Configuration Precedence, and AI API Endpoints.
Uses mocked SDK clients so zero external API quota is consumed.
"""

import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

os.environ.setdefault("DISABLE_SIMULATOR", "true")
os.environ.setdefault("ENABLE_DEMO_SEED", "false")

from app.ai.config_manager import ai_config  # noqa: E402
from app.ai.orchestrator import ProviderOrchestrator  # noqa: E402
from app.ai.providers.exceptions import (  # noqa: E402
    LLMAuthenticationError,
    LLMInvalidResponseError,
    LLMRateLimitError,
    LLMUnavailableError,
)
from app.ai.providers.gemini import GeminiLLMProvider  # noqa: E402
from app.ai.providers.groq import GroqLLMProvider  # noqa: E402
from app.main import app  # noqa: E402
from app.models.user import User  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402


VALID_CLINICAL_JSON = json.dumps(
    {
        "reasoning": "Elevated lactate and tachycardia indicate suspected septic shock.",
        "risk_drivers": ["Lactate 4.6 mmol/L", "HR 132 bpm"],
        "abnormal_vitals": ["HR 132 bpm", "SpO2 89%"],
        "abnormal_labs": ["Lactate 4.6 mmol/L"],
        "recommendations": ["Initiate sepsis bundle and repeat lactate."],
        "evidence": ["Surviving Sepsis Campaign 2021"],
        "confidence": 0.91,
    }
)


class _FakeAPIError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


class TestGroqProvider(unittest.TestCase):
    def test_init_with_and_without_credentials(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": ""}, clear=False):
            p = GroqLLMProvider()
            self.assertFalse(p.credentials_configured)
            with self.assertRaises(LLMAuthenticationError):
                p.generate("Check patient", {"vitals": {}})

        fake_client = MagicMock()
        p_with_client = GroqLLMProvider(client=fake_client)
        self.assertTrue(p_with_client.credentials_configured)

    def test_groq_successful_structured_response(self):
        fake_client = MagicMock()
        fake_client.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=VALID_CLINICAL_JSON))]
        )
        p = GroqLLMProvider(client=fake_client)
        res = p.generate("Assess sepsis risk", {"vitals": {"heart_rate": 132}})
        self.assertEqual(res["provider_metadata"]["provider"], "groq")
        self.assertFalse(res["provider_metadata"]["simulated"])
        self.assertIn("Elevated lactate", res["reasoning"])
        self.assertEqual(res["summary"], res["reasoning"])

    def test_groq_malformed_response_raises(self):
        fake_client = MagicMock()
        fake_client.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="NOT_JSON_OUTPUT"))]
        )
        p = GroqLLMProvider(client=fake_client)
        with self.assertRaises(LLMInvalidResponseError):
            p.generate("Assess", {})

    def test_groq_auth_and_rate_limit_errors(self):
        fake_client = MagicMock()
        fake_client.chat.completions.create.side_effect = _FakeAPIError("Invalid API key gsk_secret123456", 401)
        p = GroqLLMProvider(client=fake_client)
        with self.assertRaises(LLMAuthenticationError) as ctx:
            p.generate("Assess", {})
        self.assertNotIn("gsk_secret123456", str(ctx.exception))

        fake_client.chat.completions.create.side_effect = _FakeAPIError("Rate limit exceeded", 429)
        with self.assertRaises(LLMRateLimitError):
            p.generate("Assess", {})

    def test_groq_streaming_fragmented_and_empty_chunks(self):
        fake_client = MagicMock()
        mid = len(VALID_CLINICAL_JSON) // 2
        fake_client.chat.completions.create.return_value = iter([
            SimpleNamespace(choices=[]),  # usage/keepalive chunk
            SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=None), finish_reason=None)]),
            SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=VALID_CLINICAL_JSON[:mid]), finish_reason=None)]),
            SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=VALID_CLINICAL_JSON[mid:]), finish_reason="stop")]),
        ])
        p = GroqLLMProvider(client=fake_client)
        chunks = list(p.generate_stream("Assess", {"conversation_history": [{"role": "system", "content": "No json word here"}, {"role": "user", "content": "Hi"}]}))
        # Verify 'json' was auto-injected into system prompt for json_object mode
        sent_messages = fake_client.chat.completions.create.call_args.kwargs["messages"]
        self.assertIn("json", sent_messages[0]["content"].lower())
        self.assertEqual(chunks[-1]["type"], "final")
        self.assertEqual(chunks[-1]["content"]["provider_metadata"]["provider"], "groq")

    def test_groq_plain_text_mode_without_json_object(self):
        fake_client = MagicMock()
        fake_client.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="Plain clinical note."))]
        )
        p = GroqLLMProvider(client=fake_client)
        res = p.generate("Summarize", {"require_json": False})
        self.assertNotIn("response_format", fake_client.chat.completions.create.call_args.kwargs)
        self.assertEqual(res["reasoning"], "Plain clinical note.")


class TestGeminiProvider(unittest.TestCase):
    def test_gemini_successful_and_failure_handling(self):
        fake_client = MagicMock()
        fake_client.models.generate_content.return_value = SimpleNamespace(text=VALID_CLINICAL_JSON)
        p = GeminiLLMProvider(client=fake_client)
        res = p.generate("Assess", {"vitals": {}})
        self.assertEqual(res["provider_metadata"]["provider"], "gemini")
        self.assertFalse(res["provider_metadata"]["fallback_used"])

        fake_client.models.generate_content.side_effect = _FakeAPIError("RESOURCE_EXHAUSTED quota", 429)
        with patch("app.ai.providers.gemini.time.sleep"):
            with self.assertRaises(LLMRateLimitError):
                p.generate("Assess", {})

    def test_gemini_transient_503_retries_and_recovers(self):
        fake_client = MagicMock()
        fake_client.models.generate_content.side_effect = [
            _FakeAPIError("503 UNAVAILABLE: high demand", 503),
            SimpleNamespace(text=VALID_CLINICAL_JSON),
        ]
        p = GeminiLLMProvider(client=fake_client)
        with patch("app.ai.providers.gemini.time.sleep"):
            res = p.generate("Assess", {"vitals": {}})
        self.assertEqual(res["provider_metadata"]["provider"], "gemini")
        self.assertEqual(fake_client.models.generate_content.call_count, 2)


class TestOrchestratorFailoverAndStreaming(unittest.TestCase):
    def setUp(self):
        ai_config.update({"provider": "groq", "fallback_provider": "gemini", "enable_mock_fallback": False})

    def test_groq_success_does_not_call_gemini(self):
        groq = MagicMock()
        groq.provider_name = "groq"
        groq.generate.return_value = {"reasoning": "ok", "provider_metadata": {"provider": "groq", "fallback_used": False}}
        gemini = MagicMock()
        gemini.provider_name = "gemini"

        orch = ProviderOrchestrator(primary_provider=groq, fallback_provider=gemini)
        res = orch.generate("Q", {})
        self.assertEqual(res["provider_metadata"]["provider"], "groq")
        gemini.generate.assert_not_called()

    def test_groq_failure_falls_back_to_gemini(self):
        groq = MagicMock()
        groq.provider_name = "groq"
        groq.generate.side_effect = LLMRateLimitError("429", provider="groq")

        gemini = MagicMock()
        gemini.provider_name = "gemini"
        gemini.generate.return_value = {"reasoning": "from gemini", "provider_metadata": {"provider": "gemini", "fallback_used": False}}

        orch = ProviderOrchestrator(primary_provider=groq, fallback_provider=gemini)
        res = orch.generate("Q", {})
        self.assertEqual(res["provider_metadata"]["provider"], "gemini")
        self.assertTrue(res["provider_metadata"]["fallback_used"])

    def test_both_fail_raises_controlled_error_without_mock(self):
        groq = MagicMock()
        groq.provider_name = "groq"
        groq.generate.side_effect = LLMRateLimitError("429", provider="groq")

        gemini = MagicMock()
        gemini.provider_name = "gemini"
        gemini.generate.side_effect = LLMAuthenticationError("401", provider="gemini")

        orch = ProviderOrchestrator(primary_provider=groq, fallback_provider=gemini)
        with self.assertRaises(LLMUnavailableError):
            orch.generate("Q", {})

    def test_explicit_mock_fallback_when_enabled(self):
        ai_config.update({"provider": "groq", "fallback_provider": "gemini", "enable_mock_fallback": True})
        groq = MagicMock()
        groq.provider_name = "groq"
        groq.generate.side_effect = LLMRateLimitError("429", provider="groq")
        gemini = MagicMock()
        gemini.provider_name = "gemini"
        gemini.generate.side_effect = LLMRateLimitError("429", provider="gemini")

        orch = ProviderOrchestrator(primary_provider=groq, fallback_provider=gemini)
        res = orch.generate("Check sepsis", {"vitals": {"heart_rate": 130}})
        self.assertTrue(res["provider_metadata"]["simulated"])
        self.assertEqual(res["provider_metadata"]["provider"], "mock")

    def test_streaming_pre_token_failover_and_mid_stream_error(self):
        # 1. Pre-token failure -> Gemini stream
        groq = MagicMock()
        groq.provider_name = "groq"
        groq.generate_stream.side_effect = LLMRateLimitError("429", provider="groq")

        gemini = MagicMock()
        gemini.provider_name = "gemini"
        gemini.generate_stream.return_value = iter([
            {"type": "token", "content": "{"},
            {"type": "final", "content": {"reasoning": "ok", "provider_metadata": {"provider": "gemini"}}},
        ])

        orch = ProviderOrchestrator(primary_provider=groq, fallback_provider=gemini)
        chunks = list(orch.generate_stream("Q", {}))
        self.assertEqual(chunks[-1]["type"], "final")
        self.assertTrue(chunks[-1]["content"]["provider_metadata"]["fallback_used"])

        # 2. Mid-stream failure after first token -> must NOT call Gemini, must yield error event
        def broken_stream(*_args, **_kwargs):
            yield {"type": "token", "content": "partial"}
            raise RuntimeError("socket reset")

        groq2 = MagicMock()
        groq2.provider_name = "groq"
        groq2.generate_stream.side_effect = broken_stream
        gemini2 = MagicMock()
        gemini2.provider_name = "gemini"

        orch2 = ProviderOrchestrator(primary_provider=groq2, fallback_provider=gemini2)
        chunks2 = list(orch2.generate_stream("Q", {}))
        self.assertEqual(chunks2[0]["type"], "token")
        self.assertEqual(chunks2[1]["type"], "error")
        gemini2.generate_stream.assert_not_called()


class TestAIConfigAndAPIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.state.startup_complete = True
        cls.client = TestClient(app)
        cls.admin = User(
            id="usr-admin",
            username="admin_test",
            email="admin_test@intelliicu.org",
            hashed_password="x",
            role="HospitalAdmin",
            department="Administration",
            is_active=True,
        )
        cls.headers = {
            "Authorization": f"Bearer {AuthService.create_access_token({'sub': 'admin_test', 'role': 'HospitalAdmin'})}"
        }

    def test_env_precedence_over_stale_json(self):
        with patch.dict(os.environ, {"AI_PROVIDER": "groq", "AI_FALLBACK_PROVIDER": "gemini", "AI_ENABLE_MOCK_FALLBACK": "false"}):
            ai_config.load_config()
            self.assertEqual(ai_config.get("provider"), "groq")
            self.assertEqual(ai_config.get("fallback_provider"), "gemini")
            self.assertFalse(ai_config.get("enable_mock_fallback"))

    def test_ai_config_and_health_endpoints(self):
        with patch("app.core.dependencies.auth.UserRepository.get_by_username", return_value=self.admin), \
             patch("app.core.dependencies.rbac.RBACRepository.get_permissions_for_role", return_value=["Settings", "ClinicalAI"]):
            providers_resp = self.client.get("/api/ai/providers", headers=self.headers)
            self.assertEqual(providers_resp.status_code, 200)
            ids = [p["id"] for p in providers_resp.json()["providers"]]
            self.assertIn("groq", ids)
            self.assertIn("gemini", ids)

            cfg_resp = self.client.get("/api/ai/config", headers=self.headers)
            self.assertEqual(cfg_resp.status_code, 200)
            self.assertNotIn("GROQ_API_KEY", json.dumps(cfg_resp.json()))

            health_resp = self.client.get("/api/ai/health?live=false", headers=self.headers)
            self.assertEqual(health_resp.status_code, 200)
            body = health_resp.json()
            self.assertIn("primary_provider", body)
            self.assertIn("fallback_provider", body)
            self.assertIn("effective_provider", body)
            self.assertFalse(body["live_check_performed"])

            # Invalid provider rejected
            bad_put = self.client.put("/api/ai/config", json={"provider": "invalid_xyz"}, headers=self.headers)
            self.assertEqual(bad_put.status_code, 400)


if __name__ == "__main__":
    unittest.main()
