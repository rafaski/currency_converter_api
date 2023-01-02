from fastapi import FastAPI

from currency_converter_api.routers.converter import router as converter_router
from currency_converter_api.routers.health_check import router as health_router
from currency_converter_api.routers.root import router as root_router
from currency_converter_api.routers.admin import router as admin_router
from currency_converter_api.sql.database import database

description = """
Currency Converter allows you to:

* subscribe
* get all users info
* get all supported currencies
* convert currencies
* fetch a single currency exchange rate
* fetch all currency exchange rate
* get historical data on currency exchange rates

Data fetched from fastforex.io api.
"""

app = FastAPI(
    title="Currency Converter",
    description=description,
    contact={
        "name": "FastForex",
        "url": "https://www.fastforex.io/",
    },
)

app.include_router(converter_router)
app.include_router(admin_router)
app.include_router(health_router)
app.include_router(root_router)


@app.on_event("shutdown")
async def shutdown():
    database.dispose_session()