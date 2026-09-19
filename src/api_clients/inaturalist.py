"""iNaturalist API client for species occurrences and camera trap telemetry."""
import logging
from typing import Optional, List
from .base import BaseAPIClient, APIClientError
from .schemas import INatSearchResponse, INatObservation

logger = logging.getLogger(__name__)


class INaturalistClient(BaseAPIClient):
    """Client for querying real-world species occurrence data from iNaturalist."""

    BASE_URL = "https://api.inaturalist.org/v1"

    # Targeted conservation bio-indicator taxa
    INDICATOR_TAXA = [
        "Aves",         # Birds (bioacoustic & visual)
        "Mammalia",     # Mammals (camera trap)
        "Amphibia",     # Amphibians (wetland bio-indicators)
        "Insecta",      # Insects (pollinators & chorus)
        "Reptilia",     # Reptiles (thermal bio-indicators)
    ]

    def __init__(self, timeout: float = 20.0):
        # iNaturalist recommends ≤ 60 requests per minute (~1 sec interval)
        super().__init__(
            base_url=self.BASE_URL,
            timeout=timeout,
            min_request_interval=1.0,
            user_agent="BiodiversityGuardianAI/1.0 (Conservation Research; github.com/biodiversity-guardian)",
        )

    def search_observations(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 50.0,
        taxon_name: Optional[str] = None,
        per_page: int = 30,
        page: int = 1,
        quality_grade: Optional[str] = None,
    ) -> INatSearchResponse:
        """Query real wildlife observations around a coordinate point."""
        params = {
            "lat": latitude,
            "lng": longitude,
            "radius": radius_km,
            "per_page": min(per_page, 200),
            "page": page,
            "order": "desc",
            "order_by": "created_at",
            "photos": "true",
        }

        if taxon_name:
            params["taxon_name"] = taxon_name
        if quality_grade:
            params["quality_grade"] = quality_grade

        try:
            raw_data = self.get(f"{self.BASE_URL}/observations", params=params)
            return INatSearchResponse.model_validate(raw_data)
        except Exception as e:
            logger.error(
                f"iNaturalist search failed for ({latitude}, {longitude}, taxon={taxon_name}): {e}"
            )
            raise APIClientError(f"iNaturalist error: {e}") from e

    def fetch_zone_taxa(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 50.0,
        limit_per_taxon: int = 10,
    ) -> List[INatObservation]:
        """Fetch a balanced multi-taxa sample of observations for a monitoring zone."""
        all_observations: List[INatObservation] = []
        for taxon in self.INDICATOR_TAXA:
            try:
                resp = self.search_observations(
                    latitude=latitude,
                    longitude=longitude,
                    radius_km=radius_km,
                    taxon_name=taxon,
                    per_page=limit_per_taxon,
                )
                all_observations.extend(resp.results)
            except Exception as e:
                logger.warning(f"Could not retrieve {taxon} for ({latitude}, {longitude}): {e}")
                continue

        return all_observations
