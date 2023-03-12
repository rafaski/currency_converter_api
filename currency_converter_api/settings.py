import os
from typing import Any
from functools import lru_cache


@lru_cache()
def load_variable(name: str, default: Any = None) -> str:
    variable = os.getenv(name, default)
    if variable is None:
        print(f"Unable to load variable {name}")
    return variable


ADMIN_API_KEY = load_variable(name="ADMIN_API_KEY")

# Dependencies - redis
REDIS_HOST = load_variable(name="REDIS_HOST", default="127.0.0.1")
REDIS_PORT = load_variable(name="REDIS_PORT", default="6379")
REDIS_URL = load_variable(
    name="REDIS_URL",
    default=f"redis://{REDIS_HOST}:{REDIS_PORT}"
)

# Dependencies - mongodb
MONGODB_HOST = load_variable(name="MONGODB_HOST", default="127.0.0.1")
MONGODB_PORT = load_variable(name="MONGODB_PORT", default="27017")
MONGODB_URL = load_variable(
    name="MONGODB_URL",
    default=f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}"
)

# Dependencies - forex
FOREX_BASE_URL = load_variable(
    name="FOREX_BASE_URL",
    default="https://api.fastforex.io/"
)
FOREX_API_KEY = load_variable(name="FOREX_API_KEY")

# DB
DATABASE_URL = load_variable(
    name="DATABASE_URL",
    default="sqlite:///./sql_app.db"
)


