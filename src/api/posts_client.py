import requests

class PostsClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")


    def _get(self, url: str) -> requests.Response:
        try:
            response = requests.get(url, timeout=5)
            return response
        
        except requests.exceptions.Timeout:
            raise RuntimeError("Request timed out")
        
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Connection failed")
        

    def get_post_list(self) -> requests.Response:

        response = self._get(f"{self.base_url}/posts")

        if response.status_code == 404:
            raise ValueError(f"Post list in requested URL not found")
        
        if not response.headers.get("Content-Type", "").startswith("application/json"):
            raise TypeError("Response is not JSON")
        
        return response


    def get_post_by_id(self, post_id: int) -> requests.Response:
        
        response = self._get(f"{self.base_url}/posts/{post_id}")
                 
        if response.status_code == 404:
            raise ValueError(f"Post with id {post_id} not found")

        response.raise_for_status()

        if not response.headers.get("Content-Type", "").startswith("application/json"):
            raise TypeError("Response is not JSON")

        return response