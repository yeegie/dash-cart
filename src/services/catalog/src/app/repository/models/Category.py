from sqlalchemy import Column, UUID, String, Boolean, ForeignKey, Text, event
from sqlalchemy.orm import relationship, backref
from slugify import slugify

from .BaseModel import BaseModel, generate_uuid


class Category(BaseModel):
    __tablename__ = "category"

    id = Column(UUID, primary_key=True, default=generate_uuid)

    name = Column(String(32), nullable=False)
    description = Column(Text, nullable=True)
    slug = Column(String(255), index=True, unique=True, nullable=False)

    parent_id = Column(UUID, ForeignKey("category.id"), nullable=True, index=True)
    subcategories = relationship(
        "Category",
        backref=backref("parent", remote_side=[id]),
        cascade="all, delete-orphan"
    )

    products = relationship("Product", back_populates="category")

    is_active = Column(Boolean, nullable=False, default=False, index=True)

    def get_full_path(self) -> str:
        path = []
        current = self
        while current:
            path.append(current.name)
            current = current.parent
        return ' > '.join(reversed(path))
    
    def __str__(self) -> str:
        return f"[{self.id}] {self.name}"


@event.listens_for(Category, 'before_insert')
def set_slug(mapper, connection, target):
    if not target.slug and target.name:
        target.slug = slugify(target.name)
