import requests

class HttpResponse:
    def __init__(self, response: requests.Response):
        self._response = response

    @property
    def status_code(self) -> int:
        return self._response.status_code
    
    @property
    def ok(self) -> int:
        return self._response.ok

    @property
    def headers(self) -> dict:
        return self._response.headers

    def json(self):
        return self._response.json()

    @property
    def text(self) -> str:
        return self._response.text