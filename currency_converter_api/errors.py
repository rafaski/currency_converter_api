from fastapi import status

from currency_converter_api.enums import ErrorTypes


class AppException(Exception):
    """
    Base app exception class
    """
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
    details: str = "Your api key is invalid or not enough credits"


class Forbidden(ApiException):
    http_status_code: status = status.HTTP_403_FORBIDDEN
    error_type: ErrorTypes = ErrorTypes.FORBIDDEN
    details: str = "Access forbidden"


class BadRequest(ApiException):
    http_status_code: status = status.HTTP_400_BAD_REQUEST
    error_type: ErrorTypes = ErrorTypes.BAD_REQUEST
    details: str = "Bad request"


class ForexException(AppException):
    http_status_code: status = status.HTTP_424_FAILED_DEPENDENCY
    error_type: ErrorTypes = ErrorTypes.FOREX_ERROR
    details: str = "Unknown forex exception occurred"


class ForexBadRequest(ForexException):
    error_type: ErrorTypes = ErrorTypes.FOREX_INVALID_API_KEY
    details: str = "Bad request to forex API"


class ForexInvalidApiKey(ForexException):
    error_type: ErrorTypes = ErrorTypes.FOREX_INVALID_API_KEY
    details: str = "Forex API key has expired or is invalid"


class ForexForbidden(ForexException):
    error_type: ErrorTypes = ErrorTypes.FOREX_FORBIDDEN
    details: str = "Forex API access forbidden"


class ForexRateLimitExceeded(ForexException):
    error_type: ErrorTypes = ErrorTypes.FOREX_RATE_LIMIT
    details: str = "You have exceeded rate limit quota"


class RedisException(AppException):
    error_type: ErrorTypes = ErrorTypes.REDIS_ERROR
    details: str = "Redis error"

