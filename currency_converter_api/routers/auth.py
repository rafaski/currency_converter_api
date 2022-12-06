from fastapi import Request

from currency_converter_api.redis_operations import get
from currency_converter_api.errors import Unauthorized
from currency_converter_api.sql.models import User


async def verify_user(request: Request, user: User):
    """
    Verifies if user is authorized to request data.
    Valid email and api key is required.
    """
    headers = dict(request.headers)
    email = headers.get("email")
    api_key = headers.get("api_key")
    # authorization from redis case
    # if api_key == await get(email):
    #     return api_key

    # authorization from sql
    query_sql = user.select(["users"])
    raise Unauthorized()
