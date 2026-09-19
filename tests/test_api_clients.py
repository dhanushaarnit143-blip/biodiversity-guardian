"""Unit and integration tests for API clients, schemas, and ingestion pipeline."""
import pytest
from src.api_clients.schemas import (
    OpenMeteoResponse,
    OpenMeteoCurrent,
    INatObservation,
    INatTaxon,
    INatGeoJSON,
    INatPhoto,
    INatSearchResponse,
)
from src.api_clients.open_meteo import OpenMeteoClient
from src.api_clients.inaturalist import INaturalistClient
from src.database.models import SessionLocal, Observation, SpeciesDetection, EnvironmentalData, BiodiversityMetric
from scripts.ingest_real_data import ingest_live_data, determine_risk_level, map_quality_to_confidence


def test_open_meteo_schema_validation():
    """Test parsing Open-Meteo current payload."""
    payload = {
        "latitude": -16.82,
        "longitude": -56.24,
        "timezone": "America/Cuiaba",
        "current": {
            "time": "2026-09-19T01:15",
            "temperature_2m": 28.5,
            "relative_humidity_2m": 65.0,
            "precipitation": 0.0,
            "wind_speed_10m": 2.1,
            "soil_moisture_0_7cm": 0.32,
        }
    }
    parsed = OpenMeteoResponse.model_validate(payload)
    assert parsed.latitude == -16.82
    assert parsed.current is not None
    assert parsed.current.temperature_2m == 28.5
    assert parsed.current.soil_moisture_0_7cm == 0.32


def test_inaturalist_schema_validation():
    """Test parsing iNaturalist observation item."""
    payload = {
        "id": 987654321,
        "uuid": "abc-123",
        "quality_grade": "research",
        "observed_on": "2026-09-18",
        "geojson": {
            "type": "Point",
            "coordinates": [-56.24, -16.82]
        },
        "taxon": {
            "id": 1234,
            "name": "Panthera onca",
            "preferred_common_name": "Jaguar",
            "iconic_taxon_name": "Mammalia"
        },
        "photos": [
            {"id": 1, "url": "https://inaturalist-open-data.s3.amazonaws.com/photos/1/square.jpg"}
        ]
    }
    obs = INatObservation.model_validate(payload)
    assert obs.id == 987654321
    assert obs.taxon.preferred_common_name == "Jaguar"
    assert obs.geojson.latitude == -16.82
    assert obs.geojson.longitude == -56.24
    assert obs.photos[0].medium_url == "https://inaturalist-open-data.s3.amazonaws.com/photos/1/medium.jpg"


def test_risk_level_determination():
    """Test ecological risk mapping logic."""
    assert determine_risk_level(shannon_h=2.1, temp=30.0, precipitation=2.0) == "CRITICAL"
    assert determine_risk_level(shannon_h=2.9, temp=36.0, precipitation=0.2) == "CRITICAL"
    assert determine_risk_level(shannon_h=3.0, temp=27.0, precipitation=5.0) == "HIGH"
    assert determine_risk_level(shannon_h=3.5, temp=25.0, precipitation=10.0) == "MODERATE"
    assert determine_risk_level(shannon_h=4.1, temp=24.0, precipitation=15.0) == "LOW"


def test_quality_confidence_mapping():
    """Test mapping quality grades to model confidence."""
    assert map_quality_to_confidence("research") == 0.96
    assert map_quality_to_confidence("needs_id") == 0.78
    assert map_quality_to_confidence("casual") == 0.65


def test_upsert_idempotency():
    """Verify that re-running ingestion updates existing rows rather than duplicating."""
    db = SessionLocal()
    try:
        initial_inat_count = db.query(Observation).filter(Observation.source == "inaturalist").count()
        initial_meteo_count = db.query(Observation).filter(Observation.source == "open-meteo").count()
        
        # Ingest one small zone again
        test_zone = [{
            "id": "ZA",
            "name": "Wetland Zone A (Lagoa das Araras)",
            "lat": -16.82,
            "lon": -56.24,
            "radius_km": 20.0,
        }]
        result = ingest_live_data(zones=test_zone, limit_per_taxon=2)
        assert result["status"] in ("success", "cached_fallback")

        # Open-Meteo observations should stay the same count (upserted)
        new_meteo_count = db.query(Observation).filter(Observation.source == "open-meteo").count()
        assert new_meteo_count == initial_meteo_count
    finally:
        db.close()
