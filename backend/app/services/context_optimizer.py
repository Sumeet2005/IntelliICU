"""
Context Optimizer Service.
Reduces full Patient Clinical Context to a concise summary for local LLM inference.
"""

from typing import Dict, Any

class ContextOptimizer:
    """
    Optimizes comprehensive clinical contexts for LLM consumption by truncating history
    and keeping only essential parameters, ensuring timestamps and reconciliation
    between real-time telemetry and historical active alerts.
    """

    @staticmethod
    def optimize(context: Dict[str, Any]) -> Dict[str, Any]:
        patient = context.get("patient", {})
        admission = context.get("admission", {})
        vitals = context.get("vitals", {})
        vital_trends = context.get("vital_trends", {})
        pred = context.get("prediction") or {}
        
        # Format vital trends simply
        trends_summary = {}
        if isinstance(vital_trends, dict):
            for metric, data in vital_trends.items():
                if isinstance(data, dict) and "direction" in data:
                    trends_summary[metric] = f"{data['direction']} (current: {data.get('last_value', '-')}, previous: {data.get('previous_value', '-')})"

        # Keep abnormal labs condensed
        abnormal_labs = []
        for lab in context.get("abnormal_labs", []):
            if isinstance(lab, dict):
                abnormal_labs.append(f"{lab.get('metric')}: {lab.get('value')} ({lab.get('status')}, {lab.get('severity')})")

        # Keep active alerts condensed with timestamps so LLM reconciles past alarms with current vitals
        active_alerts = []
        for alert in context.get("alerts", []):
            if isinstance(alert, dict) and alert.get("status") in ["ACTIVE", "UNRESOLVED", None]:
                ts = alert.get("created_at") or "unspecified"
                active_alerts.append(
                    f"[{alert.get('severity', 'WARNING')}] {alert.get('title')}: {alert.get('message')} (Triggered at: {ts})"
                )

        # Reconcile risk score and level
        risk_score_raw = pred.get("risk_score")
        risk_level = pred.get("risk_level") or context.get("risk_level") or "LOW"
        if risk_score_raw is not None:
            try:
                score_val = float(risk_score_raw)
                pct = round(score_val * 100 if score_val <= 1.0 else score_val)
                risk_display = f"{pct}% ({risk_level})"
            except (ValueError, TypeError):
                risk_display = f"{risk_score_raw} ({risk_level})"
        else:
            risk_display = f"Unscored ({risk_level})"

        optimized = {
            "patient": {
                "id": patient.get("id"),
                "name": patient.get("name"),
                "age": patient.get("age"),
                "gender": patient.get("gender")
            },
            "admission": {
                "diagnosis": admission.get("diagnosis"),
                "ward": admission.get("ward"),
                "bed_number": admission.get("bed_number")
            },
            "current_vitals_telemetry": {
                "recorded_at": vitals.get("recorded_at", "Current"),
                "heart_rate": vitals.get("heart_rate"),
                "spo2": vitals.get("spo2"),
                "temperature": vitals.get("temperature"),
                "systolic_bp": vitals.get("systolic_bp") or (vitals.get("blood_pressure", {}).get("systolic") if isinstance(vitals.get("blood_pressure"), dict) else None),
                "diastolic_bp": vitals.get("diastolic_bp") or (vitals.get("blood_pressure", {}).get("diastolic") if isinstance(vitals.get("blood_pressure"), dict) else None),
                "respiratory_rate": vitals.get("respiratory_rate")
            },
            "vital_trends_summary": trends_summary,
            "latest_abnormal_labs": abnormal_labs,
            "active_medications": context.get("medications", []),
            "unresolved_alerts_history": active_alerts,
            "clinical_reconciliation_note": (
                "Current vitals reflect the instantaneous telemetry state at recorded_at. "
                "Unresolved alerts reflect historical trigger events that have not yet been cleared by staff. "
                "Assess risk using current vitals alongside persistent alert context."
            ),
            "ai_sepsis_risk": risk_display,
            "clinical_priority": context.get("clinical_priority", "MEDIUM")
        }
        return optimized
