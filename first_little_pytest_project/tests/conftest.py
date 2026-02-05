import pytest

@pytest.fixture
def valid_testcases_mixed_result():
    return [
        {"id": 1, "name": "A", "status": "passed", "duration": 1.0},
        {"id": 2, "name": "B", "status": "failed", "duration": 3.0},
    ]

@pytest.fixture
def valid_testcases_passed():
    return [
        {"id": 1, "name": "A", "status": "passed", "duration": 1.0},
        {"id": 2, "name": "B", "status": "passed", "duration": 3.0},
    ]

@pytest.fixture
def valid_testcases_one():
    return [
        {"id": 1, "name": "A", "status": "passed", "duration": 1.0},
    ]

@pytest.fixture
def invalid_testcases():
    return [
        {"id": 1, "name": "A", "status": "passed"},
        {"name": "B", "status": "failed", "duration": 3.0},
    ]

@pytest.fixture
def empty_testcase_list():
    return []
