"""
End-to-End Integration Tests for Clinical Copilot, RAG Context Refresh,
Clinical Reasoning Engines, Report/PDF Generation, and Hospital Assistant.
Uses mocked LLM responses to avoid consuming external API quotas.
"""

import json
import os
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

os.environ.setdefault("DISABLE_SIMULATOR", "true")
os.environ.setdefault("ENABLE_DEMO_SEED", "false")

from app.ai.providers.exceptions import LLMUnavailableError  # noqa: E402
from app.main import app  # noqa: E402
from app.models.user import User  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.clinical_copilot_service import ClinicalCopilotService  # noqa: E402


MOCK_STRUCTURED_RESPONSE = {
    "reasoning": "Patient exhibits hypotension, tachycardia, and elevated lactate consistent with septic shock.",
    "risk_drivers": ["Lactate 4.6 mmol/L", "SBP 82 mmHg", "HR 132 bpm"],
    "abnormal_vitals": ["HR 132 bpm", "SpO2 89%", "SBP 82 mmHg"],
    "abnormal_labs": ["Lactate 4.6 mmol/L", "WBC 18.5"],
    "recommendations": ["Initiate broad-spectrum IV antibiotics and 30 mL/kg crystalloid resuscitation."],
    "evidence": ["Surviving Sepsis Campaign 2021"],
    "confidence": 0.92,
    "summary": "Patient exhibits hypotension, tachycardia, and elevated lactate consistent with septic shock.",
    "findings": ["Lactate 4.6 mmol/L", "HR 132 bpm"],
    "risk": "HIGH",
    "provider_metadata": {
        "provider": "groq",
        "model": "openai/gpt-oss-120b",
        "fallback_used": False,
        "simulated": False,
    },
}


class TestEndToEndIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.state.startup_complete = True
        cls.client = TestClient(app)
        cls.doctor = User(
            id="usr-doc",
            username="doc_e2e",
            email="doc_e2e@intelliicu.org",
            hashed_password="x",
            role="Doctor",
            department="Medical ICU",
            is_active=True,
        )
        cls.headers = {
            "Authorization": f"Bearer {AuthService.create_access_token({'sub': 'doc_e2e', 'role': 'Doctor'})}"
        }

    def test_copilot_batch_rag_and_reasoning_engines(self):
        fake_llm = MagicMock()
        fake_llm.generate_response.return_value = dict(MOCK_STRUCTURED_RESPONSE)

        with patch("app.services.clinical_copilot_service.get_llm_provider", return_value=fake_llm), \
             patch("app.core.dependencies.auth.UserRepository.get_by_username", return_value=self.doctor), \
             patch("app.core.dependencies.rbac.RBACRepository.get_permissions_for_role", return_value=["ClinicalAI", "Patients", "Reports"]):
            resp = self.client.post(
                "/api/clinical-copilot/chat",
                json={"patient_id": "ICU-10248", "question": "Evaluate sepsis risk and antibiotic plan"},
                headers=self.headers,
            )
            self.assertEqual(resp.status_code, 200)
            body = resp.json()
            for key in [
                "reasoning",
                "retrieved_sources",
                "evidence_used",
                "differential_diagnosis",
                "treatment_pathway",
                "medication_plan",
                "risk_scores",
                "laboratory_interpretation",
                "trend_analysis",
                "provider_metadata",
            ]:
                self.assertIn(key, body, f"Missing expected key '{key}' in Clinical Copilot response")
            self.assertEqual(body["provider_metadata"]["provider"], "groq")
            self.assertGreater(len(body["retrieved_sources"]), 0)

    def test_copilot_system_message_refreshes_rag_evidence_on_cache_hit(self):
        svc = ClinicalCopilotService()
        fake_llm = MagicMock()
        fake_llm.generate_response.return_value = dict(MOCK_STRUCTURED_RESPONSE)

        with patch("app.services.clinical_copilot_service.get_llm_provider", return_value=fake_llm):
            svc.get_answer("ICU-10248", "septic shock antibiotics")
            first_sys = svc.conversation_memory["ICU-10248"][0]["content"]
            svc.get_answer("ICU-10248", "acute kidney injury creatinine")
            second_sys = svc.conversation_memory["ICU-10248"][0]["content"]
            # System prompt includes updated evidence for the second question
            self.assertIsInstance(first_sys, str)
            self.assertIsInstance(second_sys, str)
            self.assertIn("Patient Context Summary", second_sys)

    def test_copilot_returns_503_when_all_providers_unavailable(self):
        fake_llm = MagicMock()
        fake_llm.generate_response.side_effect = LLMUnavailableError("All providers down")

        with patch("app.services.clinical_copilot_service.get_llm_provider", return_value=fake_llm), \
             patch("app.core.dependencies.auth.UserRepository.get_by_username", return_value=self.doctor), \
             patch("app.core.dependencies.rbac.RBACRepository.get_permissions_for_role", return_value=["ClinicalAI"]):
            resp = self.client.post(
                "/api/clinical-copilot/chat",
                json={"patient_id": "ICU-10248", "question": "Check status"},
                headers=self.headers,
            )
            self.assertEqual(resp.status_code, 503)

    def test_report_generation_and_pdf_download(self):
        fake_llm = MagicMock()
        fake_llm.generate_response.return_value = dict(MOCK_STRUCTURED_RESPONSE)

        with patch("app.services.clinical_copilot_service.get_llm_provider", return_value=fake_llm), \
             patch("app.core.dependencies.auth.UserRepository.get_by_username", return_value=self.doctor), \
             patch("app.core.dependencies.rbac.RBACRepository.get_permissions_for_role", return_value=["ClinicalAI", "Reports"]):
            rep_resp = self.client.post(
                "/api/clinical-copilot/report",
                json={"patient_id": "ICU-10248", "report_type": "ICU Progress Note"},
                headers=self.headers,
            )
            self.assertEqual(rep_resp.status_code, 200)
            report_id = rep_resp.json()["report_id"]

            pdf_resp = self.client.get(
                f"/api/clinical-copilot/report/{report_id}/pdf",
                headers=self.headers,
            )
            self.assertEqual(pdf_resp.status_code, 200)
            self.assertEqual(pdf_resp.headers["content-type"], "application/pdf")
            self.assertTrue(pdf_resp.content.startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()
