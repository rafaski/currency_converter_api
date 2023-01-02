from fastapi import APIRouter, Request

from currency_converter_api.schemas import Output
from currency_converter_api.dependencies.redis_operations import ping

router = APIRouter()


@router.get("/ping")
async def health_check(request: Request):
    """
    Checking redis connection
    """
    await ping()
    return Output(success=True, message="pong")