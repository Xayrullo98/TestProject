from pydantic import BaseModel


class Sold_Product(BaseModel):
    product_id: int
    number: float
