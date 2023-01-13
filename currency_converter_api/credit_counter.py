from fastapi import Request

from currency_converter_api.dependencies.mongo import update_credits


def deduct(request: Request):
    """
    A function that deducts user credits for each successful
    API call. It can access request object and stores the amount
    of credits left in request.state. It updates credit value in database.
    """
    headers = dict(request.headers)
    api_key = headers.get("api_key")

    credits_left = request.state.credits - 1
    await update_credits(api_key=api_key, credits_left=credits_left)
