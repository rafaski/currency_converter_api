from fastapi import APIRouter, Request, Depends
from datetime import datetime

from currency_converter_api.routers.auth import verify_user
from currency_converter_api.schemas import Output
from currency_converter_api.dependencies.forex_client import ForexClient
from currency_converter_api.errors import BadRequest
from currency_converter_api.credit_counter import CreditCounter

router = APIRouter(dependencies=[Depends(verify_user)])
# router = APIRouter()  # comment out above line to avoid user verification


@router.get("/currencies", response_model=Output)
async def currencies(request: Request):
    """
    Fetch a list of all supported currencies
    """
    available_currencies = await ForexClient().get_currencies()
    await CreditCounter.deduct(request=request, call_next=currencies)
    return Output(success=True, results=available_currencies)


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
    converted_currency = await ForexClient().convert(
        from_curr=from_curr,
        to_curr=to_curr,
        amount=amount
    )
    await CreditCounter.deduct(request=request, call_next=convert)
    return Output(success=True, results=converted_currency)


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
    currency_rate = await ForexClient().get_currency_rate(
        from_curr=from_curr,
        to_curr=to_curr
    )
    await CreditCounter.deduct(request=request, call_next=fetch_one)
    return Output(success=True, results=currency_rate)


@router.get("/fetch_all", response_model=Output)
async def fetch_all(request: Request, from_curr: str):
    """
    Fetch all available currency rates.
    from_curr : Base currency symbol
    """
    all_currency_rates = await ForexClient().get_all_currency_rates(
        from_curr=from_curr
    )
    await CreditCounter.deduct(request=request, call_next=fetch_all)
    return Output(success=True, results=all_currency_rates)


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
    # checking if provided date is within the last 14 days limit
    historical_date = datetime.strptime(date, "%Y-%m-%d")
    today_date = datetime.today()
    dt = today_date - historical_date
    if dt.days > 14:
        raise BadRequest(
            details="date must be limited to within tle last 14 days"
        )

    historical_rates = await ForexClient().get_historical_rates(
        from_curr=from_curr,
        to_curr=to_curr,
        date=date
    )
    await CreditCounter.deduct(request=request, call_next=historical)
    return Output(success=True, results=historical_rates)


