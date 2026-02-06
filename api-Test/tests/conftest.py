import pytest
import yaml
from pathlib import Path

from tests.helpers.logger import setup_logging
from tests.helpers.logger import get_logger

logger = get_logger(__name__)

def pytest_configure():
    setup_logging()

## Basic configuration ##
@pytest.fixture(scope="session")
def config():
    config_path = Path(__file__).parent / "config" / "test.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def base_url(config):
    return config["base_url"]

@pytest.fixture(scope="session")
def timeout(config):
    return config["timeout"]


## Response structure ##

@pytest.fixture
def expected_post_keys():
    return {"userId", "id", "title", "body"}


## Mockers ##
@pytest.fixture
def mocked_post_list_get(mocker):
    def _fake_get(*args, **kwargs):
        logger.info("Creating fake posts list...")
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"userId": 1, "id": 1, "title": "Mocked title", "body": "Mocked body"},
            {"userId": 1, "id": 2, "title": "Mocked title 2", "body": "Mocked body 2"}]

        return mock_response
    return _fake_get

@pytest.fixture
def mocked_positive_response_get(mocker):
    def _fake_get(*args, **kwargs):
        logger.info("Creating fake positive response...")
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "userId": 1,
            "id": 1,
            "title": "Mocked title",
            "body": "Mocked body"}

        return mock_response
    return _fake_get

@pytest.fixture
def mocked_server_error_get(mocker):
    def _fake_get(*args, **kwargs):
        logger.info("Creating fake response with server error...")

        mock_response_server_error = mocker.Mock()
        mock_response_server_error.status_code = 501
        mock_response_server_error.headers = {"Content-Type": "application/json"}

        return mock_response_server_error
    return _fake_get

@pytest.fixture
def mocked_not_found_error_get(mocker):
    def _fake_get(*args, **kwargs):
        logger.info("Creating fake response with status code 404...")

        mock_response_not_found_error = mocker.Mock()
        mock_response_not_found_error.status_code = 404
        mock_response_not_found_error.headers = {"Content-Type": "application/json"}

        return mock_response_not_found_error
    return _fake_get


@pytest.fixture
def mocked_value_error_get(mocker):
    def _fake_get(*args, **kwargs):
        logger.info("Creating fake response with missing json data...")

        mock_response_value_error = mocker.Mock()
        mock_response_value_error.status_code = 200
        mock_response_value_error.headers = {}

        return mock_response_value_error
    return _fake_get




