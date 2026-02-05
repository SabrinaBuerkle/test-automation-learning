from tests.helpers.logger import get_logger

logger = get_logger(__name__)


def get_json_data_from_response(response):
    data = response.json() # if response is not in valid json format test fails at this point
    return data

