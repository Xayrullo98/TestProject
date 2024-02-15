from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: float
    trade_price: float


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    id: int
    status: bool



