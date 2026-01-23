import requests

def test_get_posts_returns_status_code_200():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    assert response.status_code == 200 # 200 = Successfull connection

def test_get_posts_returns_list_of_posts():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_post_has_expected_fields():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    post = response.json()[0]
    assert "userId" in post # int: ID of the user that made the post
    assert "id" in post # int: ID of the post
    assert "title" in post # str: title of the post
    assert "body" in post # str: body of the post

def test_get_post_by_id_returns_same_id():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    post = response.json()
    assert "userId" in post 
    assert post["id"] == 1 
    assert "title" in post 
    assert "body" in post 

def test_get_post_id99999_not_existing():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/99999")
    assert response.status_code == 404 # Requested rescourse not found