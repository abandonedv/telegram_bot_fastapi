from pydantic import BaseModel
from typing import Optional


class Price_of_crypt(BaseModel):
    fromm: str
    to: str
    price: float
