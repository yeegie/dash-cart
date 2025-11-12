from fastapi import APIRouter, Body, status
from app.repository.scheams.cart import CartSchema, GetCartSchema, GetCartsSchema
from app.repository.cart import CartRepository
from uuid import UUID


class CartRouter(APIRouter):
    def __init__(self, repository: CartRepository):
        super().__init__()
        self.__repository = repository

        self.add_api_route("/", self.create, methods=["POST"], response_model=GetCartSchema, status_code=status.HTTP_201_CREATED)

        self.add_api_route("/{id}", self.get_by_id, methods=["GET"], response_model=GetCartSchema)
        self.add_api_route("/user/{user_id}", self.get_by_user_id, methods=["GET"], response_model=GetCartSchema)
        
        self.add_api_route("/{user_id}", self.update_by_user_id, methods=["PUT"], response_model=GetCartSchema)
        self.add_api_route("/{id}", self.delete, methods=["DELETE"], status_code=status.HTTP_204_NO_CONTENT)

        self.add_api_route("/item/remove/{}")
        
        self.add_api_route("/", self.list, methods=["GET"])

    async def create(self, product: CartSchema = Body(..., embed=True)):
        return await self.__repository.create(product)

    async def get_by_id(self, id: UUID):
        return await self.__repository.get_by_id(id)
    
    async def get_by_user_id(self, user_id: UUID):
        return await self.__repository.get_by_user_id(user_id)

    async def update_by_user_id(self, user_id: UUID, cart: CartSchema = Body(..., embed=True)):
        return await self.__repository.update(user_id, cart)
    
    async def add_item(self, user_id: UUID = Body(..., embed=True), item_number: str = Body(..., embed=True)):
        return await self.__repository.add_item(user_id, item_number)

    async def remove_item(self, user_id: UUID = Body(..., embed=True), item_number: str = Body(..., embed=True)):
        return await self.__repository.remove_item(user_id, item_number)

    async def delete(self, id: UUID):
        return await self.__repository.delete(id)

    async def list(self):
        return await self.__repository.list()
