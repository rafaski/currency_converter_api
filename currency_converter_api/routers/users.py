from fastapi import APIRouter, Request

from currency_converter_api.schemas import Output, UserSubscribe, CreateUser
from currency_converter_api.sql.sql_operations import get_users, create_user

router = APIRouter()


@router.post("/subscribe", response_model=Output)
async def subscribe(request: Request, user: UserSubscribe):
    """
    Subscribe a new user with email address and subscription type.
    Subscriptions: basic, hobby, pro, enterprise
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


@router.get("/all_users", response_model=Output)
async def all_users(request: Request):
    """
    Get a list of all signed-up users
    """
    return Output(success=True, results=get_users())
