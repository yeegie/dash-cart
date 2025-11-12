from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
from uuid import UUID


# Cart Item
class CartItemSchema(BaseModel):
    item_number: str = Field(..., max_length=12)
    quantity: int = Field(default=1)


class GetCartItemSchema(CartItemSchema):
    cart_id: UUID


class GetCartItemsSchema(BaseModel):
    cart_items: List[GetCartItemSchema]


# Cart
class CartSchema(BaseModel):
    user_id: UUID
    items: List[CartItemSchema]


class GetCartSchema(CartSchema):
    id: UUID


class GetCartsSchema(BaseModel):
    carts: List[GetCartSchema] | List
