import pytest

from tests.helpers.logger import get_logger

from src.exceptions import NotFoundError, InvalidResponseError, InvalidSchemaError, RetryableError, ServerError

logger = get_logger(__name__)

def assert_client_attributes(client, base_url, timeout, max_retries) -> None:
    assert client.base_url == base_url
    assert client.timeout == timeout
    assert client.max_retries == max_retries
    logger.info("Passed: Client object contains all the expected attributes")

def assert_successful_connection(response) -> None:
    assert response.ok, f"Connection not successful, response code: {response.status_code}" # 200 = Successfull connection
    logger.info("Passed: Connection was successful")

def assert_response_is_json(response):
    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith("application/json")
    logger.info("Passed: Response contains json data")

def assert_valid_post_list(data: list) -> None:
    assert isinstance(data, list), "Error: Post data is not a list"
    assert len(data) > 0, "Error, post list is empty"
    assert all(isinstance(post, dict) for post in data), "Error: Not all posts in the list are dictionaries"
    assert ["id" in post for post in data]
    logger.info("Passed: Response contains a valid post list")

def assert_valid_post(data, expected_post_keys: set, expected_id: int) -> None:
    assert expected_post_keys.issubset(data.keys()), "Post does not contain all of the expected keys"
    logger.info("Passed: Post contains all of the expected keys")

    assert data["id"] == expected_id, f"Wrong post id: expected {expected_id}, got {data['id']}"
    assert isinstance(data["userId"], int), "Invalid User Id"
    assert isinstance(data["title"], str), "Post title is not a string"
    assert data["title"], "Post title is empty"
    assert isinstance(data["body"], str), "Post body is not a string"
    assert data["body"], "Post body is empty"

    # assert post.id == expected_id, f"Wrong post id: expected {expected_id}, got {post.id}"
    # assert isinstance(post.userId, int), "Invalid User Id"
    # assert isinstance(post.title, str), "Post title is not a string"
    # assert post.title, "Post title is empty"
    # assert isinstance(post.body, str), "Post body is not a string"
    # assert post.body, "Post body is empty"

    logger.info("Passed: Post id is correct and post keys are not empty")

def assert_get_post_by_id_NotFoundError(client) -> None:
    with pytest.raises(NotFoundError, match="not found"):
        client.get_post_by_id(99999)
    logger.info("Passed: NotFoundError was raised correctly")

def assert_get_post_by_id_InvalidResponseError(client) -> None:
    with pytest.raises(InvalidResponseError):
        client.get_post_by_id(1)
    logger.info("Passed: InvalidResponseError was raised correctly")

def assert_get_post_by_id_RetryableError(client, error_text: str) -> None:
    with pytest.raises(RetryableError, match = error_text):
        client.get_post_by_id(1)
    logger.info("Passed: RetryableError was detected correctly")

def assert_get_post_by_id_InvalidSchemaError(client):
    with pytest.raises(InvalidSchemaError, match = "Invalid post schema"):
        client.get_post_by_id(1)
    logger.info("Passed: InvalidSchemaError error was raised correctly")

def assert_get_post_list_InvalidSchemaError(client):
    with pytest.raises(InvalidSchemaError, match = "Invalid post schema"):
        client.get_post_list()
    logger.info("Passed: InvalidSchemaError error was raised correctly")





