import httpx
from dotenv import load_dotenv
from os import getenv
from functools import wraps
from typing import Optional
from fastapi import HTTPException
from enum import Enum

from currency_converter_api.redis_operations import (
    get, store_exp
)

load_dotenv()


def cache(func):
    """
    Cache forex client api response in redis
    """
    @wraps(func)
    async def _cache(*args, **kwargs):
        forex_client_obj = args[0]

        if forex_client_obj.redis_key is None:
            # I have no redis key (no cache), call API and return results
            return await func(*args, **kwargs)

        # I have a redis key, meaning I might have cache
        # Search for cache
        results = await get(key=forex_client_obj.redis_key)
        if results is None:
            # no results in redis, call the API
            results = await func(*args, **kwargs)
            await store_exp(
                key=forex_client_obj.redis_key,
                value=results,
                time=forex_client_obj.data_ttl
            )
        return results
    return _cache


def validate_input(func):
    """
    Validate if currency code is supported by forex api
    """
    @wraps(func)
    async def _validate_input(*args, **kwargs):

        async def is_currency_valid(currency_code: Optional[str]) -> bool:
            if currency_code is None:
                return True
            all_currencies = await args[0].get_currencies()
            if currency_code.upper() in all_currencies.keys():
                return True

        # before I run the function, I validate kwargs (currency codes)
        if any([
            not await is_currency_valid(kwargs.get("from_curr")),
            not await is_currency_valid(kwargs.get("to_curr"))
        ]):
            raise HTTPException(status_code=400, detail="Invalid currency")
        return await func(*args, **kwargs)
    return _validate_input


class ForexClient:
    api_key = getenv("API_KEY")
    base_url = "https://api.fastforex.io/"
    headers = {"accept": "application/json"}
    params = {
        "api_key": api_key
    }
    data_ttl = 60 * 60
    redis_key: Optional[str] = None

    @cache
    async def request(
        self,
        endpoint: str,
        parameters: Optional[dict] = None
    ) -> dict:
        """
        Make a http request to fetch data from forex API
        """
        if parameters:
            self.params.update(parameters)
        async with httpx.AsyncClient() as client:
            forex_response = await client.get(
                url=f"{self.base_url}{endpoint}",
                params=self.params,
                headers=self.headers
            )
        return forex_response.json()

    async def get_currencies(self) -> dict:
        """
        Fetch a list of supported currencies
        """
        self.data_ttl = 60 * 60 * 24
        self.redis_key = "currencies"
        endpoint = ForexEndpoint.CURRENCIES
        response = await self.request(endpoint=endpoint)
        return response["currencies"]

    @validate_input
    async def get_currency_rate(self, from_curr: str, to_curr: str) -> float:
        """
        Fetch a single currency exchange rate, from and to any supported currency
        """
        self.redis_key = f"{from_curr}-{to_curr}"
        endpoint = ForexEndpoint.FETCH_ONE
        params = {
            "from": from_curr,
            "to": to_curr
        }
        results = await self.request(endpoint=endpoint, parameters=params)
        currency_rate = results["result"][to_curr]
        return currency_rate

    @validate_input
    async def convert(self, from_curr: str, to_curr: str, amount: int) -> float:
        """
        Convert an amount of one currency into another currency
        """
        currency_rate = await self.get_currency_rate(
            from_curr=from_curr,
            to_curr=to_curr
        )
        return currency_rate * amount

    @validate_input
    async def get_all_currency_rates(self, from_curr: str) -> dict:
        """
        Fetch all available currency rates
        """
        self.redis_key = from_curr
        endpoint = ForexEndpoint.FETCH_ALL
        params = {
            "from": from_curr
        }
        return await self.request(endpoint=endpoint, parameters=params)

    @validate_input
    async def get_historical_rates(
        self,
        from_curr: str,
        to_curr: str,
        date: str
    ) -> dict:
        """
        Get historical conversion rate data
        """
        endpoint = ForexEndpoint.HISTORICAL
        params = {
            "date": date,
            "from": from_curr,
            "to": to_curr
        }
        return await self.request(endpoint=endpoint, parameters=params)


class ForexEndpoint(Enum):
    """
    Enums for forex endpoints
    """
    CURRENCIES = "currencies"
    FETCH_ONE = "fetch-one"
    FETCH_ALL = "fetch-all"
    HISTORICAL = "historical"

