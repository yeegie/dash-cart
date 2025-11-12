from sqlalchemy import Column, UUID, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from .BaseModel import BaseModel


class CartItem(BaseModel):
    __tablename__ = "cart_products"

    cart_id = Column(UUID, ForeignKey("carts.id"), primary_key=True)
    cart = relationship("Cart", back_populates="items")

    item_number = Column(String(12), primary_key=True)
    quantity = Column(Integer, default=1)
