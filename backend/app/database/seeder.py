import logging
from datetime import date, datetime
from app.database.session import SessionLocal
from app.models.patient import Patient
from app.models.admission import Admission
from app.models.vital_sign import VitalSign
from app.models.lab_result import LabResult

logger = logging.getLogger("app.database")

def seed_database_if_empty():
    """
    Seeds database with mock clinical records if the tables are empty.
    """
    db = SessionLocal()
    try:
        # Check if patient records already exist
        if db.query(Patient).count() > 0:
            logger.info("Database is already seeded with patient data.")
            return

        logger.info("🌱 Seeding database with initial patients, admissions, vitals, and labs...")

        # 1. Patients
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

        # 2. Admissions
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

        # 3. Vital signs
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

        # 4. Lab results
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
        logger.info("✅ Database seeded successfully!")
    except Exception as e:
        logger.error(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()
