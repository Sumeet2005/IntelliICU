"""
Seeder Safety & Simulator Control Tests.
Compatible with both pytest and python -m unittest.
"""

import os
import unittest
from unittest.mock import patch

from app.database.seeder import seed_database_if_empty
from app.websocket.simulator import ICUSimulator


class TestSeederAndSimulatorSafety(unittest.TestCase):
    def test_seeder_skipped_when_disabled(self):
        with patch.dict(os.environ, {"ENABLE_DEMO_SEED": "false"}):
            with patch("app.database.seeder.SessionLocal") as mock_session:
                seed_database_if_empty(force=False)
                mock_session.assert_not_called()

    def test_simulator_db_persistence_disabled_by_default(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("SIMULATOR_PERSIST_DB", None)
            sim = ICUSimulator()
            self.assertFalse(sim.persist_to_db)

    def test_simulator_stop_flag(self):
        sim = ICUSimulator()
        sim._running = True
        sim.stop()
        self.assertFalse(sim._running)


if __name__ == "__main__":
    unittest.main()
