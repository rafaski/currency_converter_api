from fastapi import FastAPI
from routers.converter import router


description = """
Currency Converter allows you to:

* get all supported currencies
* convert currencies
* fetch a single currency exchange rate
* fetch all currency exchange rate

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

app.include_router(router)
