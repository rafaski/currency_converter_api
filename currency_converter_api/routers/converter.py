from fastapi import APIRouter, Request, HTTPException, Depends
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

from currency_converter_api.schemas import Output, User
from currency_converter_api.redis_operations import (get, lpush, rpoplpush)
from currency_converter_api.forex_client import ForexClient
from currency_converter_api.routers.auth import verify_user

router = APIRouter()

load_dotenv()


@router.post("/create_user", response_model=Output)
async def create_user(request: Request, user: User):
    """
    Create a user and store user data in redis cache
    """
    redis_key = "users"
    first_item = None
    user_exists = False
    api_key = getenv("API_KEY")

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

    return Output(success=True, message="User created", results=api_key)


@router.get("/all_users", response_model=Output)
async def all_users(request: Request):
    """
    Get a list of all signed-up users
    """
    redis_key = "users"
    user_list = await get(key=redis_key)
    return Output(success=True, results=user_list)


@router.get(
    "/currencies",
    dependencies=[Depends(verify_user)],
    response_model=Output
)
async def currencies(request: Request):
    """
    Fetch a list of supported currencies
    """
    available_currencies = await ForexClient().get_currencies()
    return Output(success=True, results=available_currencies)


@router.get(
    "/convert",
    dependencies=[Depends(verify_user)],
    response_model=Output
)
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
    converted_currency = await ForexClient().convert(
        from_curr=from_curr,
        to_curr=to_curr,
        amount=amount
    )
    return Output(success=True, results=converted_currency)


@router.get(
    "/fetch_one",
    dependencies=[Depends(verify_user)],
    response_model=Output
)
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
    currency_rate = await ForexClient().get_currency_rate(
        from_curr=from_curr,
        to_curr=to_curr
    )
    return Output(success=True, results=currency_rate)


@router.get(
    "/fetch_all",
    dependencies=[Depends(verify_user)],
    response_model=Output
)
async def fetch_all(request: Request, from_curr: str):
    """
    Fetch all available currency rates.
    from_curr : Base currency symbol
    """
    all_currency_rates = await ForexClient().get_all_currency_rates(
        from_curr=from_curr
    )
    return Output(success=True, results=all_currency_rates)


@router.get(
    "/historical",
    dependencies=[Depends(verify_user)],
    response_model=Output
)
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
    historical_date = datetime.strptime(date, "%Y-%m-%d")
    today_date = datetime.today()
    dt = today_date - historical_date
    if dt.days > 14:
        raise HTTPException(
            status_code=400,
            detail="date must be limited to within tle last 14 days"
        )
    historical_rates = await ForexClient().get_historical_rates(
        from_curr=from_curr,
        to_curr=to_curr,
        date=date
    )
    return Output(success=True, results=historical_rates)


