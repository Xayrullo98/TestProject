from typing import Optional

from pydantic import BaseModel


class CustomersBase(BaseModel):
    full_name: str
    phone: str
    comment: Optional[str] = ''


class CustomersCreate(CustomersBase):
    pass


class CustomersUpdate(CustomersBase):
    id: int
    status: bool