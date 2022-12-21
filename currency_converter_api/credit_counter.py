from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from currency_converter_api.sql.sql_operations import (
    get_user_by_api_key, update_credits
)
from currency_converter_api.errors import Unauthorized


class APICredit(BaseHTTPMiddleware):

    async def deduct(self, request: Request, call_next):
        response = await call_next(request)
        headers = dict(request.headers)
        api_key = headers.get("api_key")
        user = get_user_by_api_key(api_key)
        credit_count = user.get("credits")
        if response.get("success"):
            credits_left = credit_count - 1
            update_credits(email=api_key, credits_left=credits_left)
            response.headers['X-Credits-Left'] = credits_left
            return response
        raise Unauthorized()
