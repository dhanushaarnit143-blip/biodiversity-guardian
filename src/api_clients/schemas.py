"""Pydantic V2 validation schemas for Open-Meteo and iNaturalist APIs."""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# ==============================================================================
# Open-Meteo Schemas
# ==============================================================================

class OpenMeteoCurrent(BaseModel):
    """Current weather metrics from Open-Meteo forecast endpoint."""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    time: str
    temperature_2m: Optional[float] = None
    relative_humidity_2m: Optional[float] = None
    precipitation: Optional[float] = None
    rain: Optional[float] = None
    wind_speed_10m: Optional[float] = None
    soil_moisture_0_7cm: Optional[float] = Field(
        default=None,
        validation_alias="soil_moisture_0_7cm"
    )


class OpenMeteoDaily(BaseModel):
    """Historical or daily aggregate weather metrics."""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    time: list[str] = Field(default_factory=list)
    temperature_2m_max: list[Optional[float]] = Field(default_factory=list)
    temperature_2m_min: list[Optional[float]] = Field(default_factory=list)
    temperature_2m_mean: list[Optional[float]] = Field(default_factory=list)
    precipitation_sum: list[Optional[float]] = Field(default_factory=list)
    relative_humidity_2m_mean: list[Optional[float]] = Field(default_factory=list)
    wind_speed_10m_max: list[Optional[float]] = Field(default_factory=list)
    soil_moisture_0_to_7cm_mean: list[Optional[float]] = Field(default_factory=list)


class OpenMeteoResponse(BaseModel):
    """Top-level parsed Open-Meteo weather response."""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    latitude: float
    longitude: float
    elevation: Optional[float] = None
    timezone: Optional[str] = None
    current: Optional[OpenMeteoCurrent] = None
    daily: Optional[OpenMeteoDaily] = None


# ==============================================================================
# iNaturalist Schemas
# ==============================================================================

class INatPhoto(BaseModel):
    """Observation photo item."""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: int
    url: Optional[str] = None

    @property
    def medium_url(self) -> Optional[str]:
        """Convert default square thumbnail url to medium resolution."""
        if self.url and "square" in self.url:
            return self.url.replace("square", "medium")
        return self.url


class INatTaxon(BaseModel):
    """Taxonomic details for an observed species."""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: int
    name: str
    preferred_common_name: Optional[str] = None
    iconic_taxon_name: Optional[str] = None
    rank: Optional[str] = None


class INatGeoJSON(BaseModel):
    """GeoJSON coordinate specification for observation point."""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    type: Optional[str] = "Point"
    coordinates: list[float] = Field(default_factory=list)  # [longitude, latitude]

    @property
    def latitude(self) -> Optional[float]:
        return self.coordinates[1] if len(self.coordinates) >= 2 else None

    @property
    def longitude(self) -> Optional[float]:
        return self.coordinates[0] if len(self.coordinates) >= 2 else None


class INatObservation(BaseModel):
    """Individual wildlife observation record from iNaturalist."""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: int
    uuid: Optional[str] = None
    observed_on: Optional[str] = None
    time_observed_at: Optional[str] = None
    quality_grade: Optional[str] = None  # 'research', 'needs_id', 'casual'
    place_guess: Optional[str] = None
    uri: Optional[str] = None
    geojson: Optional[INatGeoJSON] = None
    taxon: Optional[INatTaxon] = None
    photos: list[INatPhoto] = Field(default_factory=list)


class INatSearchResponse(BaseModel):
    """Paginated search response envelope from iNaturalist."""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    total_results: int = 0
    page: int = 1
    per_page: int = 30
    results: list[INatObservation] = Field(default_factory=list)
