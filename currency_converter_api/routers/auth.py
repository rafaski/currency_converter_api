from fastapi import HTTPException, Request

X_TOKEN = "secret-token"


async def verify_token(request: Request):
    headers = dict(request.headers)
    if headers.get("x-token") == X_TOKEN:
        return headers.get("x-token")
    raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_user(request: Request, login: str, password: str):
    headers = dict(request.headers)
    if headers.get("login") == login and headers.get("password") == password:
        return headers.get("login"), headers.get("password")
    raise HTTPException(status_code=400, detail="User unauthorized")


