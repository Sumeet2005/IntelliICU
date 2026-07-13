"""
Patient WebSocket Routes

Provides real-time streaming for an individual patient.

Endpoint:
    ws://localhost:8000/ws/patient/{patient_id}
"""

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.websocket.manager import manager

router = APIRouter()


@router.websocket("/ws/patient/{patient_id}")
async def patient_websocket(
    websocket: WebSocket,
    patient_id: str,
):
    """
    Individual Patient Live Stream

    Each connected client receives live updates
    only for the requested patient.
    """

    await manager.connect_patient(
        patient_id,
        websocket,
    )

    try:

        while True:

            # Keep WebSocket alive.
            #
            # Later we can support commands such as:
            # subscribe
            # unsubscribe
            # pause
            # resume
            # heartbeat

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect_patient(
            patient_id,
            websocket,
        )

    except Exception as exc:

        print(
            f"❌ Patient WebSocket Error ({patient_id}): {exc}"
        )

        manager.disconnect_patient(
            patient_id,
            websocket,
        )