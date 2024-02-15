from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, func
from sqlalchemy.orm import relationship

from db import Base


class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    roll = Column(String(20), nullable=True)
    name = Column(String(30), nullable=False)
    phone = Column(String(30), nullable=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    balance = Column(Float, nullable=True, default=0)
    status = Column(Boolean, nullable=False, default=True)
    token = Column(String(400), default='', nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

    trade = relationship("Trades", back_populates="user")
    customer = relationship("Customers", back_populates="user")
    payment = relationship("Payments", back_populates="user")
