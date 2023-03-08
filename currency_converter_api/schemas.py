import re
from pydantic import BaseModel, validator
from typing import Any
from fastapi import HTTPException
from uuid import uuid4
from datetime import datetime, timedelta

from currency_converter_api.enums import SubscriptionType


class Output(BaseModel):
    """
    User output layout class
    """
    success: bool
    message: str | None = None
    results: Any | None = None


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

    @property
    def credits(self):
        """
        subscription points based on subscription type.
        """
        subscription_mapper = {
            SubscriptionType.BASIC: 100,
            SubscriptionType.HOBBY: 500,
            SubscriptionType.PRO: 10000,
            SubscriptionType.ENTERPRISE: 50000
        }
        return subscription_mapper.get(self.subscription)

    @property
    def concurrency(self):
        """
        concurrency level based on subscription type.
        """
        concurrency_mapper = {
            SubscriptionType.BASIC: 1,
            SubscriptionType.HOBBY: 3,
            SubscriptionType.PRO: 10,
            SubscriptionType.ENTERPRISE: 15
        }
        return concurrency_mapper.get(self.subscription)


class CreateUser(BaseModel):
    """
    User sign up info from the server:
    - individual api key
    - concurrency value
    - amount of credits to make api calls based on chosen plan
    - expiration
    """

    user: UserSubscribe
    api_key: str = str(uuid4())[:13]
    expiration: str | None = str(datetime.now() + timedelta(hours=1))




