from fastapi import FastAPI, Request

from currency_converter_api.schemas import Output, UserSubscribe, CreateUser
from currency_converter_api.sql.operations import (
    get_users, create_user, get_user_by_api_key
)

app1 = FastAPI(openapi_prefix="/app1")


@app1.post("/subscribe", response_model=Output)
async def subscribe(request: Request, user: UserSubscribe):
    """
    Subscribe a new user with email address and subscription type.
    Subscriptions: basic, hobby, pro, enterprise.
    Returns individual api key to make api calls.
    """
    new_user = CreateUser(
        email=user.email,
        subscription=user.subscription
    )
    create_user(user=new_user)
    return Output(
        success=True,
        message="User created",
        results=new_user.api_key
    )


@app1.get("/users", response_model=Output)
async def all_users(request: Request):
    """
    Returns a list of all signed-up users
    """
    return Output(success=True, results=get_users())


@app1.get("/users/{api_key}", response_model=Output)
async def all_users(request: Request, api_key: str):
    """
    Returns user info from database
    """
    return Output(success=True, results=get_user_by_api_key(email=api_key))
