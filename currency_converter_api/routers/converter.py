from fastapi import APIRouter, Request, Depends
import httpx
import redis

from currency_converter_api.schemas import Output, User
from currency_converter_api._secrets import key
from currency_converter_api.routers.auth import verify_token
from currency_converter_api.redis_operations import get, store, store_exp

router = APIRouter()

redis_connection = redis.Redis(host="127.0.0.1", port=6379)

# replace key with apikey
API_KEY = key
BASE_URL = "https://api.fastforex.io/"
HEADERS = {"accept": "application/json"}


@router.post("/create_user", response_model=Output)
async def create_user(request: Request, user: User):
    """
    Create user for authorization
    """
    new_user = user.dict()
    redis_key = user.login
    redis_response = get(key=redis_key)
    if redis_response is None:
        store(key=redis_key, value=new_user)
        return Output(success=True, message="New user created")
    return Output(success=False, message="User already in database")


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
    params = {
        "api_key": API_KEY
    }
    async with httpx.AsyncClient() as client:
        forex_response = await client.get(
            url=f"{BASE_URL}{endpoint}",
            params=params,
            headers=HEADERS
        )
    forex_response = forex_response.json()

    redis_key = f"{endpoint}"
    redis_response = get(key=redis_key)
    if redis_response is None:
        store(key=redis_key, value=forex_response)
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
        "amount": amount,
        "api_key": API_KEY
    }
    async with httpx.AsyncClient() as client:
        forex_response = await client.get(
            url=f"{BASE_URL}{endpoint}",
            params=params,
            headers=HEADERS
        )
    forex_response = forex_response.json()
    return Output(success=True, results=forex_response)


@router.get("/historical", response_model=Output)
async def convert(
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
        "to": to_curr,
        "api_key": API_KEY
    }
    async with httpx.AsyncClient() as client:
        forex_response = await client.get(
            url=f"{BASE_URL}{endpoint}",
            params=params,
            headers=HEADERS
        )
    forex_response = forex_response.json()
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
        "to": to_curr,
        "api_key": API_KEY
    }
    async with httpx.AsyncClient() as client:
        forex_response = await client.get(
            url=f"{BASE_URL}{endpoint}",
            params=params,
            headers=HEADERS
        )
    forex_response = forex_response.json()

    redis_key = f"{endpoint}{from_curr}{to_curr}"
    key_exp = 60 * 60
    redis_response = get(key=redis_key)
    if redis_response is None:
        store_exp(key=redis_key, time=key_exp, value=forex_response)
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
        "from": from_curr,
        "api_key": API_KEY
    }
    async with httpx.AsyncClient() as client:
        forex_response = await client.get(
            url=f"{BASE_URL}{endpoint}",
            params=params,
            headers=HEADERS
        )
    forex_response = forex_response.json()

    redis_key = f"{endpoint}{from_curr}"
    key_exp = 60*60
    redis_response = get(key=redis_key)
    if redis_response is None:
        store_exp(key=redis_key, time=key_exp, value=forex_response)
        return Output(success=True, results=forex_response)
    return Output(success=True, results=redis_response)
