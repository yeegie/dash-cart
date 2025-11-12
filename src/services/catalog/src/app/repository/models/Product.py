from sqlalchemy import Column, String, Integer, UUID, Boolean, ForeignKey, Text, JSON, event, Float
from sqlalchemy.orm import relationship
from slugify import slugify

from .BaseModel import BaseModel, generate_uuid, generate_item_number


class Product(BaseModel):
    __tablename__ = "products"

    # Identifiers
    id = Column(UUID, primary_key=True, default=generate_uuid)
    item_number = Column(String(12), index=True, unique=True, default=generate_item_number)

    # General info
    name = Column(String(128), nullable=False, index=True)
    description = Column(Text)
    slug = Column(String(255), unique=True, index=True)

    # Pricing
    price = Column(Integer, nullable=False)
    old_price = Column(Integer)
    cost_price = Column(Integer)

    # Manufacturer and category
    manufacturer = Column(String(64))
    category_id = Column(UUID, ForeignKey("category.id"), nullable=False, index=True)
    category = relationship("Category", back_populates="products")

    # Images
    images = Column(JSON)            # image[0] is main

    # Physical attributes
    weight = Column(Integer)         # in grams
    dimensions = Column(String(50))  # format: "LxWxH" in millimeters -- 100x200x300
    characteristics = Column(JSON)   # additional technical specs or custom attributes

    # SEO
    meta_title = Column(String(255))
    meta_description = Column(String(512))

    # Rating
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    purchase_count = Column(Integer, default=0)

    quantity = Column(Integer, nullable=False)

    passport_check = Column(Boolean, default=False)

    def get_absolute_url(self) -> str:
        """Returns the canonical URL for this product."""
        return f"/catalog/{self.category.slug}/{self.slug}/"
    
    def __str__(self) -> str:
        return f"[{self.item_number}] {self.name} > {self.price}"
    

@event.listens_for(Product, 'before_insert')
def set_slug(mapper, connection, target):
    if not target.slug and target.name:
        target.slug = slugify(target.name)
