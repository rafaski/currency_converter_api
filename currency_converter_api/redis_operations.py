import redis
import json
from typing import Any, NoReturn

redis_connection = redis.Redis(host="127.0.0.1", port=6379)


def get(key: str) -> Any:
    results = redis_connection.get(key)
    if results is not None:
        results = json.loads(results)
    return results


def store(key: str, value: dict) -> None:
    redis_connection.set(name=key, value=json.dumps(value))


def store_exp(key: str, time: int, value: dict) -> None:
    redis_connection.setex(name=key, time=time, value=json.dumps(value))


def ping() -> bool | NoReturn:
    return redis_connection.ping()

