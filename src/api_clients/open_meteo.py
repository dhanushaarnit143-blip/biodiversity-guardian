"""Open-Meteo API client for current and historical weather/soil data."""
import logging
from typing import Optional, List
from .base import BaseAPIClient, APIClientError
from .schemas import OpenMeteoResponse

logger = logging.getLogger(__name__)


class OpenMeteoClient(BaseAPIClient):
    """Client for fetching meteorological telemetry from Open-Meteo."""

    FORECAST_URL = "https://api.open-meteo.com/v1"
    ARCHIVE_URL = "https://archive-api.open-meteo.com/v1"

    DEFAULT_CURRENT_VARS = [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "rain",
        "wind_speed_10m",
    ]

    DEFAULT_DAILY_VARS = [
        "temperature_2m_max",
        "temperature_2m_min",
        "temperature_2m_mean",
        "precipitation_sum",
        "relative_humidity_2m_mean",
        "wind_speed_10m_max",
        "soil_moisture_0_to_7cm_mean",
    ]

    def __init__(self, timeout: float = 15.0):
        super().__init__(
            base_url=self.FORECAST_URL,
            timeout=timeout,
            min_request_interval=0.2,  # Polite throttle
        )

    def get_current_weather(
        self,
        latitude: float,
        longitude: float,
        variables: Optional[List[str]] = None,
    ) -> OpenMeteoResponse:
        """Fetch real-time microclimate conditions for a coordinate."""
        current_vars = variables or self.DEFAULT_CURRENT_VARS
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(current_vars),
            "timezone": "auto",
        }

        try:
            raw_data = self.get(f"{self.FORECAST_URL}/forecast", params=params)
            return OpenMeteoResponse.model_validate(raw_data)
        except Exception as e:
            logger.error(f"Failed to fetch current weather for ({latitude}, {longitude}): {e}")
            raise APIClientError(f"Open-Meteo forecast error: {e}") from e

    def get_historical_weather(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
        daily_vars: Optional[List[str]] = None,
    ) -> OpenMeteoResponse:
        """Fetch historical weather telemetry for trend analysis (ISO format: YYYY-MM-DD)."""
        daily_metrics = daily_vars or self.DEFAULT_DAILY_VARS
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": ",".join(daily_metrics),
            "timezone": "auto",
        }

        try:
            raw_data = self.get(f"{self.ARCHIVE_URL}/archive", params=params)
            return OpenMeteoResponse.model_validate(raw_data)
        except Exception as e:
            logger.error(
                f"Failed to fetch historical weather for ({latitude}, {longitude}) [{start_date}..{end_date}]: {e}"
            )
            raise APIClientError(f"Open-Meteo archive error: {e}") from e
