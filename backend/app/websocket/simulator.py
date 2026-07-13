"""
Live ICU Data Simulator
"""

import asyncio
import random
from datetime import datetime

from app.websocket.manager import manager
from app.alerts.manager import manager as alert_manager
from app.alerts.models import AlertSeverity


class ICUSimulator:
    """
    Enterprise ICU Simulator
    Simulates dashboard metrics and patient status updates.
    """

    def __init__(self):

        self.dashboard = {
            "total_patients": 48,
            "critical_patients": 12,
            "bed_occupancy": 85.7,
            "active_alerts": 7,
            "available_beds": 8,
            "icu_capacity": 56,
        }

        self.patients = [
            {
                "id": "ICU-10248",
                "name": "Amelia Chen",
                "age": 67,
                "gender": "Female",
                "bed": "MICU-04",
                "status": "Critical",
                "risk_level": "HIGH",
                "risk_score": 0.93,
                "heart_rate": 132,
                "spo2": 89,
                "temperature": 39.2,
                "respiratory_rate": 31,
                "systolic_bp": 82,
                "diastolic_bp": 48,
                "lactate": 4.6,
            },
            {
                "id": "ICU-10251",
                "name": "James Wilson",
                "age": 54,
                "gender": "Male",
                "bed": "MICU-07",
                "status": "Serious",
                "risk_level": "MEDIUM",
                "risk_score": 0.61,
                "heart_rate": 108,
                "spo2": 95,
                "temperature": 38.2,
                "respiratory_rate": 24,
                "systolic_bp": 104,
                "diastolic_bp": 66,
                "lactate": 2.7,
            },
            {
                "id": "ICU-10263",
                "name": "Sophia Garcia",
                "age": 73,
                "gender": "Female",
                "bed": "MICU-11",
                "status": "Stable",
                "risk_level": "LOW",
                "risk_score": 0.18,
                "heart_rate": 76,
                "spo2": 98,
                "temperature": 36.8,
                "respiratory_rate": 17,
                "systolic_bp": 122,
                "diastolic_bp": 78,
                "lactate": 1.2,
            },
        ]

        self.alerts = []

    async def start(self):

        print("=" * 60)
        print("🚑 ICU Live Simulator Started")
        print("=" * 60)

        while True:

            self._update_dashboard()
            self._update_patients()
            self._generate_alerts()

            timestamp = datetime.now().strftime("%H:%M:%S")

            await manager.broadcast_dashboard(
                {
                    "type": "dashboard_update",
                    "timestamp": timestamp,
                    "data": self.dashboard,
                }
            )

            await manager.broadcast(
                {
                    "type": "patients_update",
                    "timestamp": timestamp,
                    "data": self.patients,
                }
            )
            
            await manager.broadcast_alerts(
                {
                    "type": "alerts_update",
                    "timestamp": timestamp,
                     "data": [
                         alert.model_dump(mode="json")
                         for alert in alert_manager.active_alerts()
                     ],
                }
            )
            
            for patient in self.patients:
                await manager.broadcast_patient(
                    patient["id"],
                    {
                        "type": "patient_update",
                        "timestamp": timestamp,
                        "data": patient
                    }
                )

            await asyncio.sleep(2)

    def _update_dashboard(self):

        self.dashboard["total_patients"] = max(
            40,
            min(
                56,
                self.dashboard["total_patients"] + random.randint(-1, 1),
            ),
        )

        self.dashboard["critical_patients"] = max(
            5,
            min(
                20,
                self.dashboard["critical_patients"] + random.randint(-1, 1),
            ),
        )

        self.dashboard["active_alerts"] = max(
            0,
            min(
                15,
                self.dashboard["active_alerts"] + random.randint(-1, 1),
            ),
        )

        self.dashboard["available_beds"] = (
            self.dashboard["icu_capacity"]
            - self.dashboard["total_patients"]
        )

        self.dashboard["bed_occupancy"] = round(
            (
                self.dashboard["total_patients"]
                / self.dashboard["icu_capacity"]
            )
            * 100,
            1,
        )

    def _update_patients(self):

        for patient in self.patients:

            # Update risk score
            delta = random.uniform(-0.03, 0.03)

            patient["risk_score"] = round(
                max(
                    0.05,
                    min(
                        0.99,
                        patient["risk_score"] + delta,
                    ),
                ),
                2,
            )

            # Update risk level
            if patient["risk_score"] >= 0.80:
                patient["risk_level"] = "HIGH"
                patient["status"] = "Critical"

            elif patient["risk_score"] >= 0.50:
                patient["risk_level"] = "MEDIUM"
                patient["status"] = "Serious"

            else:
                patient["risk_level"] = "LOW"
                patient["status"] = "Stable"

            # Live Vital Signs
            patient["heart_rate"] = max(
                45,
                min(
                    180,
                    patient["heart_rate"] + random.randint(-3, 3),
                ),
            )

            patient["spo2"] = max(
                80,
                min(
                    100,
                    patient["spo2"] + random.randint(-1, 1),
                ),
            )

            patient["temperature"] = round(
                max(
                    35.5,
                    min(
                        41.0,
                        patient["temperature"] + random.uniform(-0.2, 0.2),
                    ),
                ),
                1,
            )

            patient["respiratory_rate"] = max(
                10,
                min(
                    40,
                    patient["respiratory_rate"] + random.randint(-2, 2),
                ),
            )

            patient["systolic_bp"] = max(
                70,
                min(
                    180,
                    patient["systolic_bp"] + random.randint(-3, 3),
                ),
            )

            patient["diastolic_bp"] = max(
                40,
                min(
                    120,
                    patient["diastolic_bp"] + random.randint(-2, 2),
                ),
            )

            patient["lactate"] = round(
                max(
                    0.5,
                    min(
                        8.0,
                        patient["lactate"] + random.uniform(-0.2, 0.2),
                    ),
                ),
                1,
            )

    def _generate_alerts(self):
        for patient in self.patients:
            if patient["risk_score"] >= 0.90:
                alert_manager.create_alert(
                alert_id=f"SEPSIS-{patient['id']}",
                patient_id=patient["id"],
                patient_name=patient["name"],
                bed=patient["bed"],
                severity=AlertSeverity.CRITICAL,
                title="Critical Sepsis Risk",
                message=(
                    f"Sepsis probability "
                    f"{patient['risk_score'] * 100:.1f}%"
                ),
            )
            if patient["spo2"] < 90:
                alert_manager.create_alert(
                alert_id=f"SPO2-{patient['id']}",
                patient_id=patient["id"],
                patient_name=patient["name"],
                bed=patient["bed"],
                severity=AlertSeverity.HIGH,
                title="Low Oxygen Saturation",
                message=f"SpO₂ dropped to {patient['spo2']}%",
            )
            if patient["temperature"] >= 39:
                alert_manager.create_alert(
                alert_id=f"TEMP-{patient['id']}",
                patient_id=patient["id"],
                patient_name=patient["name"],
                bed=patient["bed"],
                severity=AlertSeverity.MEDIUM,
                title="High Temperature",
                message=f"Temperature {patient['temperature']}°C",
            )
            if patient["systolic_bp"] < 90:
                alert_manager.create_alert(
                alert_id=f"BP-{patient['id']}",
                patient_id=patient["id"],
                patient_name=patient["name"],
                bed=patient["bed"],
                severity=AlertSeverity.HIGH,
                title="Hypotension",
                message=(
                    f"BP "
                    f"{patient['systolic_bp']}/"
                    f"{patient['diastolic_bp']}"
                ),
            )
        self.dashboard["active_alerts"] = len(
            alert_manager.active_alerts()
    )


simulator = ICUSimulator()