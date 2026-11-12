"""Add missing admissions.patient_id index and NOT VALID FKs on alerts/timeline_events

Revision ID: c2d3e4f5a6b7
Revises: abaff91c38da
Create Date: 2026-11-12 15:05:00.000000
"""

from typing import Sequence, Union
from alembic import op


revision: str = "c2d3e4f5a6b7"
down_revision: Union[str, Sequence[str], None] = "abaff91c38da"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_admissions_patient_id ON admissions (patient_id)"
    )

    if dialect == "postgresql":
        # Use NOT VALID so existing pre-audit orphan timeline_events are preserved
        # while all new inserts/updates are strictly validated against patients(id).
        op.execute(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint WHERE conname = 'fk_alerts_patient_id'
                ) THEN
                    ALTER TABLE alerts
                    ADD CONSTRAINT fk_alerts_patient_id
                    FOREIGN KEY (patient_id) REFERENCES patients(id) NOT VALID;
                END IF;

                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint WHERE conname = 'fk_timeline_events_patient_id'
                ) THEN
                    ALTER TABLE timeline_events
                    ADD CONSTRAINT fk_timeline_events_patient_id
                    FOREIGN KEY (patient_id) REFERENCES patients(id) NOT VALID;
                END IF;
            END $$;
            """
        )


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("ALTER TABLE timeline_events DROP CONSTRAINT IF EXISTS fk_timeline_events_patient_id")
        op.execute("ALTER TABLE alerts DROP CONSTRAINT IF EXISTS fk_alerts_patient_id")
    op.execute("DROP INDEX IF EXISTS ix_admissions_patient_id")
