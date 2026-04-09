# API Test Automation Learning Project #

## Overview ##

This project is a hands-on learning project for building a clean and maintainable API test automation framework in Python.

It covers:

- API testing with pytest
- Test design (positive & negative cases)
- Fixtures and parametrization
- Mocking with pytest-mock
- Custom API client implementation
- Error handling and retry logic
- Schema validation

The project uses the public API:
https://jsonplaceholder.typicode.com


## Project Structure ##
```
project_root/
│
├── src/
│   ├── api/
│   │   ├── posts_client.py     # API client (business logic)
│   │   ├── http_client.py      # HTTP layer (requests, retry, errors)
│   │   ├── validators.py       # Assertion helpers
│   │   └── models.py           # Data models (e.g. Post)
│   │
├── tests/
│   ├── api/
│   │   ├── unit/               # Unit tests (mocked)
│   │   └── integration/        # Real API tests
│   │
│   └── conftest.py             # Shared fixtures
│
├── requirements.txt
└── README.md
```


## Setup ##

### 1. Create virtual environment ###
``` 
python -m venv .venv
```

### 2. Activate environment ###
Windows: 
``` 
.venv\Scripts\activate
```
Linux / Mac: 
``` 
source .venv/bin/activate
```

### 3. Install dependencies ###
``` 
pip install -r requirements.txt
```

### 4. Running Tests ###
Run all tests:       
``` 
pytest -v
```

Run only unit tests: 
``` 
pytest tests/api/unit -v
```

Run specific file:   
``` 
pytest tests/api/unit/test_posts_client.py -v
```

### 5. Debugging ###
Run with output:  
``` 
pytest -s
```
Use debugger:    
``` 
import pdb; pdb.set_trace()
```


## Learning Goals ##

This project is designed to build skills in:

- Writing clean and maintainable tests
- Structuring test automation frameworks
- Understanding API client design
- Applying mocking and isolation techniques
- Handling real-world API edge cases


## Next Steps ##

- Add contract testing
- Introduce schema validation with Pydantic
- Extend to UI testing (e.g. Playwright)
- CI integration (GitHub Actions)
  
