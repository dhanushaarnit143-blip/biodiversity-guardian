"""Image data collection for camera trap wildlife detection."""
import requests
import json
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ImageCollector:
    """Collect wildlife camera trap images."""

    INATURALIST_API = "https://api.inaturalist.org/v1/observations"

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir / "images"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def search_inaturalist(
        self,
        taxon_name: str = "Aves",
        lat: float = -16.5,
        lon: float = -56.5,
        radius_km: int = 50,
        per_page: int = 30
    ) -> list[dict]:
        """Search iNaturalist for wildlife observations."""
        params = {
            "taxon_name": taxon_name,
            "lat": lat,
            "lng": lon,
            "radius": radius_km,
            "per_page": per_page,
            "order": "desc",
            "order_by": "created_at",
            "photos": "true",
        }
        try:
            resp = requests.get(self.INATURALIST_API, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data.get("results", [])
        except Exception as e:
            logger.error(f"iNaturalist search failed: {e}")
            return []

    def download_image(self, photo_url: str, filename: str) -> Optional[Path]:
        """Download a single image."""
        filepath = self.data_dir / filename
        if filepath.exists():
            return filepath

        try:
            resp = requests.get(photo_url, timeout=30, stream=True)
            resp.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            return filepath
        except Exception as e:
            logger.error(f"Image download failed: {e}")
            return None

    def collect_wildlife_images(
        self,
        taxon: str = "Aves",
        location: tuple[float, float] = (-16.5, -56.5),
        max_images: int = 30
    ) -> list[dict]:
        """Collect wildlife images for a taxon and location."""
        observations = self.search_inaturalist(
            taxon_name=taxon,
            lat=location[0],
            lon=location[1],
            per_page=max_images
        )

        results = []
        for obs in observations:
            photos = obs.get("photos", [])
            if not photos:
                continue

            photo_url = photos[0].get("url", "").replace("square", "medium")
            species = obs.get("taxon", {}).get("name", "Unknown")
            obs_id = obs.get("id", 0)

            filepath = self.download_image(
                photo_url,
                f"inat_{obs_id}.jpg"
            )

            if filepath:
                results.append({
                    "species": species,
                    "common_name": obs.get("taxon", {}).get("preferred_common_name", ""),
                    "file_path": str(filepath),
                    "latitude": obs.get("geojson", {}).get("coordinates", [None, None])[1],
                    "longitude": obs.get("geojson", {}).get("coordinates", [None, None])[0],
                    "observed_on": obs.get("observed_on", ""),
                    "location": obs.get("place_guess", ""),
                })

        return results

    def collect_tropical_forest_images(self) -> dict[str, list[dict]]:
        """Collect images for tropical forest species."""
        taxa = {
            "birds": "Aves",
            "mammals": "Mammalia",
            "amphibians": "Amphibia",
            "reptiles": "Reptilia",
            "insects": "Insecta",
        }

        all_data = {}
        for category, taxon in taxa.items():
            all_data[category] = self.collect_wildlife_images(
                taxon=taxon,
                location=(-16.5, -56.5),
                max_images=20
            )

        return all_data
