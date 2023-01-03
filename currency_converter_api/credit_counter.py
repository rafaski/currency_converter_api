from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from currency_converter_api.sql.operations import update_credits
from currency_converter_api.errors import Unauthorized


class CreditCounter(BaseHTTPMiddleware):

    @staticmethod
    async def deduct(request: Request, call_next):
        """
        A function that deducts user credits for each successful
        API call. It can access request object and stores the amount
        of credits left in request.state. It updates credit value in database.
        """
        response = await call_next(request)
        headers = dict(request.headers)
        api_key = headers.get("api_key")

        if response.get("success"):
            credits_left = request.state.credits - 1
            update_credits(api_key=api_key, credits_left=credits_left)
            request.state.credits = credits_left
            return response
        raise Unauthorized()
