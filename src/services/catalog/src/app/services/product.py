from app.repository.product import ProductRepository
from app.repository.schemas.product import ProductSchema, GetProductSchema
from app.exceptions.product import ProductNotFound, ProductAlreadyExists
from logging import Logger
from uuid import UUID
from typing import Optional, List, Dict, Tuple


class ProductService:
    def __init__(
        self,
        repository: ProductRepository,
        logger: Logger
    ) -> None:
        self.__repository = repository
        self.__logger = logger

    async def create(self, category: GetProductSchema) -> GetProductSchema:
        return await self.__repository.create(category)
    
    async def get(self, id: UUID) -> Optional[GetProductSchema]:
        return await self.__repository.get(id)
    
    async def update(self, id: UUID, category: ProductSchema) -> Optional[GetProductSchema]:
        return await self.__repository.update(id, category)
    
    async def delete(self, id: UUID) -> bool:
        return await self.__repository.delete(id)
    
    # Bulk
    async def bulk_create(self, categories: List[ProductSchema]) -> List[GetProductSchema]:
        return await self.__repository.bulk_create(categories)
    
    async def bulk_update(self, updates: Dict[UUID, ProductSchema]) -> int:
        return await self.__repository.bulk_update(updates)
    
    async def bulk_delete(self, ids: List[UUID]) -> int:
        return await self.__repository.bulk_delete(ids)
    
    # Useful operation
    async def list(self, limit: int = 20, offset: int = 0) -> Tuple[List[GetProductSchema], int]:
        return await self.__repository.list(limit, offset)
    
    async def exists(self, id: UUID) -> bool:
        return await self.__repository.exists(id)

    async def get_many(self, ids: List[UUID]) -> List[GetProductSchema]:
        return await self.__repository.get_many(ids)
    
    async def partial_update(self, id: UUID, **fields) -> Optional[GetProductSchema]:
        return await self.__repository.partial_update(id, fields)
    
    async def get_by_item_number(self, item_number: str) -> Optional[GetProductSchema]:
        return await self.__repository.get_by_item_number(item_number)
    
    async def get_by_slug(self, slug: str) -> Optional[GetProductSchema]:
        return await self.__repository.get_by_slug(slug)
    
    async def search_with_total(self, limit: int = 20, offset: int = 0, **filters) -> Tuple[List[GetProductSchema], int]:
        return await self.__repository.search_with_total(limit, offset, **filters)
