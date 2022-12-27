# import uvicorn
from fastapi import FastAPI

from currency_converter_api.routers.users import app1
from currency_converter_api.routers.converter import router as converter_router
from currency_converter_api.routers.admin import router as admin_router
from currency_converter_api.sql.database import database
from currency_converter_api.middlewares import CreditCounter

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

app1.add_middleware(CreditCounter)

app.include_router(converter_router)
app.include_router(admin_router)
app.mount("/app1", app1)


@app.on_event("shutdown")
async def shutdown():
    database.dispose_session()


# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host="127.0.0.1",
#         port=8080,
#         reload=True
#     )
