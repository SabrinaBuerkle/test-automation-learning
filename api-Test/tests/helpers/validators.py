import pytest
from tests.helpers.logger import get_logger

logger = get_logger(__name__)

def assert_client_attributes(client, base_url, timeout, max_retries) -> None:
    assert client.base_url == base_url
    assert client.timeout == timeout
    assert client.max_retries == max_retries
    logger.info("Passed: Client object contains all the expected attributes")

def assert_successful_connection(response) -> None:
    assert response.ok, f"Connection not successful, response code: {response.status}" # 200 = Successfull connection
    logger.info("Passed: Connection was successful")

def assert_response_is_json(response):
    assert response.headers["Content-Type"].startswith("application/json"), "Response header does not start with application/json"
    logger.info("Passed: Response contains json data")

def assert_valid_post_list(data: list) -> None:
    assert isinstance(data, list), "Error: Post data is not a list"
    assert len(data) > 0, "Error, post list is empty"
    logger.info("Passed: Response contains a valid post list")

def assert_valid_post(post: dict, expected_post_keys: set, expected_id: int) -> None:
    assert set(post.keys()) == expected_post_keys, "Post eiter does not contain all of the expected keys or contains more keys" # post contains exeactly the expected keys, not more not less
    #assert expected_keys.issubset(post.keys()) # post contains the expected keys but can contain other keys as well

    assert post["id"] == expected_id, f"Wrong post id: expected {expected_id}, got {post['id']}"
    assert post["title"], "Post title is empty" # String not empty
    assert post["body"], "Post body is empty" # String not empty
    logger.info("Passed: Post id is correct and post keys are not empty")

def assert_valid_post_fields(post: dict, expected_post_keys: set) -> None:
    assert expected_post_keys.issubset(post.keys()), "Post does not contain all of the expected keys"
    logger.info("Passed: Post contains all of the expected keys")

def assert_not_found_error(client) -> None:
    with pytest.raises(ValueError, match="not found"):
        client.get_post_by_id(1)
    logger.info("Passed: Not found error was raised correctly")

def assert_type_error(client) -> None:
    with pytest.raises(TypeError):
        client.get_post_by_id(1)
    logger.info("Passed: TypeError was raised correctly")

def assert_server_error(client) -> None:
    with pytest.raises(RuntimeError, match = "Server error"):
        client.get_post_by_id(1)
    logger.info("Passed: Server error was detected correctly")

def assert_runtime_error(client, max_retries) -> None:
    match_str = f"failed after {max_retries} retries"
    with pytest.raises(RuntimeError, match = match_str):
        client.get_post_by_id(1)
    logger.info("Passed: Runtime error was raised correctly")





