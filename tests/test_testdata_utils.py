import pytest
from src.testdata_utils import filter_failed_tests, average_duration, validate_testcases

### Tests for filter_failed_tests ###
# Input list with mixed results --> Function should return only failed tests
def test_filter_failed_tests_with_mixed_results_returns_only_failed_testcases():
    testcases = [
        {"id": 1, "name": "A", "status": "passed", "duration": 1.0},
        {"id": 2, "name": "B", "status": "failed", "duration": 3.0},
    ]
    result = filter_failed_tests(testcases)
    assert result == [{"id": 2, "name": "B", "status": "failed", "duration": 3.0}]

# Input list with only passed results --> Function should return empty list
def test_filter_failed_tests_with_only_passed_results_returns_empty_list():
    testcases = [
        {"id": 1, "name": "A", "status": "passed", "duration": 1.0},
        {"id": 2, "name": "B", "status": "passed", "duration": 3.0},
    ]
    result = filter_failed_tests(testcases)
    assert result == []

# Input empty list --> Function should return empty list
def test_filter_failed_tests_with_empty_list_returns_empty_list():
    testcases = []
    result = filter_failed_tests(testcases)
    assert result == []


### Tests for average_duration ###
# Input multiple testcases --> Function should return average duration of the testcases
def test_average_duration_with_multiple_testcases_returns_average():
    testcases = [
        {"id": 1, "name": "A", "status": "passed", "duration": 1.0},
        {"id": 2, "name": "B", "status": "failed", "duration": 3.0},
    ]
    result = average_duration(testcases)
    assert result == 2.0

# Input list with only one testcase --> Function should return duration of testcase
def test_average_duration_with_one_testcase_returns_duration():
    testcases = [
        {"id": 1, "name": "A", "status": "passed", "duration": 1.0},
        ]
    result = average_duration(testcases)
    assert result == 1.0

# Input empty list --> Function should raise ValueError
def test_average_duration_with_empty_list_raises_value_error():
    with pytest.raises(ValueError):
        average_duration([])


### Tests for validate_testcases ###
# Input valid testcases --> No exception
def test_validate_testcases_with_only_valid_testcases_provokes_no_exception():
    testcases = [
        {"id": 1, "name": "A", "status": "passed", "duration": 1.0},
        {"id": 2, "name": "B", "status": "failed", "duration": 3.0},
    ]
    validate_testcases(testcases)

# Input list of invalid testcases with one missing key --> Value exception
def test_validate_testcases_only_invalid_testcases_raises_value_error():
    testcases = [
        {"id": 1, "name": "A", "status": "passed"},
        {"name": "B", "status": "failed", "duration": 3.0},
    ]
    with pytest.raises(ValueError):
        validate_testcases(testcases)

# Input list of valid testcases with one invalid testcase (different input parameters for different keys missing) --> Value exception
@pytest.mark.parametrize(
    "invalid_testcase",
    [
        {"name": "A", "status": "passed", "duration": 1.0},          # id missing
        {"id": 1, "status": "passed", "duration": 1.0},              # name missing
        {"id": 1, "name": "A", "duration": 1.0},                     # status missing
        {"id": 1, "name": "A", "status": "passed"},                  # duration missing
    ])

def test_validate_testcases_with_one_invalid_testcase_raises_value_error(invalid_testcase):
    testcases = [
        {"id": 1, "name": "A", "status": "passed", "duration": 1.0},
        invalid_testcase,
        {"id": 2, "name": "B", "status": "failed", "duration": 3.0},
    ]
    with pytest.raises(ValueError):
        validate_testcases(testcases)
