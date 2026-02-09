import requests
import pytest

import tests.helpers.validators as val
import tests.helpers.actions as act
from tests.helpers.logger import get_logger

from src.posts_client import PostsClient


logger = get_logger(__name__)

pytestmark = [
    pytest.mark.api,
    pytest.mark.unit,
]


## Positive tests ##
@pytest.mark.smoke
def test_create_PostsClient_success(base_url, timeout):

    client = PostsClient(base_url, timeout=timeout, max_retries=3)

    val.assert_client_attributes(client, base_url=base_url, timeout=timeout, max_retries=3)


def test_get_post_list_success(mocker, mocked_post_list_get, base_url, timeout):

    mock_response = mocked_post_list_get()
    mock_get = mocker.patch("requests.get", return_value = mock_response)

    client = PostsClient(base_url, timeout=timeout)
    response = client.get_post_list()
    data = act.get_json_data_from_response(response)
    
    val.assert_valid_post_list(data)
    mock_get.assert_called_once_with(f"{base_url}/posts", timeout=timeout)

@pytest.mark.smoke
def test_get_post_by_id_success(mocker, mocked_positive_response_get, base_url, timeout, expected_post_keys):
    
    mock_response = mocked_positive_response_get()
    mock_get = mocker.patch("requests.get", return_value = mock_response)

    client = PostsClient(base_url, timeout=timeout)
    response = client.get_post_by_id(1)
    post = act.get_json_data_from_response(response)
    
    val.assert_valid_post(post, expected_post_keys, 1)
    mock_get.assert_called_once_with(f"{base_url}/posts/1", timeout=timeout)




## Test of error behaviour ##

def test_get_post_by_id_not_found(mocker, mocked_NotFoundError_get, base_url, timeout):

    mock_response_not_found_error = mocked_NotFoundError_get()    
    mock_get = mocker.patch("requests.get", return_value = mock_response_not_found_error)
    
    client = PostsClient(base_url, timeout=timeout, max_retries=1)

    val.assert_get_post_by_id_NotFoundError(client)
    mock_get.assert_called_once_with(f"{base_url}/posts/99999", timeout=timeout)


def test_get_post_by_id_invalid_json_data(mocker, mocked_InvalidResponse_get, base_url, timeout):

    mock_response_value_error = mocked_InvalidResponse_get()    
    mock_get = mocker.patch("requests.get", return_value = mock_response_value_error)
    
    client = PostsClient(base_url, timeout=timeout, max_retries=1)

    val.assert_get_post_by_id_InvalidResponseError(client)        
    mock_get.assert_called_once_with(f"{base_url}/posts/1", timeout=timeout)


@pytest.mark.parametrize(
        ("error_response", "error_text"), [
        (requests.exceptions.Timeout, "Request failed after 1 retries: Timeout"), 
        (requests.exceptions.ConnectionError, "Request failed after 1 retries: ConnectionError")])

def test_get_post_by_id_RetryableError(mocker, base_url, timeout, error_response, error_text):

    mock_get = mocker.patch("requests.get", side_effect=error_response)
    logger.info("Creating fake response with %s", error_response)

    client = PostsClient(base_url, timeout=timeout, max_retries=1)

    val.assert_get_post_by_id_RetryableError(client, error_text)


def test_get_post_by_id_ServerError(mocker, mocked_ServerError_get, base_url, timeout):

    response_server_error = mocked_ServerError_get()
    mock_get = mocker.patch("requests.get", return_value =  response_server_error)

    client = PostsClient(base_url, timeout=timeout, max_retries=1)

    val.assert_get_post_by_id_RetryableError(client, "ServerError")


def test_get_post_by_id_invalid_post_schema(mocker, mocked_invalid_post_get, base_url, timeout):

    response_invalid_post = mocked_invalid_post_get()
    mock_get = mocker.patch("requests.get", return_value = response_invalid_post)

    client = PostsClient(base_url, timeout=timeout, max_retries=1)

    val.assert_get_post_by_id_InvalidSchemaError(client)


