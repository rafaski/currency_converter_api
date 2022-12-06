from fastapi import status
from enum import Enum


class ErrorTypes(str, Enum):
    """
    Enums for custom error types for exception handling
    """

    # APP errors
    UNKNOWN = "unknown"
    # API errors
    UNAUTHORIZED = "unauthorized"
    BAD_REQUEST = "bad_request"
    # Forex errors
    FOREX_ERROR = "forex_error"
    FOREX_INVALID_API_KEY = "forex_invalid_api_key"
    FOREX_RATE_LIMIT = "forex_rate_limit"
    # Redis errors
    REDIS_ERROR = "redis_error"


class AppException(Exception):
    http_status_code: status = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_type: ErrorTypes = ErrorTypes.UNKNOWN
    details: str = None

    def __init__(
        self,
        http_status_code: status = None,
        error_type: str = None,
        details: str = None
    ):
        self.http_status_code = http_status_code or self.http_status_code
        self.error_type = error_type or self.error_type
        self.details = details or self.details
        # super call to not override __init__ from Exception class
        super(AppException, self).__init__()


class ApiException(AppException):
    pass


class Unauthorized(ApiException):
    http_status_code: status = status.HTTP_401_UNAUTHORIZED
    error_type: ErrorTypes = ErrorTypes.UNAUTHORIZED
    details: str = "Your email or api key is invalid"


class BadRequest(ApiException):
    http_status_code: status = status.HTTP_400_BAD_REQUEST
    error_type: ErrorTypes = ErrorTypes.BAD_REQUEST
    details: str = "Bad request"


class ForexException(AppException):
    http_status_code: status = status.HTTP_424_FAILED_DEPENDENCY
    error_type: ErrorTypes = ErrorTypes.FOREX_ERROR
    details: str = "Unknown forex exception occurred"


class ForexInvalidApiKey(ForexException):
    error_type: ErrorTypes = ErrorTypes.FOREX_INVALID_API_KEY
    details: str = "Forex API key has expired or is invalid"


class ForexRateLimitExceeded(ForexException):
    error_type: ErrorTypes = ErrorTypes.FOREX_RATE_LIMIT
    details: str = "You have exceeded rate limit quota"


class RedisException(AppException):
    error_type: ErrorTypes = ErrorTypes.REDIS_ERROR
    details: str = "Redis error"

