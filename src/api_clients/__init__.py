"""API Clients package for live conservation telemetry."""
from .base import BaseAPIClient, APIClientError, RateLimitError
from .open_meteo import OpenMeteoClient
from .inaturalist import INaturalistClient
from .schemas import (
    OpenMeteoCurrent,
    OpenMeteoDaily,
    OpenMeteoResponse,
    INatPhoto,
    INatTaxon,
    INatGeoJSON,
    INatObservation,
    INatSearchResponse,
)

__all__ = [
    "BaseAPIClient",
    "APIClientError",
    "RateLimitError",
    "OpenMeteoClient",
    "INaturalistClient",
    "OpenMeteoResponse",
    "OpenMeteoCurrent",
    "OpenMeteoDaily",
    "INatObservation",
    "INatTaxon",
    "INatGeoJSON",
    "INatPhoto",
    "INatSearchResponse",
]
