from fastapi import APIRouter

from currency_converter_api.schemas import Output

router = APIRouter()


@router.get("/")
def root():
    """
    Index page
    """
    return Output(
        succes=True,
        messaage="Welcome to Currency Converter API. Go to /docs to test API"
    )
