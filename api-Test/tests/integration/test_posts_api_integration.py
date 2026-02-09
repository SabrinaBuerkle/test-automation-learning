import pytest

import tests.helpers.validators as val
import tests.helpers.actions as act
from tests.helpers.logger import get_logger

from src.posts_client import PostsClient


logger = get_logger(__name__)

pytestmark = pytest.mark.api
pytestmark = pytest.mark.integration


def test_get_posts_list_returns_status_code_200(base_url, timeout):

    client = PostsClient(base_url, timeout)
    response = client.get_post_list()

    val.assert_successful_connection(response)


def test_get_posts_returns_list_of_posts(base_url, timeout):

    client = PostsClient(base_url, timeout)
    response = client.get_post_list()
    data = act.get_json_data_from_response(response)
    
    val.assert_valid_post_list(data)


@pytest.mark.parametrize(
    "post_id", [1,2,3,4,5,50,100], ids=lambda x: f"post_id={x}")

def test_get_post_by_id_returns_same_id(base_url, timeout, post_id):

    client = PostsClient(base_url, timeout)
    response = client.get_post_by_id(post_id)    
    post = act.get_json_data_from_response(response)
    
    assert post["id"] == post_id, f"Post id not correct, expected {post_id}, got {post['id']}."


@pytest.mark.parametrize(
    "post_id", [1,2,3,4,5,50,100], ids=lambda x: f"post_id={x}")

def test_get_post_by_id_returns_valid_post_object(base_url, timeout, expected_post_keys, post_id):

    client = PostsClient(base_url, timeout)    
    response = client.get_post_by_id(post_id)
    post = act.get_json_data_from_response(response)

    val.assert_valid_post(post, expected_post_keys, post_id)


def test_get_post_id99999_not_existing(base_url, timeout):

    client = PostsClient(base_url, timeout)

    val.assert_get_post_by_id_NotFoundError(client)








