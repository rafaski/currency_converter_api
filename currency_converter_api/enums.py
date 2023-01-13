from enum import Enum


class ErrorTypes(str, Enum):
    """
    Enums for custom error types for exception handling
    """

    # APP errors
    UNKNOWN = "unknown"

    # API errors
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    BAD_REQUEST = "bad_request"

    # Forex errors
    FOREX_ERROR = "forex_error"
    FOREX_BAD_REQUEST = "forex_bad_request"
    FOREX_INVALID_API_KEY = "forex_invalid_api_key"
    FOREX_FORBIDDEN = "forex_forbidden"
    FOREX_RATE_LIMIT = "forex_rate_limit"

    # Redis errors
    REDIS_ERROR = "redis_error"

    # Mongo db errors
    MONGO_DB_ERROR = "mongo_db_error"


class SubscriptionType(str, Enum):
    """
    Enums for subscription types
    """

    BASIC = "basic"
    HOBBY = "hobby"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class ForexEndpoint(str, Enum):
    """
    Enums for forex endpoints
    """
    CURRENCIES = "currencies"
    FETCH_ONE = "fetch-one"
    FETCH_ALL = "fetch-all"
    HISTORICAL = "historical"

