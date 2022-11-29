from fastapi import HTTPException, Request

from currency_converter_api.redis_operations import get


async def verify_user(request: Request):
    """
    Verifies is user is authorized to request data.
    Valid email and api key is required.
    """
    headers = dict(request.headers)
    email = headers.get("email")
    api_key = headers.get("api_key")
    if api_key == await get(email):
        return api_key
    raise HTTPException(status_code=401, detail="User unauthorized")
