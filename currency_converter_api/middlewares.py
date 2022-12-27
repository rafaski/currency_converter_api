from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from currency_converter_api.sql.operations import (
    get_user_by_api_key, update_credits
)
from currency_converter_api.errors import Unauthorized


class CreditCounter(BaseHTTPMiddleware):

    @staticmethod
    async def deduct(request: Request, call_next):
        """
        A middleware function that deducts user credits for each successful
        API call. It can access request object and create a custom header
        with the amount of credits left. It updates credit value in database.
        """
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
