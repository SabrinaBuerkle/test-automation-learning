
def assert_successful_connection(response) -> None:
    assert response.ok, f"Connection not successful, response code: {response.status}" # 200 = Successfull connection

def assert_response_is_json(response):
    assert response.headers["Content-Type"].startswith("application/json"), "Response header does not start with application/json"

def assert_valid_post_list(data: list) -> None:
    assert isinstance(data, list), "Error: Post data is not a list"
    assert len(data) > 0, "Error, post list is empty"

def assert_valid_post(post: dict, expected_post_keys: set, expected_id: int) -> None:
    assert set(post.keys()) == expected_post_keys, "Post eiter does not contain all of the expected keys or contains more keys" # post contains exeactly the expected keys, not more not less
    #assert expected_keys.issubset(post.keys()) # post contains the expected keys but can contain other keys as well

    assert post["id"] == expected_id, f"Wrong post id: expected {expected_id}, got {post['id']}"
    assert post["title"], "Post title is empty" # String not empty
    assert post["body"], "Post body is empty" # String not empty

def assert_valid_post_fields(post: dict, expected_post_keys: set) -> None:
    assert expected_post_keys.issubset(post.keys()), "Post does not contain all of the expected keys"




