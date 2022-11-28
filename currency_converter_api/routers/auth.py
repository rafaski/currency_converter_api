from fastapi import HTTPException, Request


async def verify_user(request: Request, email: str, api_key: str):
    """
    Verifies is user is authorized to request data.
    Valid email and api key is required.
    """
    headers = dict(request.headers)
    if headers.get("email") == email and headers.get("api_key") == api_key:
        return headers.get("email"), headers.get("api_key")
    raise HTTPException(status_code=401, detail="User unauthorized")


