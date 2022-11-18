from pydantic import BaseModel
from typing import Optional, Any


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
    login: str
    password: str

