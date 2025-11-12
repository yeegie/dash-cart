from .base.abstract_repository import AbstractRepository
from .base.mixins.bulk import MixinBulk

from .schemas.category import CategorySchema, GetCategorySchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy import select, delete
from .models.Category import Category
from typing import Optional, Tuple, List, Dict
from uuid import UUID, uuid4
from logging import Logger
from app.exceptions.category import CategoryAlreadyExists


# Level 0: CRUD
# Level 1: Bulk
# Level 2: Useful operations

class CategoryRepository(AbstractRepository, MixinBulk):
    MAX_LIMIT = 100
    
    def __init__(self, session: AsyncSession, logger: Logger) -> None:
        self.__session = session
        self.__logger = logger

    # Base CRUD
    async def create(self, category: CategorySchema) -> GetCategorySchema:
        new_category = Category(**category.model_dump(exclude_unset=True))
        try:
            self.__session.add(new_category)
            await self.__session.commit()
            await self.__session.refresh(new_category)
        except IntegrityError as ex:
            raise CategoryAlreadyExists()

        self.__logger.info(
            f"[Category] New category created - {new_category.name}\ndata: {new_category}")
        return GetCategorySchema(**new_category.to_dict())

    async def get(self, id: UUID) -> Optional[GetCategorySchema]:
        result = await self.__session.execute(
            select(Category)
            .where(Category.id == id)
        )
        category = result.scalar_one_or_none()

        if category is None:
            return None

        return GetCategorySchema(**category.to_dict())

    async def update(self, id: UUID, category: CategorySchema) -> Optional[GetCategorySchema]:
        result = await self.__session.execute(
            select(Category)
            .where(Category.id == id)
        )

        old_category = result.scalar_one_or_none()

        if not old_category:
            return None

        for field, value in category.model_dump(exclude_unset=True).items():
            if hasattr(old_category, field):
                setattr(old_category, field, value)

        try:
            await self.__session.commit()
            await self.__session.refresh(old_category)
            self.__logger.info(f"Category updated. ID={id}")
            return GetCategorySchema(**old_category.to_dict())
        except SQLAlchemyError as ex:
            self.__logger.error(
                f"An error occurred during update error. Category id={id}: {ex}")
            await self.__session.rollback()
            return None

    async def delete(self, id: UUID) -> bool:
        try:
            result = await self.__session.execute(
                delete(Category)
                .where(Category.id == id)
            )
            await self.__session.commit()
            self.__logger.info(f"Successfully deleted category with id {id}")
            return result.rowcount > 0  # Return True if deleted
        except (IntegrityError, OperationalError) as ex:
            await self.__session.rollback()
            self.__logger.error(f"Delete failed for category\nid: {id}\nex: {ex}")
            return False
        except SQLAlchemyError as ex:
            self.__logger.error(f"An error occurred during deletion category: {ex}")
            await self.__session.rollback()
            raise

    # Bulk
    async def bulk_create(self, categories: List[CategorySchema]) -> List[GetCategorySchema]:
        if categories is None:
            return []
        
        try:
            category_models: List[Category] = []
            for category in categories:
                model = Category(
                    id=uuid4(),
                    **category.model_dump(exclude={"id"})
                )
                category_models.append(model)
            
            self.__session.add_all(category_models)
            await self.__session.commit()
            
            return [
                GetCategorySchema(**model.to_dict())
                for model in category_models
            ]
        except SQLAlchemyError as ex:
            await self.__session.rollback()
            self.__logger.error(f"Categories bulk create operation failed: {ex}")
            raise

    async def bulk_update(self, updates: Dict[UUID, CategorySchema]) -> int:
        if not updates:
            return 0
        
        try:
            ids = list(updates.keys())
            result = await self.__session.execute(
                select(Category).where(Category.id.in_(ids))
            )
            categories = result.scalars().all()
            
            categories_dict: Dict[UUID, Category] = {
                category.id: category for category in categories
            }
            
            updated_count = 0
            for id, update_schema in updates.items():
                if id in categories_dict:
                    category = categories_dict[id]
                    data = update_schema.model_dump(exclude={"id"})
                    
                    for field, value in data.items():
                        if hasattr(category, field):
                            setattr(category, field, value)
                    
                    updated_count += 1
            
            await self.__session.commit()
            return updated_count
            
        except SQLAlchemyError as ex:
            await self.__session.rollback()
            self.__logger.error(f"Categories bulk update failed for {len(updates)} items: {ex}")
            raise
    
    async def bulk_delete(self, ids: List[UUID]) -> int:
        if ids is None:
            return 0
        
        try:
            result = await self.__session.execute(
                delete(Category)
                .where(Category.id.in_(ids))
            )
            await self.__session.commit()
            self.__logger.info(f"Successfully deleted {result.rowcount} categories")
            return result.rowcount
        except (IntegrityError, OperationalError) as ex:
            await self.__session.rollback()
            self.__logger.error(f"Bulk delete failed for categories\nids: {ids}\nex: {ex}")
            return 0
        except SQLAlchemyError as ex:
            self.__logger.error(f"An error occurred during bulk deletion categories\nids: {ids}\nex: {ex}")
            await self.__session.rollback()
            raise

    # Useful operation
    async def list(self, limit: int = 20, offset: int = 0) -> Tuple[List[GetCategorySchema], int]:
        limit = min(max(1, limit), self.MAX_LIMIT)
        offset = max(0, offset)

        result = await self.__session.execute(
            select(Category)
            .limit(limit)
            .offset(offset)
        )
        categories = result.scalars().all()
        category_schemas = [GetCategorySchema(**category.to_dict()) for category in categories]
        return (category_schemas, len(category_schemas))

    async def exists(self, id: UUID) -> bool:
        result = await self.__session.execute(
            select(Category)
            .where(Category.id == id)
        )
        category = result.scalar_one_or_none()

        if category is None:
            return False

        return True

    async def get_many(self, ids: List[UUID]) -> List[GetCategorySchema]:
        if not ids:
            return []

        result = await self.__session.execute(
            select(Category)
            .where(Category.id.in_(ids))
            .limit(self.MAX_LIMIT)
        )
        categories = result.scalars().all()

        return [
            GetCategorySchema(**category.to_dict())
            for category in categories
        ]

    async def partial_update(self, id: UUID, **fields) -> Optional[GetCategorySchema]:
        result = await self.__session.execute(
            select(Category)
            .where(Category.id == id)
        )
        category = result.scalar_one_or_none()

        if category is None:
            return None
        
        for field, value in fields.items():
            if hasattr(category, field):
                setattr(category, field, value)

        return GetCategorySchema(**category.to_dict())

    async def get_by_slug(self, slug: str) -> Optional[GetCategorySchema]:
        result = await self.__session.execute(
            select(Category)
            .where(Category.slug == slug)
        )
        category = result.scalar_one_or_none()

        if category is None:
            return None

        return GetCategorySchema(**category.to_dict())
