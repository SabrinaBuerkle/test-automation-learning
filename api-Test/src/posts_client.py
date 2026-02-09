import requests
from pydantic import ValidationError

from tests.helpers.logger import get_logger
from src.models import Post
from src.exceptions import NotFoundError, InvalidResponseError, InvalidSchemaError, RetryableError, ServerError

logger = get_logger(__name__)

class PostsClient:
    def __init__(self, base_url: str, timeout: int = 5, max_retries: int = 1):

        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.timeout = timeout


    def _get(self, url: str) -> requests.Response:

        last_exception = None
        attempt = 0

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

                return response

            except(requests.exceptions.Timeout, requests.exceptions.ConnectionError, ServerError) as exc:
                last_exception = exc
                logger.warning("Attempt %i failed (%s): %s", attempt, type(exc).__name__, exc)

        raise RetryableError(f"Request failed after {attempt} retries: {type(last_exception).__name__}") from last_exception



    def get_post_list(self) -> requests.Response:

        logger.info("Getting post list...")
        response = self._get(f"{self.base_url}/posts")

        try:
            for post in response.json():
                Post.model_validate(post)
        
        except ValidationError as exc:
            logger.warning("Invalid post schema found in post list")
            raise InvalidSchemaError("Invalid post schema found in post list") from exc
        
        return response




    def get_post_by_id(self, post_id: int) -> requests.Response:

    
        logger.info("Getting post with id %i", post_id)
        response = self._get(f"{self.base_url}/posts/{post_id}")

        try:
            Post.model_validate(response.json())
        except ValidationError as exc:
            logger.warning("Invalid post schema")
            raise InvalidSchemaError("Invalid post schema") from exc
        
        return response
        
