"""Pydantic schemas — shared across all routers."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Common
# ---------------------------------------------------------------------------

class RiskLevel(str):
    pass

RiskLevelEnum = Literal["LOW", "MODERATE", "HIGH", "CRITICAL"]


# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------

class SpeciesTrendRow(BaseModel):
    species: str
    taxon: str
    status: Literal["Stable", "Declining", "Critical"]
    obs_count: int
    change_90d: str  # e.g. "-22%"

class TaxaBreakdown(BaseModel):
    taxa: str
    species_count: int
    abundance: int
    trend_90d: str  # e.g. "-14%"

class ShannonDataPoint(BaseModel):
    label: str        # e.g. "Jan '26"
    observed: float
    baseline: float

class OverviewMetricsResponse(BaseModel):
    biodiversity_score: float = Field(..., ge=0, le=100)
    shannon_index: float
    species_detected: int
    declining_species_count: int
    risk_level: RiskLevelEnum
    risk_confidence: float = Field(..., ge=0, le=1)
    sensors_online: str
    satellite_status: str
    alert_message: str | None
    shannon_trajectory: list[ShannonDataPoint]
    taxa_breakdown: list[TaxaBreakdown]
    priority_species: list[SpeciesTrendRow]
    radar_current: list[float]
    radar_baseline: list[float]
    radar_categories: list[str]


# ---------------------------------------------------------------------------
# Audio Classification
# ---------------------------------------------------------------------------

class AudioClassificationResponse(BaseModel):
    species: str
    confidence: float = Field(..., ge=0, le=1)
    all_probabilities: dict[str, float]
    processing_time_ms: float

class MultiSpeciesAudioResponse(BaseModel):
    detected_species: dict[str, int]
    total_segments: int
    unique_species: int
    processing_time_ms: float


# ---------------------------------------------------------------------------
# Vision / Wildlife Detection
# ---------------------------------------------------------------------------

class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

class DetectionResult(BaseModel):
    species: str
    confidence: float
    bbox: BoundingBox
    species_class: str  # bird, mammal, etc.

class WildlifeDetectionResponse(BaseModel):
    detections: list[DetectionResult]
    detection_count: int
    image_url: str         # path to annotated image served via /uploads
    processing_time_ms: float


# ---------------------------------------------------------------------------
# Risk Prediction
# ---------------------------------------------------------------------------

class RiskFeatureInput(BaseModel):
    """All 12 features the XGBoost model expects."""
    shannon_index: float = Field(default=2.5, ge=0)
    species_richness: int = Field(default=30, ge=0)
    evenness: float = Field(default=0.7, ge=0, le=1)
    temperature: float = Field(default=28.0)
    humidity: float = Field(default=65.0, ge=0, le=100)
    rainfall: float = Field(default=80.0, ge=0)
    vegetation_index: float = Field(default=0.55, ge=-1, le=1)
    soil_moisture: float = Field(default=0.3, ge=0, le=1)
    shannon_trend: float = Field(default=0.0)
    species_trend: float = Field(default=0.0)
    human_activity: float = Field(default=0.3, ge=0, le=1)
    habitat_fragmentation: float = Field(default=0.2, ge=0, le=1)

class ShapFactor(BaseModel):
    feature: str
    shap_value: float

class RiskPredictionResponse(BaseModel):
    risk_level: RiskLevelEnum
    confidence: float
    probabilities: dict[str, float]
    top_shap_factors: list[ShapFactor]
    processing_time_ms: float


# ---------------------------------------------------------------------------
# Conservation Agent
# ---------------------------------------------------------------------------

class ConservationQueryRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=2000)
    zone: str | None = None
    intervention_type: str | None = None
    budget_usd: int | None = None
    timeline: str | None = None

class ConservationQueryResponse(BaseModel):
    recommendation: str
    priority: Literal["HIGH", "MEDIUM", "LOW"]
    confidence: float | None
    processing_time_ms: float
    used_llm: bool


# ---------------------------------------------------------------------------
# Biodiversity Map
# ---------------------------------------------------------------------------

class SensorMarker(BaseModel):
    id: str
    lat: float
    lon: float
    sensor_type: Literal["audio", "camera", "environmental"]
    zone: str
    status: Literal["online", "offline", "warning"]
    last_reading: datetime | None
    biodiversity_score: float | None

class ZonePolygon(BaseModel):
    zone_id: str
    name: str
    risk_level: RiskLevelEnum
    coordinates: list[list[float]]  # [[lat, lon], ...]
    shannon_index: float
    species_count: int

class MapDataResponse(BaseModel):
    sensors: list[SensorMarker]
    zones: list[ZonePolygon]
    center: list[float]   # [lat, lon]
    zoom: int


# ---------------------------------------------------------------------------
# DB / History
# ---------------------------------------------------------------------------

class BiodiversityHistoryPoint(BaseModel):
    timestamp: datetime
    zone: str
    shannon_index: float
    species_richness: int
    biodiversity_score: float
    risk_level: RiskLevelEnum
