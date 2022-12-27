from fastapi import Request

from currency_converter_api.errors import Unauthorized
from currency_converter_api.sql.operations import get_user_by_api_key


async def verify_user(request: Request):
    """
    Verifies if user is authorized to make API call.
    Valid email and api key is required.
    Verifies if user has enough credits to make a request.
    """
    headers = dict(request.headers)
    api_key = headers.get("api_key")
    user = get_user_by_api_key(api_key)
    credits_left = user.get("credits")
    if user is not None and credits_left >= 0:
        return api_key
    raise Unauthorized()
