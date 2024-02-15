from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    name: str
    username: str
    roll: str
    password: str
    number: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    id: int
    balance: float


class Token(BaseModel):
    access_token = str
    token = str


class TokenData(BaseModel):
    id: Optional[str] = None


class UserCurrent(BaseModel):
    id: int
    name: str
    username: str
    password: str
    roll: str
    status: bool
