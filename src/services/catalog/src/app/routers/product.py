from fastapi import APIRouter, status, Body, Query
from app.repository.schemas.product import ProductSchema, GetProductSchema
from app.services.product import ProductService
from uuid import UUID
from typing import List, Tuple, Dict, Optional


class ProductRouter(APIRouter):
    def __init__(self, service: ProductService):
        super().__init__()
        self.__service = service

        # Base CRUD
        self.add_api_route("/", self.create, methods=["POST"], response_model=GetProductSchema, status_code=status.HTTP_201_CREATED)
        self.add_api_route("/{id}", self.get_by_id, methods=["GET"], response_model=GetProductSchema)
        self.add_api_route("/{id}", self.update_by_id, methods=["PUT"])
        self.add_api_route("/{id}", self.delete_by_id, methods=["DELETE"], status_code=status.HTTP_204_NO_CONTENT)

        # Bulk
        self.add_api_route("/bulk/create", self.bulk_create, methods=["POST"], response_model=List[GetProductSchema])
        self.add_api_route("/bulk/update", self.bulk_update, methods=["PUT"])
        self.add_api_route("/bulk/delete", self.bulk_delete, methods=["DELETE"])

        # Useful operations
        self.add_api_route("/", self.list, methods=["GET"])
        self.add_api_route("/{id}/exists/", self.exists, methods=["GET"])
        self.add_api_route("/batch", self.get_many, methods=["GET"])
        # self.add_api_route("/{id}", self.partial_update, methods=["PATCH"])
        self.add_api_route("/item_number/{id}", self.get_by_item_number, methods=["GET"], response_model=GetProductSchema)
        self.add_api_route("/slug/{slug}", self.get_by_slug, methods=["GET"], response_model=GetProductSchema)
        # self.add_api_route("/search", self.search_with_total, methods=["GET"])

    # Base CRUD
    async def create(self, product: ProductSchema = Body(..., embed=True)):
        return await self.__service.create(product)
    
    async def get_by_id(self, id: UUID):
        return await self.__service.get(id)
    
    async def update_by_id(self, id: UUID, product: ProductSchema = Body(..., embed=True)):
        return await self.__service.update(id, product)
    
    async def delete_by_id(self, id: UUID):
        return await self.__service.delete(id)
    
    # Bulk
    async def bulk_create(self, products: List[ProductSchema] = Body(..., embed=True)) -> List[GetProductSchema]:
        return await self.__service.bulk_create(products)
    
    async def bulk_update(self, updates: Dict[UUID, ProductSchema] = Body(..., embed=True)) -> int:
        return await self.__service.bulk_update(updates)
    
    async def bulk_delete(self, ids: List[UUID] = Body(..., embed=True)) -> int:
        return await self.__service.bulk_delete(ids)
    
    # Useful operations
    async def list(self, limit: int = 20, offset: int = 0):
        categories, total = await self.__service.list(limit, offset)
        return {
            "products": categories,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    
    async def exists(self, id: UUID) -> bool:
        return await self.__service.exists(id)
    
    async def get_many(self, ids: List[UUID] = Query(...)):
        return await self.__service.get_many(ids)
    
    # async def partial_update(self, id: UUID, **fields):
    #     pass

    async def get_by_item_number(self, item_number: str):
        return await self.__service.get_by_item_number(item_number)
    
    async def get_by_slug(self, slug: str):
        return await self.__service.get_by_slug(slug)
    
    # async def search_with_total(
    #     self,
    #     limit: int = Query(20, ge=1, le=100),
    #     offset: int = Query(0, ge=0),
    #     category_id: Optional[UUID] = Query(None),
    #     query: Optional[str] = Query(None, max_length=100),
    #     min_price: Optional[int] = Query(None, ge=0),
    #     max_price: Optional[int] = Query(None, ge=0),
    #     min_rating: Optional[int] = Query(None, ge=0, le=5),
    # ) -> Dict:
    #     pass



    




    
    
