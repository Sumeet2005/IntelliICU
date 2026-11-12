"""
Feature Builder for IntelliICU Production Model
"""

import math
from app.models.lab_result import LabResult
from app.models.vital_sign import VitalSign


FEATURE_ORDER = [
    "heart_rate",
    "systolic_bp",
    "diastolic_bp",
    "respiratory_rate",
    "spo2",
    "temperature",
    "wbc",
    "platelets",
    "creatinine",
    "bun",
    "potassium",
    "chloride",
    "lactate",
]


class FeatureBuilder:
    """
    Builds and validates the canonical 13-feature vector used by
    the production ML model.
    """

    @staticmethod
    def validate_features(raw: dict) -> dict[str, float]:
        validated: dict[str, float] = {}
        missing = [k for k in FEATURE_ORDER if raw.get(k) is None]
        if missing:
            raise ValueError(f"Missing required clinical features: {missing}")

        for key in FEATURE_ORDER:
            try:
                val = float(raw[key])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid numeric value for feature '{key}': {raw[key]}") from exc
            if math.isnan(val) or math.isinf(val):
                raise ValueError(f"Non-finite value for feature '{key}': {val}")
            validated[key] = val
        return validated

    @staticmethod
    def build(
        vital: VitalSign,
        lab: LabResult,
    ) -> dict[str, float]:
        raw = {
            "heart_rate": vital.heart_rate,
            "systolic_bp": vital.systolic_bp,
            "diastolic_bp": vital.diastolic_bp,
            "respiratory_rate": vital.respiratory_rate,
            "spo2": vital.spo2,
            "temperature": vital.temperature,
            "wbc": lab.wbc,
            "platelets": lab.platelets,
            "creatinine": lab.creatinine,
            "bun": lab.bun,
            "potassium": lab.potassium,
            "chloride": lab.chloride,
            "lactate": lab.lactate,
        }
        return FeatureBuilder.validate_features(raw)