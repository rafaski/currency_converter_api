from fastapi import Request, APIRouter, Depends

from currency_converter_api.schemas import Output
from currency_converter_api.sql.operations import (
    get_users, get_user_by_api_key
)
from currency_converter_api.routers.auth import verify_admin

router = APIRouter(prefix="/admin", dependencies=[Depends(verify_admin)])


@router.get("/users", response_model=Output, tags=["admin"])
async def all_users(request: Request):
    """
    Returns a list of all signed-up users
    """
    return Output(success=True, results=get_users())


@router.get("/users/{api_key}", response_model=Output, tags=["admin"])
async def all_users(request: Request, api_key: str):
    """
    Returns user info from database
    """
    return Output(success=True, results=get_user_by_api_key(api_key=api_key))
