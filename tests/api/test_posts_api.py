import requests

def test_get_posts_returns_status_code_200():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    assert response.status_code == 200

def test_get_posts_returns_list_of_posts():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_post_has_expected_fields():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    post = response.json()[0]
    assert "userId" in post
    assert "id" in post
    assert "title" in post
    assert "body" in post

def test_get_post_id1_returns_status_code_200():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    assert response.status_code == 200

def test_get_post_id99999_not_existing():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/99999")
    assert response.status_code == 404