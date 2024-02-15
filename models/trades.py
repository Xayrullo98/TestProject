from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Float
from sqlalchemy.orm import relationship

from db import Base


class Trades(Base):
    __tablename__ = "Trades"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("Customers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    amount = Column(Float, nullable=True)
    comment = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, default=True)
    trade_number = Column(String(30), nullable=True)
    user = relationship("Users", back_populates="trade")
    payment = relationship("Payments", back_populates="trade")
    customer = relationship("Customers", back_populates="trade")
