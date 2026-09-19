"""Base HTTP client with rate-limiting, retries, and error handling."""
import logging
import time
from typing import Any, Optional, Dict
import httpx

logger = logging.getLogger(__name__)


class APIClientError(Exception):
    """Base exception for API client failures."""
    pass


class RateLimitError(APIClientError):
    """Raised when an API rate limit is exceeded after retries."""
    pass


class BaseAPIClient:
    """Robust synchronous HTTP client powered by httpx.

    Features:
    - Exponential backoff retry on 429 and transient 5xx errors.
    - Automatic request rate throttling (respecting polite usage limits).
    - Descriptive error handling and timeouts.
    - Context manager support.
    """

    def __init__(
        self,
        base_url: str = "",
        timeout: float = 15.0,
        max_retries: int = 3,
        backoff_factor: float = 1.5,
        min_request_interval: float = 0.5,
        user_agent: str = "BiodiversityGuardianAI/1.0 (Hackathon Conservation Telemetry)",
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.min_request_interval = min_request_interval
        self._last_request_time: float = 0.0

        headers = {
            "User-Agent": user_agent,
            "Accept": "application/json",
        }
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=headers,
            follow_redirects=True,
        )

    def _wait_for_rate_limit(self) -> None:
        """Throttle requests to respect upstream rate limits."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.min_request_interval:
            sleep_time = self.min_request_interval - elapsed
            time.sleep(sleep_time)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform a GET request with automatic retry and rate-limiting."""
        retries = 0
        last_exception = None

        while retries <= self.max_retries:
            self._wait_for_rate_limit()
            try:
                self._last_request_time = time.time()
                response = self.client.get(endpoint, params=params)

                if response.status_code == 429:
                    wait_time = self.backoff_factor ** (retries + 1)
                    retry_after = response.headers.get("Retry-After")
                    if retry_after and retry_after.isdigit():
                        wait_time = max(wait_time, float(retry_after))
                    logger.warning(
                        f"Rate limit 429 from {endpoint}. Retrying in {wait_time:.1f}s (attempt {retries + 1}/{self.max_retries})"
                    )
                    time.sleep(wait_time)
                    retries += 1
                    continue

                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                if 500 <= status_code < 600:
                    wait_time = self.backoff_factor ** (retries + 1)
                    logger.warning(
                        f"Server error {status_code} from {endpoint}. Retrying in {wait_time:.1f}s (attempt {retries + 1}/{self.max_retries})"
                    )
                    time.sleep(wait_time)
                    retries += 1
                    last_exception = e
                    continue
                logger.error(f"HTTP error {status_code} from {endpoint}: {e.response.text}")
                raise APIClientError(f"HTTP request failed [{status_code}]: {e}") from e

            except (httpx.TimeoutException, httpx.NetworkError) as e:
                wait_time = self.backoff_factor ** (retries + 1)
                logger.warning(
                    f"Network or timeout error on {endpoint}: {e}. Retrying in {wait_time:.1f}s (attempt {retries + 1}/{self.max_retries})"
                )
                time.sleep(wait_time)
                retries += 1
                last_exception = e

        raise APIClientError(
            f"Failed to fetch from {endpoint} after {self.max_retries} retries: {last_exception}"
        ) from last_exception

    def close(self) -> None:
        """Close the underlying HTTP client session."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
