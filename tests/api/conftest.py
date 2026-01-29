import requests
import pytest

@pytest.fixture(scope="session")
def base_url():
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture
def expected_post_keys():
    return {"userId", "id", "title", "body"}

@pytest.fixture
def fake_requests_get(mocker):
    def _fake_get(url, timeout):
        mock_response = mocker.Mock()

        if url.endswith("/posts/1"):
            mock_response.status_code = 200
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.json.return_value = {
                "userId": 1,
                "id": 1,
                "title": "Mocked title",
                "body": "Mocked body"
            }
        else:
            mock_response.status_code = 404
            mock_response.headers = {}
            mock_response.json.side_effect = ValueError("No JSON")
    
        return mock_response
    return _fake_get

# @pytest.fixture
# def fake_timeout(mocker):
#     def _timeout_get(url):
#         mock_response = mocker.Mock()


