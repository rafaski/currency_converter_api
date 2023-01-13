from fastapi import FastAPI

from currency_converter_api.routers.converter import router as converter_router
from currency_converter_api.routers.health_check import router as health_router
from currency_converter_api.routers.admin import router as admin_router
from currency_converter_api.routers.subscribe import router as subscribe_router

description = """
Currency Converter allows you to:

* subscribe to services
* get all supported currencies
* convert currencies
* fetch a single currency exchange rate
* fetch all currency exchange rate
* get historical data on currency exchange rates

To access /admin endpoints you require admin api key past in headers.
To access /converter endpoints subscribe to receive user api key. Pass it in headers.

Currency data fetched from fastforex.io api.
"""

app = FastAPI(
    title="Currency Converter",
    docs_url="/",
    description=description,
    contact={
        "name": "FastForex",
        "url": "https://www.fastforex.io/",
    },
)

app.include_router(health_router)
app.include_router(subscribe_router)
app.include_router(converter_router)
app.include_router(admin_router)


