"""
WebSocket Routes
"""

import asyncio
import logging
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from app.core.dependencies.auth import get_current_user_from_token
from app.repositories.rbac_repository import RBACRepository
from app.websocket.manager import manager

logger = logging.getLogger(__name__)
router = APIRouter()


async def _authenticate_ws(websocket: WebSocket, required_permission: str) -> bool:
    token = websocket.query_params.get("token")
    if not token:
        auth_header = websocket.headers.get("authorization", "")
        if auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()
    try:
        user = await get_current_user_from_token(token)
    except HTTPException:
        await websocket.close(code=4401, reason="Unauthorized")
        return False

    perms = RBACRepository.get_permissions_for_role(user.role)
    if required_permission not in perms:
        await websocket.close(code=4403, reason="Forbidden")
        return False
    return True


@router.websocket("/ws/dashboard")
async def dashboard_websocket(websocket: WebSocket):
    """
    Live Dashboard WebSocket

    Accepts authenticated connections and keeps them alive.
    The simulator broadcasts to all connected clients every 2 seconds.
    """
    if not await _authenticate_ws(websocket, "Dashboard"):
        return

    await manager.connect(websocket)

    try:
        while True:
            # Use a short receive with timeout so we can detect stale
            # connections promptly without blocking the event loop.
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=30)
            except asyncio.TimeoutError:
                # No message from client in 30s — that's fine, keep alive.
                continue

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except Exception:
        # Catch any other transport error (TLS teardown, RST, etc.)
        manager.disconnect(websocket)