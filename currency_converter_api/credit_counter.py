from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class CreditCounter(BaseHTTPMiddleware):
    async def count(self, request: Request, call_next):
        # get user credit from sql
        response = await call_next(request)
        # deduct credits credits -= 1
        response.headers['X-Credits-Left'] = 0  # pass credit amount in headers
        # update db with new credit amount
        return response
