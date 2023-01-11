from fastapi import Request, APIRouter, Depends

from currency_converter_api.schemas import Output
from currency_converter_api.sql.operations import (
    get_users, get_user_by_api_key
)
from currency_converter_api.routers.auth import verify_admin

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(verify_admin)],
    tags=["admin"]
)


@router.get("/users", response_model=Output)
async def all_users(request: Request):
    """
    Returns a list of all signed-up users
    """
    users = get_users()
    return Output(success=True, results=users)


@router.get("/users/{api_key}", response_model=Output)
async def get_user_by_api_key(request: Request, api_key: str):
    """
    Returns user info from database
    """
    user = get_user_by_api_key(api_key=api_key)
    return Output(success=True, results=user)
