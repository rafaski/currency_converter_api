from pydantic import BaseModel, validator
from typing import Optional, Any
from fastapi import HTTPException
from uuid import uuid4
import re

from datetime import datetime, timedelta


class Output(BaseModel):
    """
    User output layout class
    """
    success: bool
    message: Optional[str] = None
    results: Optional[Any] = None


class UserEmail(BaseModel):
    email: str = None

    @validator("email")
    def validate_email(cls, value: str):
        pattern = \
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        if re.match(pattern, value):
            return value
        raise HTTPException(status_code=400, detail="Check your email address")


class CreateUser(BaseModel):
    """
    User sign up info
    """
    email: str
    api_key: str = str(uuid4())[:13]
    concurrency: Optional[bool] = False
    credits: Optional[int] = 0
    subscription: Optional[str] = "basic"
    expiration: Optional[str] = str(datetime.now() + timedelta(hours=1))


