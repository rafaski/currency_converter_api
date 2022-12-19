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


class SubscriptionType(str, Enum):
    """
    Enums for subscription types
    """

    BASIC = "basic"
    HOBBY = "hobby"
    PRO = "pro"
    ENTERPRISE = "enterprise"

