from fastapi import APIRouter, status, Body, Query
from app.repository.schemas.category import CategorySchema, GetCategorySchema
from app.services.category import CategoryService
from uuid import UUID
from typing import List, Dict, Optional


class CategoryRouter(APIRouter):
    def __init__(self, service: CategoryService):
        super().__init__()
        self.__service = service

        # Base CRUD
        self.add_api_route("/", self.create, methods=["POST"], response_model=GetCategorySchema, status_code=status.HTTP_201_CREATED)
        self.add_api_route("/{id}", self.get_by_id, methods=["GET"], response_model=GetCategorySchema)
        self.add_api_route("/{id}", self.update_by_id, methods=["PUT"], response_model=GetCategorySchema)
        self.add_api_route("/{id}", self.delete_by_id, methods=["DELETE"], status_code=status.HTTP_204_NO_CONTENT)

        # Bulk
        self.add_api_route("/bulk/create", self.bulk_create, methods=["POST"], response_model=List[GetCategorySchema])
        self.add_api_route("/bulk/update", self.bulk_update, methods=["PUT"])
        self.add_api_route("/bulk/delete", self.bulk_delete, methods=["DELETE"])

        # Useful operations
        self.add_api_route("/", self.list, methods=["GET"])
        self.add_api_route("/{id}/exists", self.exists, methods=["GET"], response_model=bool)
        self.add_api_route("/batch", self.get_many, methods=["POST"], response_model=List[GetCategorySchema])
        self.add_api_route("/slug/{slug}", self.get_by_slug, methods=["GET"], response_model=GetCategorySchema)

    # Base CRUD
    async def create(self, category: CategorySchema = Body(..., embed=True)) -> GetCategorySchema:
        return await self.__service.create(category)
    
    async def get_by_id(self, id: UUID) -> GetCategorySchema:
        return await self.__service.get(id)
    
    async def update_by_id(self, id: UUID, category: CategorySchema = Body(..., embed=True)) -> GetCategorySchema:
        return await self.__service.update(id, category)
    
    async def delete_by_id(self, id: UUID) -> None:
        await self.__service.delete(id)
    
    # Bulk
    async def bulk_create(self, categories: List[CategorySchema] = Body(..., embed=True)) -> List[GetCategorySchema]:
        return await self.__service.bulk_create(categories)
    
    async def bulk_update(self, updates: Dict[UUID, CategorySchema] = Body(..., embed=True)) -> int:
        return await self.__service.bulk_update(updates)
    
    async def bulk_delete(self, ids: List[UUID] = Body(..., embed=True)) -> int:
        return await self.__service.bulk_delete(ids)
    
    # Useful operations
    async def list(
        self, 
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0)
    ):
        categories, total = await self.__service.list(limit, offset)
        return {
            "categories": categories,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    
    async def exists(self, id: UUID) -> bool:
        return await self.__service.exists(id)
    
    async def get_many(self, ids: List[UUID] = Body(..., embed=True)) -> List[GetCategorySchema]:
        return await self.__service.get_many(ids)
    
    async def get_by_slug(self, slug: str) -> GetCategorySchema:
        return await self.__service.get_by_slug(slug)