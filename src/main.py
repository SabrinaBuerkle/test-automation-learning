from src.testdata_utils import (
    filter_failed_tests,
    average_duration,
    validate_testcases,
)
from data.testcases import testcases0, testcases1, testcases2

def main(testcases):
    failed_tests = filter_failed_tests(testcases)
    print("Failed testcases: ")
    print([test.get("name") for test in failed_tests])

    avg_duration = average_duration(testcases)
    print("Average duration: " + str(avg_duration))

    validate_testcases(testcases)

if __name__ == "__main__":
    main(testcases0)
    #main(testcases1) # Empty list
    #main(testcases2) # Missing key for one testcase