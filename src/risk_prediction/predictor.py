"""Biodiversity risk prediction using XGBoost."""
import numpy as np
import json
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

FEATURE_NAMES = [
    "shannon_index", "species_richness", "evenness",
    "temperature", "humidity", "rainfall",
    "vegetation_index", "soil_moisture",
    "shannon_trend", "species_trend",
    "human_activity_index", "habitat_fragmentation"
]

RISK_LEVELS = ["LOW", "MODERATE", "HIGH", "CRITICAL"]


class BiodiversityRiskPredictor:
    def __init__(self, model_path: Optional[Path] = None):
        self.feature_names = FEATURE_NAMES
        self.risk_levels = RISK_LEVELS
        self._model = None
        self._explainer = None

        if model_path and model_path.exists():
            self.load_model(model_path)

    @property
    def model(self):
        if self._model is None:
            import xgboost as xgb
            self._model = xgb.XGBClassifier(
                n_estimators=100, max_depth=6, learning_rate=0.1,
                objective="multi:softprob", num_class=4, eval_metric="mlogloss",
                use_label_encoder=False
            )
        return self._model

    def prepare_features(self, biodiversity: dict, environmental: dict, trends: Optional[dict] = None) -> np.ndarray:
        trends = trends or {}
        features = [
            biodiversity.get("shannon_index", 0),
            biodiversity.get("species_richness", 0),
            biodiversity.get("evenness", 0),
            environmental.get("temperature", 25),
            environmental.get("humidity", 70),
            environmental.get("rainfall", 100),
            environmental.get("vegetation_index", 0.6),
            environmental.get("soil_moisture", 0.3),
            trends.get("shannon_trend", 0),
            trends.get("species_trend", 0),
            environmental.get("human_activity", 0.2),
            environmental.get("habitat_fragmentation", 0.1),
        ]
        return np.array(features).reshape(1, -1)

    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the risk prediction model."""
        self.model.fit(X, y)
        logger.info("Risk prediction model trained")

    def predict(self, features: np.ndarray) -> dict:
        probs = self.model.predict_proba(features)[0]
        risk_idx = np.argmax(probs)
        return {
            "risk_level": self.risk_levels[risk_idx],
            "confidence": round(float(probs[risk_idx]), 4),
            "probabilities": {self.risk_levels[i]: round(float(p), 4) for i, p in enumerate(probs)},
        }

    def explain(self, features: np.ndarray) -> dict:
        import shap
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(features)

        if isinstance(shap_values, list):
            values = shap_values[0]
        else:
            values = shap_values

        feature_importance = sorted(
            zip(self.feature_names, values[0].tolist()),
            key=lambda x: abs(x[1]), reverse=True
        )
        return {
            "top_factors": feature_importance[:5],
            "all_shap_values": {name: round(float(val), 4) for name, val in zip(self.feature_names, values[0].tolist())},
        }

    def save_model(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.model.save_model(str(path / "risk_model.json"))
        logger.info(f"Model saved to {path}")

    def load_model(self, path: Path):
        self.model.load_model(str(path / "risk_model.json"))
        logger.info(f"Model loaded from {path}")