import aioredis
from typing import Any, NoReturn
import json
from typing import Optional
from functools import wraps
from os import getenv

from currency_converter_api.errors import RedisException

redis_connection = aioredis.from_url(getenv("REDIS_URL"))


def redis_operation(func):
    """
    Custom error handler for Redis errors
    """
    @wraps(func)
    async def _redis_operation(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except aioredis.exceptions.RedisError as error:
            raise RedisException(details=str(error))
    return _redis_operation


def cast(
    value: Optional[Any],  # this is a value loaded from redis
    expected_type: str = "str",
) -> Optional[Any]:
    """
    Checks data type of the value stored in redis and loads or decodes value.
    """
    if any([value is None, expected_type is None]):
        return value

    if expected_type == "dict":
        return json.loads(value)
    if expected_type == "str":
        return value.decode("utf-8")


@redis_operation
async def get(key: str, expected_type: Optional[str] = "str") -> Any:
    results = await redis_connection.get(key)
    return cast(value=results, expected_type=expected_type)


@redis_operation
async def lpush(key: str, value: str) -> None:
    await redis_connection.lpush(key, value)


@redis_operation
async def rpoplpush(key: str) -> str:
    return await redis_connection.rpoplpush(key, key)


@redis_operation
async def store(key: str, value: Any) -> None:
    if isinstance(value, dict):
        value = json.dumps(value)
    await redis_connection.set(name=key, value=value)


@redis_operation
async def store_exp(key: str, time: int, value: Any) -> None:
    if isinstance(value, dict):
        value = json.dumps(value)
    await redis_connection.setex(name=key, time=time, value=value)


@redis_operation
def ping() -> bool | NoReturn:
    return redis_connection.ping()
