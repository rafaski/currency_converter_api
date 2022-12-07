from fastapi import APIRouter, Request
from uuid import uuid4

from currency_converter_api.schemas import Output, CreateUser
from currency_converter_api.redis_operations import get, lpush, store
from currency_converter_api.errors import BadRequest
from currency_converter_api.sql.sql_operations import get_users, create_user

router = APIRouter()


@router.post("/create_user", response_model=Output)
async def create_user(request: Request, user: CreateUser):
    """
    Create a user and store user data in redis cache
    """
    # redis_key = "users"
    # user_exists = False
    #
    # existing_users = []
    # while True:
    #     existing_email = await rpoplpush(redis_key)
    #     existing_email = existing_email.decode("utf-8")
    #     if existing_email is None:
    #         break
    #     if existing_email == user.email:
    #         user_exists = True
    #         break
    #     if existing_email in existing_users:
    #         break
    #     existing_users.append(existing_email)
    #
    # if user_exists:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Email already exists"
    #     )
    if await get(key=user.email):
        raise BadRequest(details="Email already exists")

    api_key = str(uuid4())[:13]
    await store(key=user.email, value=api_key)
    await lpush(key="users", value=user.email)
    # sql
    await create_user()
    return Output(success=True, message="User created", results=api_key)


@router.get("/all_users", response_model=Output)
async def all_users(request: Request):
    """
    Get a list of all signed-up users
    """
    redis_key = "users"
    user_list_redis = await get(key=redis_key)
    # sql
    users = await get_users()
    return Output(success=True, results=users)
