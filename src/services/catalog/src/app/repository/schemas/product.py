from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
from uuid import UUID


class ProductSchema(BaseModel):    
    name: str = Field(..., min_length=1, max_length=128)
    description: Optional[str] = None
    
    price: int = Field(..., gt=0)
    old_price: Optional[int] = Field(None, ge=0)
    cost_price: Optional[int] = Field(None, ge=0)
    
    images: Optional[List[str]] = None
    
    weight: Optional[float] = Field(None, ge=0)
    dimensions: Optional[str] = Field(None, max_length=50)
    characteristics: Optional[Dict] = None
    
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=512)

    rating: Optional[float] = Field(default=0.0, le=5)
    review_count: Optional[int] = 0
    purchase_count: Optional[int] = 0
    
    manufacturer: str = Field(None, max_length=64)
    category_id: UUID

    quantity: int = 0
    
    passport_check: bool = False


class GetProductSchema(ProductSchema):
    id: UUID
    item_number: str
    slug: str

