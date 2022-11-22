import aioredis
from typing import Any, NoReturn, List
import json

redis_connection = aioredis.from_url("redis://localhost")


async def get(key: str) -> Any:
    results = await redis_connection.get(key)
    if results is not None:
        results = json.loads(results)
    return results


async def lpush(key: str, value: str) -> None:
    await redis_connection.lpush(key, value)


def rpoplpush(key: str) -> str:
    return redis_connection.rpoplpush(key)


async def store(key: str, value: dict) -> None:
    await redis_connection.set(name=key, value=json.dumps(value))


async def store_exp(key: str, time: int, value: dict) -> None:
    await redis_connection.setex(name=key, time=time, value=json.dumps(value))


def ping() -> bool | NoReturn:
    return redis_connection.ping()
