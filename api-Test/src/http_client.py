import requests

from tests.helpers.logger import get_logger
from src.http_response import HttpResponse
from src.exceptions import NotFoundError, InvalidResponseError, RetryableError, ServerError

logger = get_logger(__name__)

class HttpClient:
    def __init__(self, base_url: str, timeout: int = 5, max_retries: int = 1):

        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.timeout = timeout


    def get(self, path: str) -> HttpResponse:

        url = f"{self.base_url}/{path.lstrip('/')}" 
        last_exception = None
        
        for attempt in range(1, self.max_retries+1):
            try:
                logger.info("Requesting url %s: attempt %i", url, attempt)
                response = requests.get(url, timeout=self.timeout)

                if response.status_code == 404:
                    raise NotFoundError(f"Post list or post ID with requested URL {url} not found")

                if 500 <= response.status_code < 600:
                    raise ServerError(f"Server error: {response.status_code}")

                response.raise_for_status()

                if not response.headers.get("Content-Type", "").startswith("application/json"):
                    raise InvalidResponseError("Response is not JSON")

                return HttpResponse(response)

            except(requests.exceptions.Timeout, requests.exceptions.ConnectionError, ServerError) as exc:
                last_exception = exc
                logger.warning("Attempt %i failed (%s): %s", attempt, type(exc).__name__, exc)

        raise RetryableError(f"Request failed after {attempt} retries: {type(last_exception).__name__}") from last_exception