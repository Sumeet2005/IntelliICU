"""
Base LLM Provider Interface and shared clinical response normalization helpers.
"""

from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, List


CLINICAL_SYSTEM_PROMPT = (
    "You are an expert ICU Clinical Decision Support AI. Analyze the provided patient context "
    "and retrieved clinical evidence to answer the clinical question.\n"
    "Ground your response strictly in the provided patient context and retrieved evidence. "
    "Do NOT invent guideline citations or patient values that are not in the context.\n"
    "You MUST respond ONLY with a valid JSON object matching this exact schema:\n"
    "{\n"
    '  "reasoning": "Detailed clinical reasoning explaining findings",\n'
    '  "risk_drivers": ["List of positive/negative features contributing to risk"],\n'
    '  "abnormal_vitals": ["List of out-of-range vital signs"],\n'
    '  "abnormal_labs": ["List of out-of-range lab results"],\n'
    '  "recommendations": ["Recommended clinical stabilization guidelines"],\n'
    '  "evidence": ["Biomarkers or retrieved guideline evidence justifying findings"],\n'
    '  "confidence": 0.85\n'
    "}\n"
    "Do not include markdown wrappers like ```json in the response."
)


def extract_json_object(raw_text: str) -> Dict[str, Any]:
    """Parse a JSON object from raw LLM output, stripping optional markdown fences."""
    if not raw_text or not isinstance(raw_text, str):
        raise ValueError("Empty LLM response text.")

    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned).strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end > start:
            parsed = json.loads(cleaned[start : end + 1])
        else:
            raise

    if not isinstance(parsed, dict):
        raise ValueError("LLM response JSON is not an object.")
    return parsed


def _ensure_str_list(val: Any) -> List[str]:
    if isinstance(val, list):
        return [str(x) for x in val if x is not None]
    if isinstance(val, str) and val.strip():
        return [val.strip()]
    return []


def normalize_clinical_response(
    data: Dict[str, Any],
    *,
    provider: str,
    model: str,
    fallback_used: bool = False,
    simulated: bool = False,
) -> Dict[str, Any]:
    """Normalize provider JSON into the canonical IntelliICU clinical response contract."""
    reasoning = str(data.get("reasoning") or data.get("summary") or "").strip()
    risk_drivers = _ensure_str_list(data.get("risk_drivers"))
    abnormal_vitals = _ensure_str_list(data.get("abnormal_vitals"))
    abnormal_labs = _ensure_str_list(data.get("abnormal_labs"))
    recommendations = _ensure_str_list(data.get("recommendations"))
    evidence = _ensure_str_list(data.get("evidence"))

    try:
        confidence = float(data.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0
    confidence = max(0.0, min(1.0, confidence))

    findings = _ensure_str_list(data.get("findings"))
    if not findings:
        findings = risk_drivers + abnormal_vitals + abnormal_labs

    risk = str(data.get("risk") or (risk_drivers[0] if risk_drivers else "Unknown"))

    return {
        "reasoning": reasoning,
        "risk_drivers": risk_drivers,
        "abnormal_vitals": abnormal_vitals,
        "abnormal_labs": abnormal_labs,
        "recommendations": recommendations,
        "evidence": evidence,
        "confidence": confidence,
        "summary": reasoning,
        "findings": findings,
        "risk": risk,
        "provider_metadata": {
            "provider": provider,
            "model": model,
            "fallback_used": fallback_used,
            "simulated": simulated,
        },
    }


def sanitize_error_message(exc: Exception) -> str:
    """Return a short, secret-free error message safe for logs and API responses."""
    msg = str(exc) or exc.__class__.__name__
    msg = re.sub(r"(gsk_|sk-|AIza)[A-Za-z0-9_\-]{8,}", "[REDACTED_KEY]", msg)
    msg = re.sub(r"Bearer\s+[A-Za-z0-9\-._~+/]+=*", "Bearer [REDACTED]", msg, flags=re.IGNORECASE)
    return msg[:300]


class BaseLLMProvider(ABC):
    """
    Abstract Base Class for clinical LLM providers.
    """

    provider_name: str = "base"

    @abstractmethod
    def generate(self, question: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes query analysis and returns explainable clinical parameters.
        """
        pass

    def generate_response(self, question: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Backward-compatible alias used by ClinicalCopilotService and HospitalAssistantService.
        """
        return self.generate(question, context)

    @abstractmethod
    def generate_stream(self, question: str, context: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        """
        Generates streaming output chunks during clinical reasoning.
        """
        pass
