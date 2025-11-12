from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import date


class UserSchema(BaseModel):
    name: Optional[str] = None
    telephone: str
    email: Optional[EmailStr] = None
    registered_at: date = Field(None, description="By default -> func.now()")


class GetUserSchema(UserSchema):
    id: UUID


class GetUsersSchema(BaseModel):
    users: List[GetUserSchema]
