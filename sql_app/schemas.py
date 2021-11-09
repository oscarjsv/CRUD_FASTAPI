from typing import List, Optional
import requests

from pydantic import BaseModel
from datetime import datetime


class AuthDetails(BaseModel):
    username: str
    password: str


class Dogs_Base(BaseModel):
    id: Optional[int]
    name: str
    picture: str = (requests.get(
        'https://dog.ceo/api/breeds/image/random').json())['message']
    is_adopted: Optional[bool] = False
    created_at: datetime

    class Config:
        orm_mode = True


class User_Base(BaseModel):
    name: str
    email: str
    last_name: str
    dogs: List[Dogs_Base] = []

    class Config:
        orm_mode = True

class User(User_Base):
    id : Optional[int]