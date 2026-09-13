"""Audio data collection from Xeno-Canto and BirdCLEF datasets."""
import requests
import json
from pathlib import Path
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AudioCollector:
    """Collect wildlife audio recordings."""

    XENOCANTO_API = "https://xeno-canto.org/api/2/recordings"

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir / "audio"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def search_xenocanto(
        self,
        query: str = "gen:bird",
        page: int = 1,
        count: int = 50
    ) -> list[dict]:
        """Search Xeno-Canto for bird recordings."""
        params = {
            "query": query,
            "page": page,
            "cnt": count
        }
        try:
            resp = requests.get(self.XENOCANTO_API, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data.get("recordings", [])
        except Exception as e:
            logger.error(f"Xeno-Canto search failed: {e}")
            return []

    def download_recording(self, recording: dict) -> Optional[Path]:
        """Download a single recording."""
        rec_id = recording.get("id")
        file_url = recording.get("file")
        if not file_url:
            return None

        filename = f"xc_{rec_id}.mp3"
        filepath = self.data_dir / filename

        if filepath.exists():
            return filepath

        try:
            resp = requests.get(f"https:{file_url}", timeout=60, stream=True)
            resp.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info(f"Downloaded: {filename}")
            return filepath
        except Exception as e:
            logger.error(f"Download failed for {rec_id}: {e}")
            return None

    def collect_species_audio(
        self,
        species_name: str,
        max_recordings: int = 20
    ) -> list[dict]:
        """Collect audio for a specific species."""
        query = f"sp:{species_name}"
        recordings = self.search_xenocanto(query=query, count=max_recordings)

        results = []
        for rec in recordings:
            filepath = self.download_recording(rec)
            if filepath:
                results.append({
                    "species": rec.get("en", species_name),
                    "scientific_name": rec.get("sp", ""),
                    "file_path": str(filepath),
                    "location": rec.get("loc", ""),
                    "date": rec.get("date", ""),
                    "latitude": rec.get("lat"),
                    "longitude": rec.get("lng"),
                    "length": rec.get("length"),
                })

        return results

    def collect_tropical_forest_species(self) -> dict[str, list[dict]]:
        """Collect audio for key tropical forest indicator species."""
        indicator_species = {
            "birds": [
                "Asian Koel", "Indian Peafowl", "Hornbill",
                "Kingfisher", "Woodpecker", "Crow"
            ],
            "amphibians": [
                "Indian Frog", "Tree Frog", "Bullfrog"
            ],
            "insects": [
                "Cicada", "Cricket", "Grasshopper"
            ],
            "mammals": [
                "Indian Bat", "Langur", "Monkey"
            ]
        }

        all_data = {}
        for category, species_list in indicator_species.items():
            all_data[category] = []
            for species in species_list:
                data = self.collect_species_audio(species, max_recordings=5)
                all_data[category].extend(data)

        return all_data
