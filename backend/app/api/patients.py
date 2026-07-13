"""
Patients API
"""

from fastapi import APIRouter, HTTPException
from app.services.clinical_ai_service import ClinicalAIEngine

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)

# ---------------------------------------------------------------------
# Temporary In-Memory Patient Data
# NOTE:
# This will be replaced by PostgreSQL in Sprint 7.
# ---------------------------------------------------------------------

PATIENTS = [
    {
        "id": "ICU-10248",
        "name": "Amelia Chen",
        "age": 67,
        "gender": "Female",
        "bed": "MICU-04",
        "status": "Critical",
        "risk_level": "HIGH",
        "risk_score": 0.93,
    },
    {
        "id": "ICU-10251",
        "name": "James Wilson",
        "age": 54,
        "gender": "Male",
        "bed": "MICU-07",
        "status": "Serious",
        "risk_level": "MEDIUM",
        "risk_score": 0.61,
    },
    {
        "id": "ICU-10263",
        "name": "Sophia Garcia",
        "age": 73,
        "gender": "Female",
        "bed": "MICU-11",
        "status": "Stable",
        "risk_level": "LOW",
        "risk_score": 0.18,
    },
]


@router.get("/")
def get_patients():
    """
    Return all ICU patients for the dashboard.
    """
    return PATIENTS


@router.get("/{patient_id}")
def get_patient(patient_id: str):
    """
    Enterprise Patient Clinical Workspace API.

    This endpoint returns the complete clinical profile
    required by the Patient Drawer.
    """

    patient = next(
        (p for p in PATIENTS if p["id"] == patient_id),
        None,
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found.",
        )

    res = {
        "patient": patient,

        "admission": {
            "diagnosis": "Septic Shock",
            "unit": "Medical ICU",
            "bed": patient["bed"],
            "admission_date": "2026-07-07 09:25",
            "icu_day": 4,
            "attending_physician": "Dr. Sarah Johnson",
            "code_status": "Full Code",
        },

        "vitals": {
            "heart_rate": 132,
            "spo2": 89,
            "temperature": 39.2,
            "respiratory_rate": 31,
            "blood_pressure": {
                "systolic": 82,
                "diastolic": 48,
            },
            "mean_arterial_pressure": 59,
        },

        "labs": {
            "WBC": "18.2 ×10⁹/L",
            "Lactate": "4.6 mmol/L",
            "Creatinine": "2.1 mg/dL",
            "Platelets": "118 ×10⁹/L",
            "Hemoglobin": "10.4 g/dL",
            "CRP": "148 mg/L",
            "Procalcitonin": "18.3 ng/mL",
        },

        "medications": [
            {
                "name": "Meropenem",
                "dose": "1 g",
                "route": "IV",
                "frequency": "Every 8 Hours",
            },
            {
                "name": "Norepinephrine",
                "dose": "0.15 mcg/kg/min",
                "route": "IV Infusion",
                "frequency": "Continuous",
            },
            {
                "name": "Paracetamol",
                "dose": "1 g",
                "route": "IV",
                "frequency": "Every 6 Hours",
            },
        ],

        "clinical_notes": [
            {
                "time": "08:15",
                "author": "Dr. Sarah Johnson",
                "note": "Patient remains hypotensive despite fluid resuscitation.",
            },
            {
                "time": "09:10",
                "author": "ICU Nurse",
                "note": "Urine output improving after vasopressor adjustment.",
            },
            {
                "time": "10:00",
                "author": "Critical Care Team",
                "note": "Continue sepsis bundle and repeat lactate.",
            },
        ],

        "alerts": [
            {
                "severity": "HIGH",
                "title": "Hypotension",
                "message": "Mean arterial pressure below target.",
            },
            {
                "severity": "MEDIUM",
                "title": "High Lactate",
                "message": "Repeat lactate recommended within 4 hours.",
            },
        ],

        "recommendations": [],

               "history": [
            {
                "time": "08:00",
                "heart_rate": 128,
                "spo2": 91,
                "temperature": 38.8,
                "respiratory_rate": 28,
                "map": 64,
            },
            {
                "time": "09:00",
                "heart_rate": 129,
                "spo2": 90,
                "temperature": 39.0,
                "respiratory_rate": 29,
                "map": 62,
            },
            {
                "time": "10:00",
                "heart_rate": 131,
                "spo2": 90,
                "temperature": 39.1,
                "respiratory_rate": 30,
                "map": 61,
            },
            {
                "time": "11:00",
                "heart_rate": 130,
                "spo2": 89,
                "temperature": 39.2,
                "respiratory_rate": 30,
                "map": 60,
            },
            {
                "time": "12:00",
                "heart_rate": 132,
                "spo2": 89,
                "temperature": 39.2,
                "respiratory_rate": 31,
                "map": 59,
            },
        ],
                       "ai": {
            "summary": {
                "overall_condition": "Critical but Hemodynamically Stable",
                "confidence": 0.96,
                "clinical_reasoning": (
                    "Persistent hypotension, elevated lactate, "
                    "tachycardia and inflammatory markers indicate "
                    "ongoing septic shock with a high probability "
                    "of clinical deterioration."
                ),
                "priority_actions": [
                    "Maintain MAP above 65 mmHg.",
                    "Repeat lactate in 4 hours.",
                    "Continue broad-spectrum antibiotics.",
                    "Monitor renal function and urine output.",
                ],
            },

            "explainability": {},

            "risk_progress": {},
        },   
                    "timeline": [
            {
                "time": "07:45",
                "type": "Admission",
                "description": "Patient admitted to Medical ICU.",
            },
            {
                "time": "08:10",
                "type": "Medication",
                "description": "Meropenem initiated.",
            },
            {
                "time": "08:40",
                "type": "Alert",
                "description": "Hypotension alert generated.",
            },
            {
                "time": "09:15",
                "type": "Laboratory",
                "description": "Lactate increased to 4.6 mmol/L.",
            },
            {
                "time": "10:00",
                "type": "AI",
                "description": "AI predicted high risk of septic shock progression.",
            },
        ],



    }
    ai = ClinicalAIEngine.generate(res)
    res["recommendations"] = ai["recommendations"]
    res["ai"]["summary"] = ai["summary"]
    res["ai"]["explainability"] = ai["explainability"]
    res["ai"]["risk_progress"] = ai["risk_progress"]
    return res
    