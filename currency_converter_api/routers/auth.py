from fastapi import Request

from currency_converter_api.errors import Unauthorized
from currency_converter_api.sql.sql_operations import get_user


async def verify_user(request: Request):
    """
    Verifies if user is authorized to request data.
    Valid email and api key is required.
    """
    headers = dict(request.headers)
    email = headers.get("email")
    api_key = headers.get("api_key")
    if get_user(email):
        return api_key
    raise Unauthorized()
