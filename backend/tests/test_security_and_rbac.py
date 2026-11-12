"""
Security, Authentication, RBAC, and WebSocket Authorization Tests.
Compatible with both pytest and python -m unittest.
"""

import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

# Prevent simulator background loop or demo DB wiping during test import
os.environ.setdefault("DISABLE_SIMULATOR", "true")
os.environ.setdefault("ENABLE_DEMO_SEED", "false")

from app.main import app  # noqa: E402
from app.models.user import User  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402


class TestSecurityAndRBAC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.state.startup_complete = True
        cls.client = TestClient(app)

    def _make_token(self, username: str, role: str) -> str:
        return AuthService.create_access_token({"sub": username, "role": role})

    def test_unauthenticated_v1_endpoints_rejected(self):
        for path in [
            "/api/v1/patients",
            "/api/v1/admissions",
            "/api/v1/vital-signs",
            "/api/v1/lab-results",
        ]:
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 401, f"{path} must reject unauthenticated GET")

        resp = self.client.post("/api/v1/predictions/generate/adm-10248")
        self.assertEqual(resp.status_code, 401)

    def test_unauthenticated_ai_timeline_telemetry_rejected(self):
        self.assertEqual(self.client.get("/api/ai/config").status_code, 401)
        self.assertEqual(self.client.put("/api/ai/config", json={"provider": "mock"}).status_code, 401)
        self.assertEqual(self.client.get("/api/timeline/ICU-10248").status_code, 401)
        self.assertEqual(self.client.get("/api/telemetry/trends").status_code, 401)

    def test_unauthenticated_websocket_rejected(self):
        with self.assertRaises(Exception):
            with self.client.websocket_connect("/ws/dashboard"):
                pass
        with self.assertRaises(Exception):
            with self.client.websocket_connect("/ws/patient/ICU-10248"):
                pass

    def test_inactive_user_rejected(self):
        inactive_user = User(
            id="usr-inactive",
            username="inactive_doc",
            email="inactive@intelliicu.org",
            hashed_password=AuthService.get_password_hash("secret123"),
            role="Doctor",
            department="Medical ICU",
            is_active=False,
        )
        token = self._make_token("inactive_doc", "Doctor")
        with patch("app.core.dependencies.auth.UserRepository.get_by_username", return_value=inactive_user):
            resp = self.client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
            self.assertEqual(resp.status_code, 401)

        with patch("app.services.auth_service.UserRepository.get_by_username", return_value=inactive_user):
            self.assertIsNone(AuthService.authenticate_user("inactive_doc", "secret123"))

    def test_viewer_forbidden_on_clinical_ai_and_settings(self):
        viewer = User(
            id="usr-viewer",
            username="viewer1",
            email="viewer1@intelliicu.org",
            hashed_password="x",
            role="Viewer",
            department="General",
            is_active=True,
        )
        token = self._make_token("viewer1", "Viewer")
        headers = {"Authorization": f"Bearer {token}"}

        with patch("app.core.dependencies.auth.UserRepository.get_by_username", return_value=viewer), \
             patch("app.core.dependencies.rbac.RBACRepository.get_permissions_for_role", return_value=["Dashboard", "Patients"]):
            self.assertEqual(self.client.put("/api/ai/config", json={"provider": "mock"}, headers=headers).status_code, 403)
            self.assertEqual(self.client.post("/api/alerts/resolve/AL-1", headers=headers).status_code, 403)
            self.assertEqual(self.client.delete("/api/rag/documents/test.pdf", headers=headers).status_code, 403)


if __name__ == "__main__":
    unittest.main()
