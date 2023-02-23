from fastapi import APIRouter, Request
from redis import asyncio as aioredis

from currency_converter_api.schemas import Output
from currency_converter_api.dependencies.redis import ping

router = APIRouter(tags=["health"])


@router.get("/ping")
async def health_check(request: Request):
    """
    Checking redis connection
    """
    try:
        if ping():
            return Output(success=True, message="Pong")
    except aioredis.ConnectionError:
        return Output(success=False, message="Raised connection error")
