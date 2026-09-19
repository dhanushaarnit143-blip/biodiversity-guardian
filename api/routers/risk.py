"""
Risk router — /api/v1/risk

Endpoints:
  POST /predict   — 12-feature input → risk level + SHAP top factors
"""

from __future__ import annotations

import logging
import time

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool

from api.core.model_registry import ModelRegistry
from api.core.schemas import RiskFeatureInput, RiskPredictionResponse, ShapFactor

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/predict",
    response_model=RiskPredictionResponse,
    summary="Predict ecosystem risk level with SHAP explanations",
)
async def predict_risk(body: RiskFeatureInput) -> RiskPredictionResponse:
    """
    Accepts 12 ecosystem features and returns:
    - `risk_level`: LOW / MODERATE / HIGH / CRITICAL
    - `confidence`: probability of the predicted class
    - `probabilities`: full 4-class probability distribution
    - `top_shap_factors`: top-5 SHAP feature importances
    - `processing_time_ms`

    The XGBoost model is lazy-loaded on first request (~0.5 s cold start).
    If no trained weights exist in `models/risk_model/`, the model predicts
    with its default (untrained) parameters — results will not be meaningful
    until the model is trained via `scripts/download_datasets.py`.
    """
    predictor = ModelRegistry.get_risk_predictor()

    biodiversity = {
        "shannon_index":    body.shannon_index,
        "species_richness": body.species_richness,
        "evenness":         body.evenness,
    }
    environmental = {
        "temperature":          body.temperature,
        "humidity":             body.humidity,
        "rainfall":             body.rainfall,
        "vegetation_index":     body.vegetation_index,
        "soil_moisture":        body.soil_moisture,
        "human_activity":       body.human_activity,
        "habitat_fragmentation":body.habitat_fragmentation,
    }
    trends = {
        "shannon_trend": body.shannon_trend,
        "species_trend": body.species_trend,
    }

    t0 = time.perf_counter()
    try:
        def _run() -> tuple[dict, dict]:
            features = predictor.prepare_features(biodiversity, environmental, trends)
            prediction = predictor.predict(features)
            try:
                explanation = predictor.explain(features)
            except Exception:
                explanation = {"top_factors": [], "all_shap_values": {}}
            return prediction, explanation

        prediction, explanation = await run_in_threadpool(_run)
    except Exception as exc:
        logger.exception("Risk prediction failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    elapsed_ms = (time.perf_counter() - t0) * 1000

    top_factors = [
        ShapFactor(feature=name, shap_value=val)
        for name, val in explanation.get("top_factors", [])
    ]

    return RiskPredictionResponse(
        risk_level=prediction["risk_level"],
        confidence=prediction["confidence"],
        probabilities=prediction["probabilities"],
        top_shap_factors=top_factors,
        processing_time_ms=round(elapsed_ms, 1),
    )
