from fastapi import APIRouter, Request
import httpx

from currency_converter_api.schemas import Output
from currency_converter_api._secrets import key

router = APIRouter()

# replace key with apikey
API_KEY = key
BASE_URL = "https://api.fastforex.io/"
HEADERS = {"accept": "application/json"}


@router.get("/currencies", response_model=Output)
async def currencies(request: Request):
    """
    Fetch a list of supported currencies
    """
    endpoint = "currencies"
    params = {
        "api_key": API_KEY
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f"{BASE_URL}{endpoint}",
            params=params,
            headers=HEADERS
        )
    return Output(success=True, results=response.json())


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
        response = await client.get(
            url=f"{BASE_URL}{endpoint}",
            params=params,
            headers=HEADERS
        )
    return Output(success=True, results=response.json())


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
        response = await client.get(
            url=f"{BASE_URL}{endpoint}",
            params=params,
            headers=HEADERS
        )
    return Output(success=True, results=response.json())


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
        response = await client.get(
            url=f"{BASE_URL}{endpoint}",
            params=params,
            headers=HEADERS
        )
    return Output(success=True, results=response.json())


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
        response = await client.get(
            url=f"{BASE_URL}{endpoint}",
            params=params,
            headers=HEADERS
        )
    return Output(success=True, results=response.json())
