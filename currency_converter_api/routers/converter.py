from fastapi import APIRouter, Request, Depends
import httpx
import redis
import json
from datetime import datetime, timedelta

from currency_converter_api.schemas import Output
from currency_converter_api._secrets import key
from currency_converter_api.routers.auth import verify_token

router = APIRouter()

redis_connection = redis.Redis(host="127.0.0.1", port=6379)

# replace key with apikey
API_KEY = key
BASE_URL = "https://api.fastforex.io/"
HEADERS = {"accept": "application/json"}


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
    redis_store = redis_connection.set(
        name=redis_key,
        value=json.dumps(forex_response)
    )
    if redis_store is not None:
        redis_response = redis_connection.get(redis_key)
        redis_response = json.loads(redis_response)
        return Output(success=True, results=redis_response)
    return Output(success=True, results=forex_response)


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
    return Output(success=True, results=forex_response)


@router.get("/fetch_all", response_model=Output)
async def fetch_all(request: Request, from_curr: str):
    """
    Fetch all available currency rates.
    from_curr : Base currency symbol
    TODO: Redis cache
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

    # redis_key = f"{endpoint}{from_curr}"
    #
    # if redis_connection.get(redis_key) is None:
    #     redis_connection.set(
    #         name=redis_key,
    #         value=json.dumps(forex_response.json())
    #     )
    #     redis_response = redis_connection.get(redis_key)
    #     redis_response = json.loads(redis_response)
    #     return Output(success=True, results=redis_response)
    # else:
    #     if
    #     redis_response = redis_connection.get(redis_key)
    #     redis_response = json.loads(redis_response)
    #     if redis_response["updated"]


    # lifetime_in_hours = 1.0
    # last_update_str = forex_response["updated"]
    # last_update_obj = datetime.strptime(last_update_str, '%Y-%m-%d %H:%M:%S')
    # dt = datetime.now() - last_update_obj
    # if dt / timedelta(minutes=60) < lifetime_in_hours:
    #     print("less than hour")
    # else:
    #     print("more than hour")
    #
    # redis_key = f"{endpoint}{from_curr}"
    # redis_store = redis_connection.set(
    #     name=redis_key,
    #     value=json.dumps(forex_response.json())
    # )
    # if redis_store is not None:
    #     redis_response = redis_connection.get(redis_key)
    #     redis_response = json.loads(redis_response)
    # #     if redis_response["updated"]
    #     return Output(success=True, results=redis_response)
    return Output(success=True, results=forex_response)
