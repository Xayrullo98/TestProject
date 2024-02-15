from sqlalchemy import Column, Integer, String, DateTime, Boolean, func,ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Customers(Base):
    __tablename__ = "Customers"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=True)
    comment = Column(String(100), nullable=True)
    user_id = Column(Integer,ForeignKey('Users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    user = relationship("Users", back_populates="customer")
    trade = relationship("Trades", back_populates="customer")
