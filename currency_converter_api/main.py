# import uvicorn
from fastapi import FastAPI

from currency_converter_api.routers.converter import router as converter_router
from currency_converter_api.routers.users import router as user_router
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

converter_router.add_middleware(CreditCounter)

app.include_router(user_router)
app.include_router(converter_router)


@app.on_event("shutdown")
async def shutdown():
    database.dispose_session()


@app.get("/")
def root():
    """
    Index page
    """
    return {
        "message": "Welcome to Currency Converter API. Go to /docs to test API"
    }


# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host="127.0.0.1",
#         port=8080,
#         reload=True
#     )
