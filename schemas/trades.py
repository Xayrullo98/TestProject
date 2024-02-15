from typing import Optional,List
from pydantic import BaseModel
from pydantic.datetime_parse import datetime

from schemas.sold_products import Sold_Product


class TradeBase(BaseModel):
    customer_id: int
    products: List[Sold_Product]
    date: datetime


class TradeCreate(TradeBase):
    pass


class TradeUpdate(TradeBase):
    id: int
    status: bool
