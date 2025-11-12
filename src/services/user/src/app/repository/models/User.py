from sqlalchemy import Column, String, Date, UUID, func, JSON
from .BaseModel import BaseModel, generate_uuid


class User(BaseModel):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=True)
    telephone = Column(String(20), nullable=False, unique=True)
    email = Column(String(255), nullable=True, unique=True)
    registered_at = Column(Date(), nullable=False, default=func.now())
