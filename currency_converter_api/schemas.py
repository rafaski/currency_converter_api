import re
from pydantic import BaseModel, validator
from typing import Optional, Any
from fastapi import HTTPException
from uuid import uuid4
from datetime import datetime, timedelta

from currency_converter_api.enums import SubscriptionType


class Output(BaseModel):
    """
    User output layout class
    """
    success: bool
    message: Optional[str] = None
    results: Optional[Any] = None


class UserSubscribe(BaseModel):
    """
    Subscribing new user with email address and subscription type.
    """
    email: str = None
    subscription: SubscriptionType = None

    @validator("email")
    def validate_email(cls, value: str):
        pattern = \
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        if re.match(pattern, value):
            return value
        raise HTTPException(status_code=400, detail="Check your email address")

    @staticmethod
    def credit_points(sub_type: SubscriptionType):
        """
        subscription points
        """
        subscriptions = {
            SubscriptionType.BASIC: 100,
            SubscriptionType.HOBBY: 500,
            SubscriptionType.PRO: 10000,
            SubscriptionType.ENTERPRISE: 50000
        }
        return subscriptions.get(sub_type)


class CreateUser(BaseModel):
    """
    User sign up info from the server:
    - individual api key
    - concurrency value
    - amount of credits to make api calls based on chosen plan
    - expiration
    """

    email: str
    subscription: SubscriptionType
    api_key: str = str(uuid4())[:13]
    concurrency: Optional[bool] = False
    credits: int = UserSubscribe.credit_points(UserSubscribe.subscription)
    expiration: Optional[str] = str(datetime.now() + timedelta(hours=1))


