from fastapi import APIRouter, Request

from currency_converter_api.schemas import Output
from currency_converter_api.dependencies.redis_operations import ping
from currency_converter_api.sql.database import init_db

router = APIRouter()


@router.get("/ping")
async def health_check(request: Request):
    await ping()
    init_db()
    return Output(success=True, message="pong")


@router.get("/")
def root():
    """
    Index page
    """
    return Output(
        succes=True,
        messaage="Welcome to Currency Converter API. Go to /docs to test API"
    )
