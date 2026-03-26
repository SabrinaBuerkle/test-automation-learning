import requests
from pydantic import ValidationError

from tests.helpers.logger import get_logger
from src.http_client import HttpClient
from src.models import Post
from src.exceptions import InvalidSchemaError

logger = get_logger(__name__)

class PostsClient:
    def __init__(self, http_client: HttpClient):

        self.http = http_client    


    def get_post_list(self) -> requests.Response:

        logger.info("Getting post list...")
        response = self.http.get("posts")

        try:            
            return [Post.model_validate(post) for post in response.json()]
        
        except ValidationError as exc:
            logger.warning("Invalid post schema found in post list")
            raise InvalidSchemaError("Invalid post schema found in post list") from exc
        

    def get_post_by_id(self, post_id: int) -> Post:
    
        logger.info("Getting post with id %i", post_id)
        response = self.http.get(f"posts/{post_id}")

        try:
            return Post.model_validate(response.json())
        except ValidationError as exc:
            logger.warning("Invalid post schema")
            raise InvalidSchemaError("Invalid post schema") from exc
        
        
