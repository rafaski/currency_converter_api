from fastapi import APIRouter, Request, Depends, HTTPException

from currency_converter_api.schemas import Output, User
from currency_converter_api.routers.auth import verify_token
from currency_converter_api.aioredis_operations import (
    get, store, store_exp, lpush, rpoplpush
)
from currency_converter_api.forex_client import ForexClient

router = APIRouter()


@router.post("/create_user", response_model=Output)
async def create_user(request: Request, user: User):
    """
    Create user
    """
    redis_key = "users"
    first_item = None
    user_exists = False

    # CHECK WHETHER THE USER EXISTS
    while not user_exists:
        email = rpoplpush(redis_key)
        if first_item is None:
            first_item = user.email
        if email == user.email:
            user_exists = True
        if email == first_item:
            break

    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    await lpush(redis_key, user.email)
    return Output(success=True, message="User created")

@router.get(
    "/currencies",
    dependencies=[Depends(verify_token)],
    response_model=Output
)
async def currencies(request: Request):
    """
    Fetch a list of supported currencies
    """
    endpoint = "currencies"
    params = {}
    forex_response = await ForexClient().forex_client(
        endpoint=endpoint,
        params=params
    )
    redis_key = f"{endpoint}"
    redis_response = get(key=redis_key)
    if redis_response is None:
        await store(key=redis_key, value=forex_response)
        return Output(success=True, results=forex_response)
    return Output(success=True, results=redis_response)


@router.get("/convert", response_model=Output)
async def convert(
    request: Request,
    amount: int,
    from_curr: str,
    to_curr: str
):
    """
    Convert an amount of one currency into another currency.
    from_curr : Base currency symbol
    to_curr : Target currency symbol
    amount : Amount of source currency to convert
    """
    endpoint = "convert"
    params = {
        "from": from_curr,
        "to": to_curr,
        "amount": amount
    }
    forex_response = await ForexClient().forex_client(
        endpoint=endpoint,
        params=params
    )
    return Output(success=True, results=forex_response)


@router.get("/historical", response_model=Output)
async def historical(
        request: Request,
        from_curr: str,
        to_curr: str,
        date: str
):
    """
    Gets you historical conversion data. Due to trial version,
    date must be limited to within tle last 14 days
    from_curr : Base currency symbol
    to_curr : Target currency symbol
    date: UTC date in YYYY-MM-DD format
    """
    endpoint = "historical"
    params = {
        "date": date,
        "from": from_curr,
        "to": to_curr
    }
    forex_response = await ForexClient().forex_client(
        endpoint=endpoint,
        params=params
    )
    return Output(success=True, results=forex_response)


@router.get("/fetch_one", response_model=Output)
async def fetch_one(
    request: Request,
    from_curr: str,
    to_curr: str
):
    """
    Fetch a single currency exchange rate, from and to any supported currency.
    from_curr : Base currency symbol
    to_curr : Target currency symbol
    """
    endpoint = "fetch-one"
    params = {
        "from": from_curr,
        "to": to_curr
    }
    forex_response = await ForexClient().forex_client(
        endpoint=endpoint,
        params=params
    )

    redis_key = f"{endpoint}{from_curr}{to_curr}"
    key_exp = 60 * 60
    redis_response = await get(key=redis_key)
    if redis_response is None:
        await store_exp(key=redis_key, time=key_exp, value=forex_response)
        return Output(success=True, results=forex_response)
    return Output(success=True, results=redis_response)


@router.get("/fetch_all", response_model=Output)
async def fetch_all(request: Request, from_curr: str):
    """
    Fetch all available currency rates.
    from_curr : Base currency symbol
    """
    endpoint = "fetch-all"
    params = {
        "from": from_curr
    }
    forex_response = await ForexClient().forex_client(
        endpoint=endpoint,
        params=params
    )
    redis_key = f"{endpoint}{from_curr}"
    key_exp = 60*60
    redis_response = await get(key=redis_key)
    if redis_response is None:
        await store_exp(key=redis_key, time=key_exp, value=forex_response)
        return Output(success=True, results=forex_response)
    return Output(success=True, results=redis_response)
