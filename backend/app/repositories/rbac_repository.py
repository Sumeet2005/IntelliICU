from app.models.role import Role, Permission

MOCK_PERMISSIONS = {
    "dashboard": Permission(id="perm-1", name="Dashboard", description="View dashboard stats and status"),
    "patients": Permission(id="perm-2", name="Patients", description="View patient list and profile telemetry"),
    "clinicalai": Permission(id="perm-3", name="ClinicalAI", description="Run sepsis AI risk analyses"),
    "alerts": Permission(id="perm-4", name="Alerts", description="Acknowledge, resolve, and manage alerts"),
    "timeline": Permission(id="perm-5", name="Timeline", description="Audit patient clinical events timeline log"),
    "reports": Permission(id="perm-6", name="Reports", description="Export patient timeline reports as PDF/CSV/JSON"),
    "analytics": Permission(id="perm-7", name="Analytics", description="View alerts response times and system analytics"),
    "usermanagement": Permission(id="perm-8", name="UserManagement", description="Manage administrative users"),
    "settings": Permission(id="perm-9", name="Settings", description="Modify clinical limits and configuration thresholds"),
}

MOCK_ROLES = {
    "superadmin": Role(
        id="role-1",
        name="SuperAdmin",
        permissions=[p.name for p in MOCK_PERMISSIONS.values()]
    ),
    "hospitaladmin": Role(
        id="role-2",
        name="HospitalAdmin",
        permissions=["Dashboard", "Patients", "Reports", "Analytics", "UserManagement", "Settings"]
    ),
    "icumanager": Role(
        id="role-3",
        name="ICUManager",
        permissions=["Dashboard", "Patients", "ClinicalAI", "Alerts", "Timeline", "Reports", "Analytics", "Settings"]
    ),
    "doctor": Role(
        id="role-4",
        name="Doctor",
        permissions=["Dashboard", "Patients", "ClinicalAI", "Alerts", "Timeline", "Reports", "Analytics"]
    ),
    "nurse": Role(
        id="role-5",
        name="Nurse",
        permissions=["Dashboard", "Patients", "Alerts", "Timeline", "Reports"]
    ),
    "labtechnician": Role(
        id="role-6",
        name="LabTechnician",
        permissions=["Dashboard", "Patients", "Reports"]
    ),
    "receptionist": Role(
        id="role-7",
        name="Receptionist",
        permissions=["Dashboard", "Patients"]
    ),
    "viewer": Role(
        id="role-8",
        name="Viewer",
        permissions=["Dashboard", "Patients"]
    )
}

class RBACRepository:
    @staticmethod
    def get_role_by_name(name: str) -> Role | None:
        return MOCK_ROLES.get(name.lower())

    @staticmethod
    def get_all_roles() -> list[Role]:
        return list(MOCK_ROLES.values())

    @staticmethod
    def get_all_permissions() -> list[Permission]:
        return list(MOCK_PERMISSIONS.values())

    @classmethod
    def get_permissions_for_role(cls, role_name: str) -> list[str]:
        role = cls.get_role_by_name(role_name)
        if not role:
            return []
        return role.permissions
