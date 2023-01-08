from fastapi import APIRouter

from currency_converter_api.schemas import Output

router = APIRouter()


@router.get("/")
def root():
    """
    Index page
    """
    return Output(
        success=True,
        message="Welcome to Currency Converter API. Go to /docs to test API"
    )
