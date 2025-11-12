from .base.abstract_product_repository import AbstractProductRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from .models.Product import Product
from .schemas.product import ProductSchema, GetProductSchema
from logging import Logger
from typing import Optional, List, Tuple, Dict
from uuid import UUID, uuid4
from app.exceptions.product import ProductAlreadyExists
import re


# Level 0: CRUD
# Level 1: Bulk
# Level 2: Useful operations

class ProductRepository(AbstractProductRepository):
    MAX_LIMIT = 100
    MAX_QUERY_LENGTH = 100
    ALLOWED_FILTERS = {
        "category_id", "query", "min_price", "max_price", "min_rating"
    }

    def __init__(self, session: AsyncSession, logger: Logger) -> None:
        self.__session = session
        self.__logger = logger

    # Base CRUD
    async def create(self, product: ProductSchema) -> GetProductSchema:
        new_product = Product(**product.model_dump(exclude_unset=True))
        try:
            self.__session.add(new_product)
            await self.__session.commit()
            await self.__session.refresh(new_product)
        except IntegrityError as ex:
            raise ProductAlreadyExists()
        
        self.__logger.info(f"New product created - {new_product}")
        return GetProductSchema(**new_product.to_dict())

    async def get(self, id: UUID) -> Optional[GetProductSchema]:
        result = await self.__session.execute(
            select(Product)
            .where(Product.id == id)
        )
        product = result.scalar_one_or_none()

        if product is None:
            return None
        
        return GetProductSchema(**product.to_dict())

    async def update(self, id: UUID, product: ProductSchema) -> Optional[GetProductSchema]:
        result = await self.__session.execute(
            select(Product)
            .where(Product.id == id)
        )

        old_product = result.scalar_one_or_none()

        if not old_product:
            return None
        
        for field, value in product.model_dump(exclude_unset=True).items():
            if hasattr(old_product, field):
                setattr(old_product, field, value)

        try:
            await self.__session.commit()
            await self.__session.refresh(old_product)
            self.__logger.info(f"Product updated. ID={id}")
            return GetProductSchema(**old_product.to_dict())
        except SQLAlchemyError as ex:
            self.__logger.error(f"An error occurred during update error. Product id={id}: {ex}")
            await self.__session.rollback()
            return None

    async def delete(self, id: UUID) -> bool:
        try:
            result = await self.__session.execute(
                delete(Product)
                .where(Product.id == id)
            )
            await self.__session.commit()
            return result.rowcount > 0  # Return True if deleted
        except (IntegrityError, OperationalError) as ex:
            await self.__session.rollback()
            self.__logger.error(f"Delete failed for product\nid: {id}\nex: {ex}")
            return False
        except SQLAlchemyError as ex:
            self.__logger.error(f"An error occurred during deletion product: {ex}")
            await self.__session.rollback()
            return False
        
    # Bulk
    async def bulk_create(self, products: List[ProductSchema]) -> List[GetProductSchema]:
        if products is None:
            return []
        
        try:
            product_models: List[Product] = []
            for product in products:
                model = Product(
                    id=uuid4(),
                    **product.model_dump(exclude={"id"})
                )
                product_models.append(model)
            
            self.__session.add_all(product_models)
            await self.__session.commit()
            
            return [
                GetProductSchema(**model.to_dict())
                for model in product_models
            ]
        except SQLAlchemyError as ex:
            await self.__session.rollback()
            self.__logger.error(f"Product bulk create operation failed: {ex}")
            raise
    
    async def bulk_update(self, updates: Dict[UUID, GetProductSchema]) -> int:
        if not updates:
            return 0
        
        try:
            ids = list(updates.keys())
            result = await self.__session.execute(
                select(Product).where(Product.id.in_(ids))
            )
            products = result.scalars().all()
            
            products_dict: Dict[UUID, Product] = {
                product.id: product for product in products
            }
            
            updated_count = 0
            for id, update_schema in updates.items():
                if id in products_dict:
                    product = products_dict[id]
                    data = update_schema.model_dump(exclude={"id"})
                    
                    for field, value in data.items():
                        if hasattr(product, field):
                            setattr(product, field, value)
                    
                    updated_count += 1
            
            await self.__session.commit()
            return updated_count
            
        except SQLAlchemyError as ex:
            await self.__session.rollback()
            self.__logger.error(f"Products bulk update failed for {len(updates)} items: {ex}")
            raise
    
    async def bulk_delete(self, ids: List[UUID]) -> int:
        if ids is None:
            return 0
        
        try:
            result = await self.__session.execute(
                delete(Product)
                .where(Product.id.in_(ids))
            )
            await self.__session.commit()
            self.__logger.info(f"Successfully deleted {result.rowcount} products")
            return result.rowcount
        except (IntegrityError, OperationalError) as ex:
            await self.__session.rollback()
            self.__logger.error(f"Bulk delete failed for products\nids: {ids}\nex: {ex}")
            return 0
        except SQLAlchemyError as ex:
            self.__logger.error(f"An error occurred during bulk deletion products\nids: {ids}\nex: {ex}")
            await self.__session.rollback()
            raise
        
    # Useful operations
    async def list(self, limit: int = 20, offset: int = 0) -> Tuple[List[GetProductSchema], int]:
        limit = min(max(1, limit), self.MAX_LIMIT)
        offset = max(0, offset)
        
        result = await self.__session.execute(
            select(Product)
            .limit(limit)
            .offset(offset)
        )
        products = result.scalars().all()
        product_schemas = [GetProductSchema(**product.to_dict()) for product in products]
        return (product_schemas, len(product_schemas))
    
    async def exists(self, id: UUID) -> bool:
        result = await self.__session.execute(
            select(Product)
            .where(Product.id == id)
        )
        product = result.scalar_one_or_none()

        if product is None:
            return False

        return True
    
    async def get_many(self, ids: List[UUID]) -> List[GetProductSchema]:
        if not ids:
            return []

        result = await self.__session.execute(
            select(Product)
            .where(Product.id.in_(ids))
            .limit(self.MAX_LIMIT)
        )
        products = result.scalars().all()

        return [
            GetProductSchema(**product.to_dict())
            for product in products
        ]
    
    async def partial_update(self, id: UUID, **fields) -> Optional[GetProductSchema]:
        result = await self.__session.execute(
            select(Product)
            .where(Product.id == id)
        )
        product = result.scalar_one_or_none()

        if product is None:
            return None
        
        for field, value in fields.items():
            if hasattr(product, field):
                setattr(product, field, value)

        return GetProductSchema(**product.to_dict())
    
    async def get_by_item_number(self, item_number: str) -> Optional[GetProductSchema]:
        result = await self.__session.execute(
            select(Product)
            .where(Product.item_number == item_number)
        )
        product = result.scalar_one_or_none()
        
        if product is None:
            return None
        
        return GetProductSchema(**product.to_dict())
    
    async def get_by_slug(self, slug: str) -> Optional[GetProductSchema]:
        result = await self.__session.execute(
            select(Product)
            .where(Product.slug == slug)
        )
        product = result.scalar_one_or_none()
        
        if product is None:
            return None
        
        return GetProductSchema(**product.to_dict())
    
    async def search_with_total(
            self,
            limit: int = 20,
            offset: int = 0,
            **filters,
    ) -> Tuple[List[GetProductSchema], int]:
        limit = min(max(1, limit), self.MAX_LIMIT)
        offset = max(0, offset)

        safe_filters = self._sanitize_filters(filters)

        stmt = select(Product)
        where = []

        if "category_id" in safe_filters:
            where.append(Product.category_id == safe_filters["category_id"])

        if "query" in safe_filters:
            query = safe_filters['query']
            if len(query) <= self.MAX_QUERY_LENGTH:
                safe_query = re.sub(r'([%_])', r'\\\1', query)
                where.append(Product.name.ilike(f"%{safe_query}%"))

        if "min_price" in safe_filters:
            min_price = safe_filters['min_price']
            if isinstance(min_price, (int, float)) and min_price >= 0:
                where.append(Product.price >= min_price)

        if 'max_price' in safe_filters:
            max_price = safe_filters['max_price']
            if isinstance(max_price, (int, float)) and max_price >= 0:
                where.append(Product.price <= max_price)
        
        if 'min_rating' in safe_filters:
            min_rating = safe_filters['min_rating']
            if isinstance(min_rating, (int, float)) and 0 <= min_rating <= 5:
                where.append(Product.rating >= min_rating)

        for bool_field in ['in_stock', 'is_active']:
            if bool_field in safe_filters:
                value = safe_filters[bool_field]
                if isinstance(value, bool):
                    where.append(getattr(Product, bool_field) == value)

        if where:
            stmt = stmt.where(and_(*where))
        
        stmt = stmt.offset(offset).limit(limit)
        result = await self.__session.execute(stmt)
        products = result.scalars().all()

        products_schemas = [GetProductSchema(**product.to_dict()) for product in products]

        return (products_schemas, len(products_schemas))

    def _sanitize_filters(self, filters: dict) -> dict:
        safe_filters = {}
        
        for key, value in filters.items():
            if key not in self.ALLOWED_FILTERS:
                continue
                
            if key in ['min_price', 'max_price', 'min_rating']:
                try:
                    safe_filters[key] = float(value) if value is not None else None
                except (TypeError, ValueError):
                    continue
                    
            elif key == 'query':
                if isinstance(value, str) and len(value) <= self.MAX_QUERY_LENGTH:
                    cleaned = re.sub(r'[^\w\s\-\.@]', '', value)
                    safe_filters[key] = cleaned.strip()
                    
            elif key in ['in_stock', 'is_active']:
                safe_filters[key] = bool(value)
                
        return safe_filters