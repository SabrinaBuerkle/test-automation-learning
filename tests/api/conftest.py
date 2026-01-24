import requests
import pytest

@pytest.fixture(scope="session")
def base_url():
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture
def get_post_by_id(base_url):
    def _get_post(post_id: int):
        return requests.get(f"{base_url}\posts\{post_id}")
    return _get_post

