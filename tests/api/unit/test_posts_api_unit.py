import requests
import pytest

import tests.api.helpers.validators as val
import tests.api.helpers.actions as act

from src.api.posts_client import PostsClient

import pdb


def test_get_post_by_id_success(mocker, base_url, expected_post_keys):
    fake_post = {
        "userId": 1,
        "id": 1,
        "title": "Mocked title",
        "body": "Mocked body"
    }

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = fake_post

    mocker.patch("requests.get", return_value = mock_response)

    client = PostsClient(base_url)
    response = client.get_post_by_id(1)

    post = response.json()
    
    #val.assert_valid_post_fields(post, expected_post_keys)
    val.assert_valid_post(post, expected_post_keys, 1)

    requests.get.assert_called_once_with(f"{base_url}/posts/1", timeout=5)


def test_get_post_by_id_not_found(mocker, base_url):

    mock_response = mocker.Mock()
    mock_response.status_code = 404
       
    mocker.patch("requests.get", return_value = mock_response)

    client = PostsClient(base_url)
    
    with pytest.raises(ValueError, match = "not found"):
        client.get_post_by_id(99999)

    requests.get.assert_called_once_with(f"{base_url}/posts/99999", timeout=5)


@pytest.mark.parametrize("post_id, expected_status", [(1, 200), (99999, 404)], ids=["post_id=1, expected_status=200", "post_id=99999, expected_status=404"]) #ids = lambda param: f"post_id = {param[0]}, expected_status = {param[1]}")

def test_get_post_by_id_mocked_with_side_effect(mocker, base_url, expected_post_keys, fake_requests_get, post_id, expected_status):
    
    mocker.patch("requests.get", side_effect=fake_requests_get)

    client = PostsClient(base_url)
    
    if expected_status == 200:

        response = client.get_post_by_id(post_id)
        post = act.get_json_data_from_response(response)

        val.assert_successful_connection(response)
        val.assert_valid_post(post, expected_post_keys, post_id)

    elif expected_status == 404:
        with pytest.raises(ValueError, match = "not found"):
            client.get_post_by_id(post_id)

    
    requests.get.assert_called_once_with(f"{base_url}/posts/{post_id}", timeout=5)


@pytest.mark.parametrize("error_response, error_text", [(requests.exceptions.Timeout, "timed out"), (requests.exceptions.ConnectionError, "Connection failed")])

def test_get_post_by_id_timeout(mocker, base_url, error_response, error_text):

    mocker.patch("requests.get", side_effect=error_response)

    client = PostsClient(base_url)

    with pytest.raises(RuntimeError, match = error_text):
        client.get_post_by_id(1)


