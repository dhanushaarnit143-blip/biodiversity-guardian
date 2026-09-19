"""
ModelRegistry — centralised, thread-safe lazy loader for all ML models.

Design decisions
----------------
- Every model is a module-level singleton loaded exactly once (idempotent).
- Heavy models (YOLO, TinyLlama) are **not** pre-loaded at startup; they are
  loaded on first request.  This keeps startup time under 2 s.
- A threading.Lock per model prevents duplicate initialisation under concurrent
  requests (e.g., two audio requests arriving simultaneously at cold start).
"""

from __future__ import annotations

import logging
import sys
import threading
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.audio_processing.species_classifier import AudioSpeciesClassifier
    from src.conservation_agent.agent import ConservationAgent
    from src.image_detection.detector import WildlifeDetector
    from src.risk_prediction.predictor import BiodiversityRiskPredictor

logger = logging.getLogger(__name__)

# Ensure src/ is importable
_SRC = Path(__file__).resolve().parent.parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

_MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"


class ModelRegistry:
    """Singleton registry for all ML models."""

    _audio_classifier: "AudioSpeciesClassifier | None" = None
    _wildlife_detector: "WildlifeDetector | None" = None
    _risk_predictor: "BiodiversityRiskPredictor | None" = None
    _conservation_agent: "ConservationAgent | None" = None

    _audio_lock = threading.Lock()
    _vision_lock = threading.Lock()
    _risk_lock = threading.Lock()
    _agent_lock = threading.Lock()

    # ------------------------------------------------------------------
    # Audio CNN (ResNet18 + mel spectrogram)
    # ------------------------------------------------------------------
    @classmethod
    def get_audio_classifier(cls) -> "AudioSpeciesClassifier":
        if cls._audio_classifier is None:
            with cls._audio_lock:
                if cls._audio_classifier is None:  # double-checked locking
                    from src.audio_processing.species_classifier import AudioSpeciesClassifier
                    model_path = _MODELS_DIR / "audio_model"
                    cls._audio_classifier = AudioSpeciesClassifier(
                        model_path=model_path if model_path.exists() else None
                    )
                    logger.info("✅ AudioSpeciesClassifier loaded")
        return cls._audio_classifier

    # ------------------------------------------------------------------
    # YOLOv8 Wildlife Detector
    # ------------------------------------------------------------------
    @classmethod
    def get_wildlife_detector(cls) -> "WildlifeDetector":
        if cls._wildlife_detector is None:
            with cls._vision_lock:
                if cls._wildlife_detector is None:
                    from src.image_detection.detector import WildlifeDetector
                    cls._wildlife_detector = WildlifeDetector()
                    logger.info("✅ WildlifeDetector (YOLOv8) loaded")
        return cls._wildlife_detector

    # ------------------------------------------------------------------
    # XGBoost Risk Predictor
    # ------------------------------------------------------------------
    @classmethod
    def get_risk_predictor(cls) -> "BiodiversityRiskPredictor":
        if cls._risk_predictor is None:
            with cls._risk_lock:
                if cls._risk_predictor is None:
                    from src.risk_prediction.predictor import BiodiversityRiskPredictor
                    model_path = _MODELS_DIR / "risk_model"
                    cls._risk_predictor = BiodiversityRiskPredictor(
                        model_path=model_path if model_path.exists() else None
                    )
                    logger.info("✅ BiodiversityRiskPredictor (XGBoost) loaded")
        return cls._risk_predictor

    # ------------------------------------------------------------------
    # TinyLlama Conservation Agent
    # ------------------------------------------------------------------
    @classmethod
    def get_conservation_agent(cls) -> "ConservationAgent":
        if cls._conservation_agent is None:
            with cls._agent_lock:
                if cls._conservation_agent is None:
                    from src.conservation_agent.agent import ConservationAgent
                    cls._conservation_agent = ConservationAgent()
                    logger.info("✅ ConservationAgent (TinyLlama) loaded (LLM lazy)")
        return cls._conservation_agent
