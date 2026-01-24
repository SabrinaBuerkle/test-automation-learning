import requests
import json

def test_get_posts_returns_status_code_200(base_url):
    response = requests.get(base_url)
    assert response.status_code == 200 # 200 = Successfull connection

def test_get_posts_returns_list_of_posts(base_url):
    response = requests.get(base_url)
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_post_has_expected_fields(base_url):
    response = requests.get(base_url)
    post = response.json()[0]
    assert "userId" in post # int: ID of the user that made the post
    assert "id" in post # int: ID of the post
    assert "title" in post # str: title of the post
    assert "body" in post # str: body of the post

def test_get_post_by_id_returns_same_id(base_url):
    response = requests.get(base_url)

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    post = response.json() # if response is not in valid json format test fails at this point
    
    expected_keys = {"userId", "id", "title", "body"}
    assert set(post.keys()) == expected_keys # post contains exeactly the expected keys, not more not less
    #assert expected_keys.issubset(post.keys()) # post contains the expected keys but can contain other keys as well

    assert post["id"] == 1 
    assert post["title"] # String not empty
    assert post["body"] # String not empty


def test_get_post_id99999_not_existing():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/99999")
    assert response.status_code == 404 # Requested rescourse not found