def test_get_post_list_invalid_post_schema(mocker, mocked_invalid_post_list_get, base_url, timeout):

    response_invalid_post_list = mocked_invalid_post_list_get()
    mock_get = mocker.patch("requests.get", return_value = response_invalid_post_list)

    client = PostsClient(base_url, timeout=timeout, max_retries=1)

    val.assert_get_post_list_InvalidSchemaError(client)


    



## Test of retry logic ##

@pytest.mark.parametrize("error_response", [requests.exceptions.Timeout, requests.exceptions.ConnectionError])

def test_get_post_by_id_retries_after_TimeoutError_and_ConnectionError_and_succeeds(mocker, mocked_positive_response_get, base_url, timeout, error_response):
    mock_response = mocked_positive_response_get()

    mock_get = mocker.patch("requests.get",
        side_effect = [error_response, error_response, mock_response]
    )
    logger.info("Mocking requests.get with two unsuccessful tries and third try successful")

    client = PostsClient(base_url, timeout=timeout, max_retries=3)
    response = client.get_post_by_id(1)

    val.assert_successful_connection(response)
    assert mock_get.call_count == 3


@pytest.mark.parametrize(
        ("error_response", "error_text"), [
        (requests.exceptions.Timeout, "Request failed after 3 retries: Timeout"), 
        (requests.exceptions.ConnectionError, "Request failed after 3 retries: ConnectionError")])

def test_get_post_by_id_retries_after_TimeoutError_and_ConnectionError_and_fails(mocker, base_url, timeout, error_response, error_text):

    mock_get = mocker.patch("requests.get", side_effect = error_response)
    logger.info("Creating fake response with %s", error_response)

    client = PostsClient(base_url, timeout, max_retries=3)

    val.assert_get_post_by_id_RetryableError(client, error_text)
    assert mock_get.call_count == 3


def test_get_post_by_id_retries_after_ServerError_and_succeeds(mocker, mocked_positive_response_get, mocked_ServerError_get, timeout, base_url):
    
    mock_response_successfull = mocked_positive_response_get()
    mock_response_server_error = mocked_ServerError_get()
    
    mock_get = mocker.patch("requests.get",
        side_effect = [mock_response_server_error, mock_response_server_error, mock_response_successfull]
    )
    logger.info("Mocking requests.get with two unsuccessful tries and third try successful")

    client = PostsClient(base_url, timeout=timeout, max_retries=3)
    response = client.get_post_by_id(1)

    val.assert_successful_connection(response)
    assert mock_get.call_count == 3


def test_get_post_by_id_retries_after_ServerError_and_fails(mocker, mocked_ServerError_get, base_url, timeout):
    
    mock_response_server_error = mocked_ServerError_get()    
    mock_get = mocker.patch("requests.get", return_value = mock_response_server_error)

    client = PostsClient(base_url, timeout=timeout, max_retries=3)

    val.assert_get_post_by_id_RetryableError(client, error_text="ServerError")
    assert mock_get.call_count == 3


def test_get_post_by_id_doesnt_retry_after_NotFoundError(mocker, mocked_NotFoundError_get, base_url, timeout):
    
    mock_response_not_found_error = mocked_NotFoundError_get()    
    mock_get = mocker.patch("requests.get", return_value = mock_response_not_found_error)

    client = PostsClient(base_url, timeout=timeout, max_retries=3)

    val.assert_get_post_by_id_NotFoundError(client)
    assert mock_get.call_count == 1


def test_get_post_by_id_doesnt_retry_after_InvalidResponseError(mocker, mocked_InvalidResponse_get, base_url, timeout):

    mock_response_value_error = mocked_InvalidResponse_get()    
    mock_get = mocker.patch("requests.get", return_value = mock_response_value_error)
    
    client = PostsClient(base_url, timeout=timeout, max_retries=3)

    val.assert_get_post_by_id_InvalidResponseError(client)        
    assert mock_get.call_count == 1