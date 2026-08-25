"""
Load IntelliICU Production Model
"""

from pathlib import Path
import threading
import logging

logger = logging.getLogger(__name__)

MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "ml_models"
    / "intelliicu_final_model.pkl"
)

class LazyModelProxy:
    def __init__(self, path):
        self._path = path
        self._model = None
        self._lock = threading.Lock()

    def _load_model(self):
        if self._model is None:
            with self._lock:
                if self._model is None:
                    logger.info("Loading IntelliICU production ML model (809MB)...")
                    import joblib
                    self._model = joblib.load(self._path)
                    logger.info("IntelliICU production ML model loaded successfully.")
        return self._model

    def __getattr__(self, name):
        model = self._load_model()
        return getattr(model, name)

MODEL = LazyModelProxy(MODEL_PATH)