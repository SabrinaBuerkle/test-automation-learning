import pytest
import pdb
from src.testdata_utils import filter_failed_tests, average_duration, validate_testcases


### Tests for filter_failed_tests ###
# Input list with mixed results --> Function should return only failed tests
def test_filter_failed_tests_with_mixed_results_returns_only_failed_testcases(valid_testcases_mixed_result):
    result = filter_failed_tests(valid_testcases_mixed_result)
    assert len(result) == 1
    assert all([res.get("status") == "failed" for res in result])

# Input list with only passed results --> Function should return empty list
def test_filter_failed_tests_with_only_passed_results_returns_empty_list(valid_testcases_passed):
    result = filter_failed_tests(valid_testcases_passed)
    assert result == []

# Input empty list --> Function should return empty list
def test_filter_failed_tests_with_empty_list_returns_empty_list(empty_testcase_list):
    result = filter_failed_tests(empty_testcase_list)
    assert result == []


### Tests for average_duration ###
# Input multiple testcases --> Function should return average duration of the testcases
def test_average_duration_with_multiple_testcases_returns_average(valid_testcases_mixed_result):
    result = average_duration(valid_testcases_mixed_result)
    assert result == 2.0

# Input list with only one testcase --> Function should return duration of testcase
def test_average_duration_with_one_testcase_returns_duration(valid_testcases_one):
    result = average_duration(valid_testcases_one)
    assert result == 1.0

# Input empty list --> Function should raise ValueError
def test_average_duration_with_empty_list_raises_value_error(empty_testcase_list):
    with pytest.raises(ValueError):
        average_duration(empty_testcase_list)


### Tests for validate_testcases ###
# Input valid testcases --> No exception
def test_validate_testcases_with_only_valid_testcases_provokes_no_exception(valid_testcases_mixed_result):
    validate_testcases(valid_testcases_mixed_result)

# Input list of invalid testcases with one missing key --> Value exception
def test_validate_testcases_only_invalid_testcases_raises_value_error(invalid_testcases):
    with pytest.raises(ValueError):
        validate_testcases(invalid_testcases)

# Input list of valid testcases with one invalid testcase (different input parameters for different keys missing) --> Value exception
@pytest.mark.parametrize(
"invalid_testcase_one_key_missing",
[
    {"name": "A", "status": "passed", "duration": 1.0},          # id missing
    {"id": 1, "status": "passed", "duration": 1.0},              # name missing
    {"id": 1, "name": "A", "duration": 1.0},                     # status missing
    {"id": 1, "name": "A", "status": "passed"},                  # duration missing
])

def test_validate_testcases_with_one_invalid_testcase_raises_value_error(invalid_testcase_one_key_missing, valid_testcases_mixed_result):
    testcase = [
        valid_testcases_mixed_result[0],
        invalid_testcase_one_key_missing,
        valid_testcases_mixed_result[1],
    ]
    with pytest.raises(ValueError):
        validate_testcases(testcase)
