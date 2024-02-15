from sqlalchemy import Column, Integer, String, DateTime, Boolean, func,ForeignKey,Float
from sqlalchemy.orm import relationship

from db import Base


class Payments(Base):
    __tablename__ = "Payments"
    id = Column(Integer, primary_key=True)
    trade_id = Column(Integer,ForeignKey("Trades.id"), nullable=False)
    amount = Column(Float, nullable=False)
    user_id = Column(Integer,ForeignKey('Users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    user = relationship("Users", back_populates="customer")
    trade = relationship("Trades", back_populates="customer")
