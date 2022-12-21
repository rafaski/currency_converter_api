from fastapi import Request

from currency_converter_api.errors import Unauthorized
from currency_converter_api.sql.sql_operations import get_user_by_api_key


async def verify_user(request: Request):
    """
    Verifies if user is authorized to request data.
    Valid email and api key is required.
    """
    headers = dict(request.headers)
    api_key = headers.get("api_key")
    if get_user_by_api_key(api_key):
        return api_key
    raise Unauthorized()
