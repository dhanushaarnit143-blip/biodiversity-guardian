"""Environmental data collection from Open-Meteo API."""
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import json
import logging

logger = logging.getLogger(__name__)


class EnvironmentalCollector:
    """Collect environmental/weather data from Open-Meteo."""

    BASE_URL = "https://archive-api.open-meteo.com/v1"
    FORECAST_URL = "https://api.open-meteo.com/v1"

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir / "environmental"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def get_historical_weather(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
        daily_vars: Optional[list[str]] = None,
    ) -> dict:
        """Fetch historical weather data."""
        if daily_vars is None:
            daily_vars = [
                "temperature_2m_max",
                "temperature_2m_min",
                "temperature_2m_mean",
                "precipitation_sum",
                "relative_humidity_2m_mean",
                "wind_speed_10m_max",
                "soil_moisture_0_to_7cm_mean",
            ]

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": ",".join(daily_vars),
            "timezone": "auto",
        }

        try:
            resp = requests.get(f"{self.BASE_URL}/archive", params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"Historical weather fetch failed: {e}")
            return {}

    def get_current_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        """Fetch current weather conditions."""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,precipitation,rain,wind_speed_10m,soil_moisture_0_7cm",
            "timezone": "auto",
        }

        try:
            resp = requests.get(f"{self.FORECAST_URL}/forecast", params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"Current weather fetch failed: {e}")
            return {}

    def collect_ecosystem_environmental_data(
        self,
        latitude: float = -16.5,
        longitude: float = -56.5,
        months_back: int = 12,
    ) -> list[dict]:
        """Collect environmental data for ecosystem monitoring."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months_back * 30)

        historical = self.get_historical_weather(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
        )

        current = self.get_current_weather(
            latitude=latitude,
            longitude=longitude,
        )

        results = []
        daily = historical.get("daily", {})
        dates = daily.get("time", [])

        for i, date in enumerate(dates):
            results.append({
                "date": date,
                "latitude": latitude,
                "longitude": longitude,
                "temperature_max": daily.get("temperature_2m_max", [None])[i],
                "temperature_min": daily.get("temperature_2m_min", [None])[i],
                "temperature_mean": daily.get("temperature_2m_mean", [None])[i],
                "precipitation_mm": daily.get("precipitation_sum", [None])[i],
                "humidity_pct": daily.get("relative_humidity_2m_mean", [None])[i],
                "wind_speed_max": daily.get("wind_speed_10m_max", [None])[i],
                "soil_moisture": daily.get("soil_moisture_0_to_7cm_mean", [None])[i],
            })

        current_data = current.get("current", {})
        if current_data:
            results.append({
                "date": current_data.get("time", ""),
                "latitude": latitude,
                "longitude": longitude,
                "temperature_mean": current_data.get("temperature_2m"),
                "humidity_pct": current_data.get("relative_humidity_2m"),
                "precipitation_mm": current_data.get("precipitation"),
                "wind_speed_max": current_data.get("wind_speed_10m"),
                "soil_moisture": current_data.get("soil_moisture_0_7cm"),
                "is_current": True,
            })

        return results

    def save_environmental_data(self, data: list[dict], filename: str = "environmental_data.json"):
        """Save environmental data to file."""
        filepath = self.data_dir / filename
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved environmental data to {filepath}")
        return filepath
