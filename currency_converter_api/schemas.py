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
        pattern = r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$"
        if re.match(pattern, value):
            return value
        raise HTTPException(status_code=400, detail="Check your email address")



