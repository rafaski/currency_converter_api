from fastapi import Request

from currency_converter_api.errors import Unauthorized, Forbidden
from currency_converter_api.dependencies.mongo_connection import (
    get_user_by_api_key
)
from currency_converter_api.settings import ADMIN_API_KEY


async def verify_user(request: Request):
    """
    Verifies if user is authorized to make API call.
    Valid email and api key is required.
    Verifies if user has enough credits to make a request.
    """
    headers = dict(request.headers)
    api_key = headers.get("api_key")
    user = await get_user_by_api_key(api_key)
    credits_left = user.get("credits")
    if user is None:
        raise Unauthorized()
    if credits_left <= 0:
        raise Forbidden()
    request.state.credits = credits_left
    return api_key


async def verify_admin(request: Request):
    """
    Verifies admin access with admin api key
    """
    headers = dict(request.headers)
    api_key = headers.get("api_key")
    if api_key == ADMIN_API_KEY:
        return api_key
    raise Forbidden()

