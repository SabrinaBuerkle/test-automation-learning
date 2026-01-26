import requests
import pytest
import mock

import src.api.validators as val


def test_get_posts_returns_status_code_200(base_url):

    response = requests.get(f"{base_url}/posts")

    val.assert_successful_connection(response)


def test_get_posts_returns_list_of_posts(base_url):

    response = requests.get(f"{base_url}/posts")
    data = response.json()
    
    val.assert_valid_post_list(data)


def test_post_has_expected_fields(base_url, expected_post_keys):

    response = requests.get(f"{base_url}/posts")
    post = response.json()[0]
    
    val.assert_valid_post_fields(post, expected_post_keys)
    

@pytest.mark.parametrize(
    "post_id", [1,2,3,4,5,50,100], ids=lambda x: f"post_id={x}")

def test_get_post_by_id_returns_same_id(get_post_by_id, post_id, expected_post_keys):

    response = get_post_by_id(post_id)

    val.assert_successful_connection(response)

    val.assert_response_is_json(response)
    post = val.get_json_data_from_response(response)
    
    val.assert_valid_post(post, expected_post_keys, post_id)


def test_get_post_id99999_not_existing(get_post_by_id):

    response = get_post_by_id(99999)

    val.assert_resource_not_found(response)





fake_post = {
    "userID": 1,
    "id": 1,
    "title": "Mocked title",
    "body": "Mocked body"
}

mock_response = mock.Mock()
mock_response.status_code = 200
mock_response.headers = {"Content-Type": "application/json"}
mock_response.json.return_value = fake_post

mock.patch(
    "requests.get",
    return_value = mock_response
)

def test_get_post_by_id_mocked(mocker, get_post_by_id, expected_post_keys, base_url):
    response = requests.get(f"{base_url}/posts/1")
    post = val.get_json_data_from_response(response)
        
    val.assert_valid_post_fields(post, expected_post_keys)