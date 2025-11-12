from app.repository.category import CategoryRepository
from app.repository.product import ProductRepository
from app.repository.schemas.category import CategorySchema, GetCategorySchema
from app.exceptions.category import CategoryNotFound, CategoryAlreadyExists
from logging import Logger
from uuid import UUID
from typing import Optional, List, Dict, Tuple


class CategoryService:
    def __init__(
        self,
        repository: CategoryRepository,
        product_repository: ProductRepository,
        logger: Logger
    ) -> None:
        self.__repository = repository
        self.__logger = logger

    # Base CRUD
    async def create(self, category: GetCategorySchema) -> GetCategorySchema:
        return await self.__repository.create(category)
    
    async def get(self, id: UUID) -> Optional[GetCategorySchema]:
        return await self.__repository.get(id)
    
    async def update(self, id: UUID, category: CategorySchema) -> Optional[GetCategorySchema]:
        return await self.__repository.update(id, category)
    
    async def delete(self, id: UUID) -> bool:
        return await self.__repository.delete(id)
    
    # Bulk
    async def bulk_create(self, categories: List[CategorySchema]) -> List[GetCategorySchema]:
        return await self.__repository.bulk_create(categories)
    
    async def bulk_update(self, updates: Dict[UUID, CategorySchema]) -> int:
        return await self.__repository.bulk_update(updates)
    
    async def bulk_delete(self, ids: List[UUID]) -> int:
        return await self.__repository.bulk_delete(ids)
    
    # Useful operation
    async def list(self, limit: int = 20, offset: int = 0) -> Tuple[List[GetCategorySchema], int]:
        return await self.__repository.list(limit, offset)
    
    async def exists(self, id: UUID) -> bool:
        return await self.__repository.exists(id)
    
    async def get_many(self, ids: List[UUID]) -> List[GetCategorySchema]:
        return await self.__repository.get_many(ids)
    
    async def partial_update(self, id: UUID, **fields) -> Optional[GetCategorySchema]:
        return await self.__repository.partial_update(id, **fields)
    
    async def get_by_slug(self, slug: str) -> Optional[GetCategorySchema]:
        return await self.__repository.get_by_slug(slug)
