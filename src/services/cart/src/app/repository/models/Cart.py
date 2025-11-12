from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.orm import relationship, backref

from .BaseModel import BaseModel, generate_uuid


class Cart(BaseModel):
    __tablename__ = "carts"

    id = Column(UUID, primary_key=True, default=generate_uuid)
    user_id = Column(UUID, nullable=False, index=True)

    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
