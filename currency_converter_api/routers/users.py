from fastapi import APIRouter, Request
from uuid import uuid4

from currency_converter_api.schemas import Output, UserEmail, CreateUser
from currency_converter_api.redis_operations import get, lpush, store
from currency_converter_api.errors import BadRequest
from currency_converter_api.sql.sql_operations import get_users, create_user

router = APIRouter()


@router.post("/create_user", response_model=Output)
async def create_new_user(request: Request, user: UserEmail):
    """
    Create a user and store user data in redis cache
    """
    new_user = CreateUser(email=user.email)
    await create_user(user=new_user)
    return Output(
        success=True,
        message="User created",
        results=new_user.api_key
    )


@router.get("/all_users", response_model=Output)
async def all_users(request: Request):
    """
    Get a list of all signed-up users
    """
    redis_key = "users"
    user_list_redis = await get(key=redis_key)
    # sql
    # users = await get_users()
    # return Output(success=True, results=users)
