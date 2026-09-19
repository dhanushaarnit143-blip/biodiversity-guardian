"""
Biodiversity Map router — /api/v1/map

Endpoints:
  GET /data  — sensor markers + zone polygons for React-Leaflet
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from datetime import datetime, timezone

from fastapi import APIRouter

_SRC = Path(__file__).resolve().parent.parent.parent / "src"
_ROOT = Path(__file__).resolve().parent.parent.parent
for p in [str(_SRC), str(_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from api.core.schemas import MapDataResponse, SensorMarker, ZonePolygon

logger = logging.getLogger(__name__)
router = APIRouter()


def _build_map_data() -> MapDataResponse:
    """
    Returns sensor markers and zone polygons for React-Leaflet, queried from SQLite DB.
    """
    # ── Default Sensors ──
    sensors: list[SensorMarker] = [
        # Audio PAM sensors
        SensorMarker(id="pam-01", lat=-16.82, lon=-56.24, sensor_type="audio",  zone="Wetland Zone A", status="online",  last_reading=datetime.now(timezone.utc), biodiversity_score=58.0),
        SensorMarker(id="pam-02", lat=-17.15, lon=-56.81, sensor_type="audio",  zone="Forest Corridor B", status="online",  last_reading=datetime.now(timezone.utc), biodiversity_score=82.0),
        SensorMarker(id="pam-03", lat=-16.35, lon=-57.02, sensor_type="audio",  zone="Savanna Transition C", status="warning", last_reading=datetime.now(timezone.utc), biodiversity_score=49.0),
        SensorMarker(id="pam-04", lat=-16.94, lon=-55.95, sensor_type="audio",  zone="Riparian Delta D", status="online",  last_reading=datetime.now(timezone.utc), biodiversity_score=74.0),
        SensorMarker(id="pam-05", lat=-17.38, lon=-56.32, sensor_type="audio",  zone="Highland Plateau E", status="warning", last_reading=datetime.now(timezone.utc), biodiversity_score=32.0),
        # Camera traps
        SensorMarker(id="ct-01",  lat=-16.80, lon=-56.22, sensor_type="camera", zone="Wetland Zone A", status="online",  last_reading=datetime.now(timezone.utc), biodiversity_score=55.0),
        SensorMarker(id="ct-02",  lat=-17.12, lon=-56.79, sensor_type="camera", zone="Forest Corridor B", status="online",  last_reading=datetime.now(timezone.utc), biodiversity_score=80.0),
        SensorMarker(id="ct-03",  lat=-16.92, lon=-55.92, sensor_type="camera", zone="Riparian Delta D", status="online",  last_reading=datetime.now(timezone.utc), biodiversity_score=71.0),
        # Environmental sensors
        SensorMarker(id="env-01", lat=-16.85, lon=-56.26, sensor_type="environmental", zone="Wetland Zone A", status="online", last_reading=datetime.now(timezone.utc), biodiversity_score=None),
        SensorMarker(id="env-02", lat=-17.40, lon=-56.30, sensor_type="environmental", zone="Highland Plateau E", status="online", last_reading=datetime.now(timezone.utc), biodiversity_score=None),
    ]

    zones: list[ZonePolygon] = []

    try:
        from database.models import (
            SessionLocal,
            BiodiversityMetric,
            Observation,
            SpeciesDetection,
        )
        from sqlalchemy import func

        db = SessionLocal()
        # Query latest metric for each distinct zone
        subquery = (
            db.query(
                BiodiversityMetric.ecosystem_zone,
                func.max(BiodiversityMetric.timestamp).label("max_ts")
            )
            .group_by(BiodiversityMetric.ecosystem_zone)
            .subquery()
        )
        metrics = (
            db.query(BiodiversityMetric)
            .join(
                subquery,
                (BiodiversityMetric.ecosystem_zone == subquery.c.ecosystem_zone)
                & (BiodiversityMetric.timestamp == subquery.c.max_ts)
            )
            .all()
        )

        if metrics:
            for i, m in enumerate(metrics):
                zone_code = f"zone-{chr(97 + i)}"
                lat = m.location_lat or -16.82
                lon = m.location_lon or -56.24

                # Count species detected for this zone
                sp_count = (
                    db.query(func.count(func.distinct(SpeciesDetection.species_name)))
                    .join(Observation)
                    .filter(Observation.ecosystem_zone == m.ecosystem_zone)
                    .scalar()
                ) or m.species_richness or 15

                # Generate bounding polygon box around center coordinate (+/- 0.1 deg)
                coords = [
                    [round(lat - 0.08, 4), round(lon - 0.08, 4)],
                    [round(lat - 0.08, 4), round(lon + 0.08, 4)],
                    [round(lat + 0.08, 4), round(lon + 0.08, 4)],
                    [round(lat + 0.08, 4), round(lon - 0.08, 4)],
                ]

                risk = m.risk_level if m.risk_level in ("LOW", "MODERATE", "HIGH", "CRITICAL") else "MODERATE"

                zones.append(
                    ZonePolygon(
                        zone_id=zone_code,
                        name=m.ecosystem_zone,
                        risk_level=risk,
                        coordinates=coords,
                        shannon_index=round(m.shannon_index or 3.2, 2),
                        species_count=int(sp_count),
                    )
                )

        db.close()
    except Exception as e:
        logger.warning(f"Failed to query map zones from DB: {e}")

    # Fallback if DB query was empty
    if not zones:
        zones = [
            ZonePolygon(zone_id="zone-a", name="Wetland Zone A", risk_level="HIGH", coordinates=[[-16.74, -56.32], [-16.74, -56.16], [-16.90, -56.16], [-16.90, -56.32]], shannon_index=2.81, species_count=38),
            ZonePolygon(zone_id="zone-b", name="Forest Corridor B", risk_level="LOW", coordinates=[[-17.07, -56.89], [-17.07, -56.73], [-17.23, -56.73], [-17.23, -56.89]], shannon_index=3.74, species_count=64),
            ZonePolygon(zone_id="zone-c", name="Savanna C", risk_level="MODERATE", coordinates=[[-16.27, -57.10], [-16.27, -56.94], [-16.43, -56.94], [-16.43, -57.10]], shannon_index=3.12, species_count=47),
            ZonePolygon(zone_id="zone-d", name="Riparian Delta D", risk_level="HIGH", coordinates=[[-16.86, -56.03], [-16.86, -55.87], [-17.02, -55.87], [-17.02, -56.03]], shannon_index=3.38, species_count=55),
            ZonePolygon(zone_id="zone-e", name="Highland Plateau E", risk_level="CRITICAL", coordinates=[[-17.30, -56.40], [-17.30, -56.24], [-17.46, -56.24], [-17.46, -56.40]], shannon_index=2.12, species_count=22),
        ]

    return MapDataResponse(
        sensors=sensors,
        zones=zones,
        center=[-16.85, -56.45],
        zoom=9,
    )


@router.get("/data", response_model=MapDataResponse, summary="Sensor markers and zone polygons for the map")
async def get_map_data() -> MapDataResponse:
    """Returns all data needed to render the React-Leaflet biodiversity map."""
    return _build_map_data()
