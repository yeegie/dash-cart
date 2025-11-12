from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


class CategorySchema(BaseModel):
    name: str = Field(..., max_length=32)
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
    is_active: bool = False


class GetCategorySchema(CategorySchema):
    id: UUID
    slug: str
