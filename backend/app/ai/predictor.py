"""
ML Predictor for IntelliICU
"""

from app.ai.feature_builder import FEATURE_ORDER, FeatureBuilder
from app.ai.model_loader import MODEL
from app.models.lab_result import LabResult
from app.models.vital_sign import VitalSign


class Predictor:

    THRESHOLD = 0.20

    @staticmethod
    def predict_from_dict(raw_features: dict) -> dict:
        import pandas as pd

        features = FeatureBuilder.validate_features(raw_features)
        X = pd.DataFrame([features], columns=FEATURE_ORDER)

        probability = float(
            MODEL.predict_proba(X)[0][1]
        )

        if probability >= Predictor.THRESHOLD:
            risk_level = "HIGH"
            recommendation = (
                "Immediate ICU physician review. "
                "Consider sepsis protocol."
            )
        else:
            risk_level = "LOW"
            recommendation = (
                "Continue routine ICU monitoring."
            )

        return {
            "risk_score": round(probability * 100, 2),
            "probability": round(probability, 4),
            "risk_level": risk_level,
            "recommendation": recommendation,
            "model_version": "v2.0-rf",
            "features_used": FEATURE_ORDER,
        }

    @staticmethod
    def predict(
        vital: VitalSign,
        lab: LabResult,
    ) -> dict:
        features = FeatureBuilder.build(vital, lab)
        return Predictor.predict_from_dict(features)