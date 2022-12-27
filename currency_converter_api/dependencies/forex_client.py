import httpx
from dotenv import load_dotenv
from os import getenv
from functools import wraps
from typing import Optional

from currency_converter_api.enums import ForexEndpoint
from currency_converter_api.dependencies.redis_operations import get, store_exp
from currency_converter_api.errors import (
    BadRequest, ForexException, ForexInvalidApiKey, ForexRateLimitExceeded
)

load_dotenv()

# exception_mapper = {
#     400: ForexException,
#     401: ForexInvalidApiKey,
#     403: ForexException,
#     429: ForexRateLimitExceeded
# }


def cache(func):
    """
    Cache forex client api response into redis
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
    Validate if currency code is supported by forex API
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
            raise BadRequest(details="Invalid currency")
        return await func(*args, **kwargs)
    return _validate_input


def httpx_error_handler(func):
    """
    A generic httpx error handler
    """
    @wraps(func)
    async def _http_error_handler(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPError as error:
            raise ForexException(details=str(error))
    return _http_error_handler


class ForexClient:
    """
    A class wrapper over all forex client api calls
    """
    api_key = getenv("API_KEY")
    base_url = "https://api.fastforex.io/"
    headers = {"accept": "application/json"}
    params = {
        "api_key": api_key
    }
    data_ttl = 60 * 60
    redis_key: Optional[str] = None

    @httpx_error_handler
    @cache
    async def request(
        self,
        endpoint: str,
        parameters: Optional[dict] = None
    ) -> dict:
        """
        Make a http request to fetch data from forex api
        """
        if parameters:
            self.params.update(parameters)
        async with httpx.AsyncClient() as client:
            forex_response = await client.get(
                url=f"{self.base_url}{endpoint}",
                params=self.params,
                headers=self.headers
            )
            # handling forex exceptions
            # if forex_response.status_code is not 200:
            #     raise exception_mapper.get(forex_response.status_code)(
            #         details=forex_response.text
            #     )
            if forex_response.status_code == 400:
                raise ForexException(details="Bad request to forex api")
            if forex_response.status_code == 401:
                raise ForexInvalidApiKey()
            if forex_response.status_code == 403:
                raise ForexException(details="Forbidden")
            if forex_response.status_code == 429:
                raise ForexRateLimitExceeded()

        return forex_response.json()

    async def get_currencies(self) -> dict:
        """
        Fetch a list of all supported currencies
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
