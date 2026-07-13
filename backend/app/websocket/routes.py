"""
WebSocket Routes
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.manager import manager

router = APIRouter()


@router.websocket("/ws/dashboard")
async def dashboard_websocket(websocket: WebSocket):
    """
    Live Dashboard WebSocket
    """

    await manager.connect(websocket)

    try:

        while True:
            # Keep the connection alive
            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(websocket)