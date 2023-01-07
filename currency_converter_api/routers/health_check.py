from fastapi import APIRouter, Request

from currency_converter_api.schemas import Output
from currency_converter_api.dependencies.redis_operations import ping

router = APIRouter()


@router.get("/ping", tags=["health"])
async def health_check(request: Request):
    """
    Checking redis connection
    """
    try:
        if ping():
            return Output(success=True, message="Pong")
    except redis.ConnectionError:
        return Output(success=False, message="Raised connection error")
