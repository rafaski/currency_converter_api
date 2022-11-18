from fastapi import HTTPException, Request

X_TOKEN = "secret-token"


async def verify_token(request: Request):
    headers = dict(request.headers)
    if headers.get("x-token") == X_TOKEN:
        return headers.get("x-token")
    raise HTTPException(status_code=400, detail="X-Token header invalid")
