from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import date


class ClientSchema(BaseModel):
    name: Optional[str] = None
    telephone: str
    email: Optional[EmailStr] = None
    registered_at: date = Field(None, description="By default -> func.now()")


class GetClientSchema(ClientSchema):
    id: UUID


class GetClientsSchema(BaseModel):
    clients: List[GetClientSchema]
