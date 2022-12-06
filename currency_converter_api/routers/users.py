from fastapi import APIRouter, Request
from uuid import uuid4

from currency_converter_api.schemas import Output, CreateUser
from currency_converter_api.redis_operations import get, lpush, store
from currency_converter_api.errors import BadRequest
from currency_converter_api.sql.database import database
from currency_converter_api.sql.models import users

router = APIRouter()


@router.on_event("startup")
async def startup():
    await database.connect()


@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


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
    query_sql = users.insert().values(
        email=user.email,
        api_key=api_key,
        concurrency=user.concurrency,
        credits=user.credits,
        subscription=user.subscription,
        expiration=user.expiration
    )
    last_record_id = await database.execute(query_sql)

    return Output(success=True, message="User created", results=api_key)


@router.get("/all_users", response_model=Output)
async def all_users(request: Request):
    """
    Get a list of all signed-up users
    """
    redis_key = "users"
    user_list_redis = await get(key=redis_key)
    # sql
    query_sql = users.select()
    user_list_sql = await database.fetch_all(query_sql)

    return Output(success=True, results=query_sql)
