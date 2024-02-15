from sqlalchemy import Column, Integer, String, DateTime, Boolean, func,ForeignKey,Float
from sqlalchemy.orm import relationship

from db import Base


class Products(Base):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    trade_price = Column(Float, nullable=True)
    user_id = Column(Integer,ForeignKey('Users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    user = relationship("Users", back_populates="customer")
    trade = relationship("Trades", back_populates="customer")
