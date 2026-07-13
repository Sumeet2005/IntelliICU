import logging
from datetime import date, datetime
from app.database.session import SessionLocal
from app.models.patient import Patient
from app.models.admission import Admission
from app.models.vital_sign import VitalSign
from app.models.lab_result import LabResult
from app.database.models import DBUser, DBRole, DBDepartment, DBPermission
from app.repositories.rbac_repository import MOCK_ROLES, MOCK_PERMISSIONS
from app.repositories.user_repository import MOCK_USERS

logger = logging.getLogger("app.database")

def seed_database_if_empty():
    """
    Seeds database with mock clinical records and users/roles/permissions if the tables are empty.
    """
    db = SessionLocal()
    try:
        # 1. Seed clinical data if empty
        if db.query(Patient).count() == 0:
            logger.info("🌱 Seeding database with initial patients, admissions, vitals, and labs...")

            p1 = Patient(
                id="ICU-10248",
                hospital_patient_id="ICU-10248",
                first_name="Amelia",
                last_name="Chen",
                date_of_birth=date(1959, 1, 1),
                gender="Female",
                status="Critical",
            )
            p2 = Patient(
                id="ICU-10251",
                hospital_patient_id="ICU-10251",
                first_name="James",
                last_name="Wilson",
                date_of_birth=date(1972, 1, 1),
                gender="Male",
                status="Serious",
            )
            p3 = Patient(
                id="ICU-10263",
                hospital_patient_id="ICU-10263",
                first_name="Sophia",
                last_name="Garcia",
                date_of_birth=date(1953, 1, 1),
                gender="Female",
                status="Stable",
            )
            db.add_all([p1, p2, p3])
            db.commit()

            a1 = Admission(
                id="adm-10248",
                patient_id="ICU-10248",
                admission_number="ADM-10248",
                diagnosis="Septic Shock",
                doctor_name="Dr. Sarah Johnson",
                ward="Medical ICU",
                bed_number="MICU-04",
            )
            a2 = Admission(
                id="adm-10251",
                patient_id="ICU-10251",
                admission_number="ADM-10251",
                diagnosis="Sepsis",
                doctor_name="Dr. Sarah Johnson",
                ward="Medical ICU",
                bed_number="MICU-07",
            )
            a3 = Admission(
                id="adm-10263",
                patient_id="ICU-10263",
                admission_number="ADM-10263",
                diagnosis="Recovery",
                doctor_name="Dr. Sarah Johnson",
                ward="Medical ICU",
                bed_number="MICU-11",
            )
            db.add_all([a1, a2, a3])
            db.commit()

            v1 = VitalSign(
                id="vit-10248",
                admission_id="adm-10248",
                heart_rate=132.0,
                systolic_bp=82.0,
                diastolic_bp=48.0,
                respiratory_rate=31.0,
                spo2=89.0,
                temperature=39.2,
                glasgow_coma_scale=15,
                urine_output_ml=50.0,
            )
            v2 = VitalSign(
                id="vit-10251",
                admission_id="adm-10251",
                heart_rate=108.0,
                systolic_bp=104.0,
                diastolic_bp=66.0,
                respiratory_rate=24.0,
                spo2=95.0,
                temperature=38.2,
                glasgow_coma_scale=15,
                urine_output_ml=60.0,
            )
            v3 = VitalSign(
                id="vit-10263",
                admission_id="adm-10263",
                heart_rate=76.0,
                systolic_bp=122.0,
                diastolic_bp=78.0,
                respiratory_rate=17.0,
                spo2=98.0,
                temperature=36.8,
                glasgow_coma_scale=15,
                urine_output_ml=75.0,
            )
            db.add_all([v1, v2, v3])

            l1 = LabResult(
                id="lab-10248",
                admission_id="adm-10248",
                hemoglobin=10.4,
                wbc=18.2,
                platelets=118.0,
                creatinine=2.1,
                bun=25.0,
                sodium=138.0,
                potassium=4.2,
                chloride=102.0,
                lactate=4.6,
                ph=7.32,
                pao2=80.0,
                paco2=38.0,
            )
            l2 = LabResult(
                id="lab-10251",
                admission_id="adm-10251",
                hemoglobin=11.2,
                wbc=14.5,
                platelets=125.0,
                creatinine=1.7,
                bun=20.0,
                sodium=140.0,
                potassium=4.0,
                chloride=104.0,
                lactate=2.7,
                ph=7.38,
                pao2=85.0,
                paco2=40.0,
            )
            l3 = LabResult(
                id="lab-10263",
                admission_id="adm-10263",
                hemoglobin=12.1,
                wbc=8.4,
                platelets=180.0,
                creatinine=1.0,
                bun=15.0,
                sodium=142.0,
                potassium=3.8,
                chloride=105.0,
                lactate=1.2,
                ph=7.42,
                pao2=95.0,
                paco2=42.0,
            )
            db.add_all([l1, l2, l3])
            db.commit()

        # 2. Seed default permissions if empty
        if db.query(DBPermission).count() == 0:
            logger.info("🌱 Seeding permissions...")
            perms = []
            for name, mock_perm in MOCK_PERMISSIONS.items():
                perms.append(DBPermission(
                    id=mock_perm.id,
                    name=mock_perm.name,
                    description=mock_perm.description
                ))
            db.add_all(perms)
            db.commit()

        # 3. Seed default roles if empty
        if db.query(DBRole).count() == 0:
            logger.info("🌱 Seeding roles and matching permissions...")
            roles = []
            for name, mock_role in MOCK_ROLES.items():
                role_db = DBRole(
                    id=mock_role.id,
                    name=mock_role.name
                )
                # Map permissions
                db_perms = db.query(DBPermission).filter(DBPermission.name.in_(mock_role.permissions)).all()
                role_db.permissions = db_perms
                roles.append(role_db)
            db.add_all(roles)
            db.commit()

        # 4. Seed default departments if empty
        if db.query(DBDepartment).count() == 0:
            logger.info("🌱 Seeding departments...")
            d1 = DBDepartment(id="dept-1", name="Administration", description="Hospital admin department")
            d2 = DBDepartment(id="dept-2", name="Medical ICU", description="Intensive Care Unit")
            db.add_all([d1, d2])
            db.commit()

        # 5. Seed default users if empty
        if db.query(DBUser).count() == 0:
            logger.info("🌱 Seeding admin and default clinical users...")
            users = []
            for username, mock_user in MOCK_USERS.items():
                users.append(DBUser(
                    id=mock_user["id"],
                    username=mock_user["username"],
                    email=mock_user["email"],
                    hashed_password=mock_user["hashed_password"],
                    role=mock_user["role"],
                    department=mock_user.get("department"),
                    is_active=mock_user["is_active"]
                ))
            db.add_all(users)
            db.commit()

        logger.info("✅ Seeder run complete!")
    except Exception as e:
        logger.error(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()
