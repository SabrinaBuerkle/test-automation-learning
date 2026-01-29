import requests
import pytest

import tests.api.helpers.validators as val

from src.api.posts_client import PostsClient


def test_get_posts_list_returns_status_code_200(base_url):

    client = PostsClient(base_url)
    response = client.get_post_list()

    val.assert_successful_connection(response)


def test_get_posts_returns_list_of_posts(base_url):

    client = PostsClient(base_url)
    response = client.get_post_list()
    data = response.json()
    
    val.assert_valid_post_list(data)


def test_post_has_expected_fields(base_url, expected_post_keys):

    client = PostsClient(base_url)
    response = client.get_post_list()
    post = response.json()[0]
    
    val.assert_valid_post_fields(post, expected_post_keys)
    

@pytest.mark.parametrize(
    "post_id", [1,2,3,4,5,50,100], ids=lambda x: f"post_id={x}")

def test_get_post_by_id_returns_same_id(base_url, expected_post_keys, post_id):

    client = PostsClient(base_url)
    response = client.get_post_by_id(post_id)

    val.assert_successful_connection(response)

    val.assert_response_is_json(response)
    post = val.get_json_data_from_response(response)
    
    val.assert_valid_post(post, expected_post_keys, post_id)


def test_get_post_id99999_not_existing(base_url):

    client = PostsClient(base_url)

    with pytest.raises(ValueError, match = "not found"):
        client.get_post_by_id(99999)








