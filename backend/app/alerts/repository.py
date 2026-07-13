"""
Enterprise Alert Repository
Stores and manages ICU alerts.
"""

from typing import Dict, List

from app.alerts.models import ICUAlert, AlertStatus


class AlertRepository:
    """
    In-memory alert repository.

    Later this can be replaced by PostgreSQL
    without changing the API layer.
    """

    def __init__(self):
        self._alerts: Dict[str, ICUAlert] = {}

    # --------------------------
    # CRUD
    # --------------------------

    def add(self, alert: ICUAlert):

        self._alerts[alert.id] = alert

    def get(self, alert_id: str):

        return self._alerts.get(alert_id)

    def get_all(self) -> List[ICUAlert]:

        return list(self._alerts.values())

    def remove(self, alert_id: str):

        if alert_id in self._alerts:
            del self._alerts[alert_id]

    # --------------------------
    # Status
    # --------------------------

    def acknowledge(self, alert_id: str):

        alert = self.get(alert_id)

        if alert:

            alert.status = AlertStatus.ACKNOWLEDGED

    def escalate(self, alert_id: str):

        alert = self.get(alert_id)

        if alert:

            alert.status = AlertStatus.ESCALATED

    def resolve(self, alert_id: str):

        alert = self.get(alert_id)

        if alert:

            alert.status = AlertStatus.RESOLVED

    # --------------------------
    # Active Alerts
    # --------------------------

    def active(self) -> List[ICUAlert]:

        return [
            alert
            for alert in self._alerts.values()
            if alert.status != AlertStatus.RESOLVED
        ]

    # --------------------------
    # Cleanup
    # --------------------------

    def cleanup(self):

        resolved = []

        for alert in self._alerts.values():

            if alert.status == AlertStatus.RESOLVED:

                resolved.append(alert.id)

        for alert_id in resolved:

            self.remove(alert_id)


repository = AlertRepository()