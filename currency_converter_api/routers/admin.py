from fastapi import APIRouter, Request

from currency_converter_api.schemas import Output
from currency_converter_api.dependencies.redis_operations import ping

router = APIRouter()


@router.get("/ping")
async def ping(request: Request):
    return Output(success=True, results=ping())


@router.get("/")
def root():
    """
    Index page
    """
    return {
        "message": "Welcome to Currency Converter API. Go to /docs to test API"
    }
