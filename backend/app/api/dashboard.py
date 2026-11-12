"""
Dashboard API
"""

from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.dependencies.rbac import require_permission

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/")
def get_dashboard(current_user: User = Depends(require_permission("Dashboard"))):

    return {
        "total_patients": 48,
        "critical_patients": 12,
        "bed_occupancy": 85.7,
        "active_alerts": 7,
        "available_beds": 8,
        "icu_capacity": 56,
    }