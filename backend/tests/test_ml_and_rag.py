"""
AI/ML Feature Validation, Predictor, Explainability, and RAG Pipeline Tests.
Compatible with both pytest and python -m unittest.
"""

import math
import unittest

from app.ai.feature_builder import FEATURE_ORDER, FeatureBuilder
from app.services.explainability_service import ExplainabilityEngine
from app.services.hospital_assistant_service import HospitalAssistantService


class TestMLAndRAG(unittest.TestCase):
    def test_feature_order_and_validation(self):
        self.assertEqual(len(FEATURE_ORDER), 13)
        valid = {k: 1.0 for k in FEATURE_ORDER}
        out = FeatureBuilder.validate_features(valid)
        self.assertEqual(list(out.keys()), FEATURE_ORDER)

        # Missing feature must raise ValueError
        incomplete = dict(valid)
        del incomplete["lactate"]
        with self.assertRaises(ValueError):
            FeatureBuilder.validate_features(incomplete)

        # NaN must raise ValueError
        bad_nan = dict(valid)
        bad_nan["heart_rate"] = float("nan")
        with self.assertRaises(ValueError):
            FeatureBuilder.validate_features(bad_nan)

    def test_explainability_is_honestly_labelled_as_clinical_rules(self):
        res = ExplainabilityEngine.generate({
            "vitals": {"heart_rate": 135, "spo2": 88, "temperature": 39.4, "respiratory_rate": 32},
            "labs": {"lactate": 4.8},
            "risk_score": 0.91,
        })
        self.assertEqual(res.get("explainability_method"), "clinical_rules")
        self.assertIn("not SHAP", res.get("disclaimer", ""))
        self.assertGreater(len(res["positive_contributors"]), 0)

    def test_hospital_assistant_uses_provider_factory_not_hardcoded_mock(self):
        svc = HospitalAssistantService()
        # Verify llm is resolved dynamically as a property rather than hardcoded attribute
        self.assertIsInstance(HospitalAssistantService.llm, property)
        self.assertIsNotNone(svc.llm)


if __name__ == "__main__":
    unittest.main()
