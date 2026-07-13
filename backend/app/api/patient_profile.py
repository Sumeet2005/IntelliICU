from fastapi import APIRouter, HTTPException

from app.websocket.simulator import simulator

router = APIRouter(
    prefix="/patient",
    tags=["Patient Profile"],
)


@router.get("/{patient_id}")
async def get_patient(patient_id: str):
    """
    Get complete patient profile.
    """

    patient = next(
        (
            p
            for p in simulator.patients
            if p["id"] == patient_id
        ),
        None,
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return {
        "patient": patient,

        "labs": {
            "WBC": 16.4,
            "Lactate": patient["lactate"],
            "Creatinine": 1.7,
            "Platelets": 132,
            "CRP": 118,
            "Procalcitonin": 5.8,
        },

        "medications": [
            "Meropenem",
            "Norepinephrine",
            "Paracetamol",
            "Normal Saline",
        ],

        "clinical_notes": [
            "Patient admitted with septic shock.",
            "Broad-spectrum antibiotics started.",
            "Hypotension persists despite fluids.",
        ],

        "recommendations": [
            "Repeat lactate in 2 hours.",
            "Continue broad-spectrum antibiotics.",
            "Maintain MAP > 65 mmHg.",
            "Monitor urine output hourly.",
        ],
    }