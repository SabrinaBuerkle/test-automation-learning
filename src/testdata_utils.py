

def filter_failed_tests(testcases: list[dict]) -> list[dict]:
    return [testcase for testcase in testcases if testcase.get("status")=="failed"]
    
    
def average_duration(testcases: list[dict]) -> float:

    if testcases == []:
        raise ValueError("Cannot calculate average duration with empty testcases list")
    
    sum_duration = 0
    
    for testcase in testcases:
        sum_duration = sum_duration + testcase["duration"]

    average_duration = sum_duration / len(testcases)
    
    return average_duration


def validate_testcases(testcases: list[dict]) -> None:
    keys = ["id", "name", "status", "duration"]
    
    for testcase in testcases:
        for key in keys:
            try:
                testcase[key]
            except:
                if testcase.get("name") != None:
                    raise ValueError("Key " + key + " doesn´t exist in testcase " + testcase.get("name"))
                elif testcase.get("id") != None:
                    raise ValueError("Key " + key + " doesn´t exist in testcase " + str(testcase.get("id")))
                else:
                    raise ValueError("Key " + key + " doesn´t exist in one of the testcases in the given list")
                

    
