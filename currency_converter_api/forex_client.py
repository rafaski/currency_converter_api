import httpx
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class ForexClient:
    API_KEY = getenv("API_KEY")
    BASE_URL = "https://api.fastforex.io/"
    HEADERS = {"accept": "application/json"}
    PARAMS = {
        "api_key": API_KEY
    }

    async def forex_client(self, endpoint: str, params: dict) -> dict:
        params.update(self.PARAMS)
        async with httpx.AsyncClient() as client:
            forex_response = await client.get(
                url=f"{self.BASE_URL}{endpoint}",
                params=params,
                headers=self.HEADERS
            )
        return forex_response.json()
