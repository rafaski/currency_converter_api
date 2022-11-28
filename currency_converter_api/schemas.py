from pydantic import BaseModel, validator
from typing import Optional, Any
from fastapi import HTTPException
import re


class Output(BaseModel):
    """
    User output layout class
    """
    success: bool
    message: Optional[str] = None
    results: Optional[Any] = None


class User(BaseModel):
    """
    User login info
    """
    email: str

    @validator("email")
    def validate_email(cls, value: str):
        pattern = \
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        if re.match(pattern, value):
            return value
        raise HTTPException(status_code=400, detail="Check your email address")



