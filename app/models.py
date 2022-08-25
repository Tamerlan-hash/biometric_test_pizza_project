from sqlalchemy import Column, BigInteger, String, ForeignKey, Boolean, Enum

from settings.database.connection import Base

from .enums import Thickness, Cheese


class Restaurant(Base):
    __tablename__ = "Restaurants"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)


class Pizza(Base):
    __tablename__ = "Pizzas"
    id = Column(BigInteger, primary_key=True, index=True)
    restaurant_id = Column(
        BigInteger,
        ForeignKey("Restaurants.id", ondelete="CASCADE")
    )
    name = Column(String(100), nullable=False)
    cheese = Column(Enum(Cheese), default=Cheese.PARMEZAN)
    thickness = Column(Enum(Thickness), default=Thickness.MEDIUM)
    secret_ingredient = Column(String(100), nullable=True)
