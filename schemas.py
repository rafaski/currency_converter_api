from pydantic import BaseModel
from typing import Optional, List


class Output(BaseModel):
    """
    User output layout class
    """
    success: bool
    message: Optional[str] = None
    results: Optional[List[str]] = None
