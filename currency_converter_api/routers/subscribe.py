from fastapi import Request, APIRouter

from currency_converter_api.schemas import Output, UserSubscribe, CreateUser
from currency_converter_api.dependencies.mongo_connection import create_user

router = APIRouter(tags=["subscribe"])


@router.post("/subscribe", response_model=Output)
async def subscribe(request: Request, user: UserSubscribe):
    """
    Subscribe a new user with email address and subscription type.
    Subscriptions: basic, hobby, pro, enterprise.
    Returns individual api key to make api calls.
    """
    new_user = CreateUser(user=user)
    await create_user(user=new_user)
    return Output(
        success=True,
        message="User created",
        results=new_user.api_key
    )

