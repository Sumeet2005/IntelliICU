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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup / shutdown.
    """

    print("=" * 60)
    print("🚀 IntelliICU Starting...")
    print("=" * 60)

    # Start ICU Simulator
    asyncio.create_task(simulator.start())

    yield

    print("=" * 60)
    print("🛑 IntelliICU Shutdown")
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

@app.get("/")
async def root():
    return {
        "application": "IntelliICU",
        "status": "running",
        "version": "2.0.0",
    }