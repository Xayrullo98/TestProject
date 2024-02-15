from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Float
from sqlalchemy.orm import relationship

from db import Base


class Sold_Products(Base):
    __tablename__ = "Sold_Products"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("Customers.id"), nullable=False)
    trade_id = Column(Integer, ForeignKey("Trades.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("Products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    number = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, default=True)

    user = relationship("Users", back_populates="trade")
    payment = relationship("Payments", back_populates="trade")
    customer = relationship("Customers", back_populates="trade")
