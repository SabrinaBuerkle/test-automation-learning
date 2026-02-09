
class ApiClientError(Exception):
    """Base exception for API client errors."""
    pass


class NotFoundError(ApiClientError):
    pass

class InvalidResponseError(ApiClientError):
    pass

class InvalidSchemaError(ApiClientError):
    pass

class ServerError(ApiClientError):
    pass

class RetryableError(ApiClientError):
    pass