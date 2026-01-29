

def get_json_data_from_response(response):
    data = response.json() # if response is not in valid json format test fails at this point
    return data

