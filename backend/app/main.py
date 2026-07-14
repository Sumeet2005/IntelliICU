"""
IntelliICU Main Application
"""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# =====================================================
# REST API Routers
# =====================================================

from app.api.dashboard import router as dashboard_router
from app.api.patients import router as patients_router
from app.api.clinical_ai import router as clinical_ai_router
from app.api.alerts import router as alerts_router
from app.api import patient_profile
from app.api.timeline_routes import router as timeline_router
from app.api.auth import router as auth_router
from app.api.rbac import router as rbac_router
from app.api.user_management import router as user_management_router, dept_router as department_router
from app.api.clinical_copilot import router as clinical_copilot_router
from app.telemetry.routes import router as telemetry_router
from app.api.hospital_assistant import router as hospital_assistant_router
from app.api.rag import router as rag_router
from app.api.ai import router as ai_router

# =====================================================
# WebSocket Routers
# =====================================================

from app.websocket.routes import router as dashboard_websocket_router
from app.websocket.patient_routes import router as patient_websocket_router

# =====================================================
# Simulator
# =====================================================

from app.websocket.simulator import simulator


# =====================================================
# Application Lifespan
# =====================================================

from app.database.session import check_db_connectivity
from app.database.seeder import seed_database_if_empty

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup / shutdown.
    """

    print("=" * 60)
    print("STARTING: IntelliICU Starting...")
    print("=" * 60)

    # Validate database connection at boot
    if check_db_connectivity():
        seed_database_if_empty()

    # Start ICU Simulator
    asyncio.create_task(simulator.start())

    yield

    print("=" * 60)
    print("SHUTDOWN: IntelliICU Shutdown")
    print("=" * 60)


# =====================================================
# FastAPI Application
# =====================================================

app = FastAPI(
    title="IntelliICU API",
    version="2.0.0",
    lifespan=lifespan,
)

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# REST APIs
# =====================================================

app.include_router(
    dashboard_router,
    prefix="/api",
)

app.include_router(
    patients_router,
    prefix="/api",
)

app.include_router(
    clinical_ai_router,
    prefix="/api",
)

app.include_router(
    alerts_router,
    prefix="/api",
)

app.include_router(
    patient_profile.router,
    prefix="/api",
)

app.include_router(
    timeline_router,
    prefix="/api",
)

app.include_router(
    auth_router,
    prefix="/api",
)

app.include_router(
    rbac_router,
    prefix="/api",
)

app.include_router(
    user_management_router,
    prefix="/api",
)

app.include_router(
    department_router,
    prefix="/api",
)

app.include_router(
    clinical_copilot_router,
    prefix="/api",
)

app.include_router(
    telemetry_router,
    prefix="/api",
)

app.include_router(
    hospital_assistant_router,
    prefix="/api",
)

app.include_router(
    rag_router,
    prefix="/api",
)

app.include_router(
    ai_router,
    prefix="/api",
)

# =====================================================
# WebSocket APIs
# =====================================================

# Dashboard Live Stream
app.include_router(
    dashboard_websocket_router,
)

# Patient Live Stream
app.include_router(
    patient_websocket_router,
)

# =====================================================
# Root Endpoint
# =====================================================

from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("app.main")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Unhandled global exception: {str(exc)} | Path: {request.url.path}",
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please contact administrator."}
    )

@app.get("/health")
@app.get("/ready")
@app.get("/live")
async def health_check():
    db_ok = check_db_connectivity()
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "disconnected",
        "services": "online",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/")
async def root():
    return {
        "application": "IntelliICU",
        "status": "running",
        "version": "2.0.0",
    }