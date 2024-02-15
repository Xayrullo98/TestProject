from pydantic import BaseModel


class PaymentBase(BaseModel):
    trade_id: int
    amount: float


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(PaymentBase):
    id: int
    status: bool


