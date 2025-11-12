from fastapi import APIRouter, status, Body
from app.repository.scheams.user import UserSchema, GetUserSchema, GetUsersSchema
from app.services.user import UserService
from uuid import UUID


class UserRouter(APIRouter):
    def __init__(self, service: UserService):
        super().__init__()
        self.__service = service

        # CRUD
        self.add_api_route("/", self.create, methods=["POST"], response_model=GetUserSchema, status_code=status.HTTP_201_CREATED)
        self.add_api_route("/{id}", self.get_by_id, methods=["GET"], response_model=GetUserSchema)
        self.add_api_route("/telephone/{telephone}", self.get_by_telephone, methods=["GET"], response_model=GetUserSchema)
        self.add_api_route("/{id}", self.update, methods=["PUT"], response_model=GetUserSchema)
        self.add_api_route("/{id}", self.delete, methods=["DELETE"], status_code=status.HTTP_204_NO_CONTENT)
        
        self.add_api_route("/", self.list, methods=["GET"], response_model=GetUsersSchema)

        # For auth-service
        self.add_api_route("/get-or-create", self.get_or_create, methods=["POST"], response_model=GetUserSchema)

    async def create(self, user: UserSchema):
        return await self.__service.create(user)

    async def get_by_id(self, id: UUID):
        return await self.__service.get_by_id(id)
    
    async def get_or_create(self, telephone: str = Body(..., embed=True)):
        return await self.__service.get_or_create(telephone)

    async def get_by_telephone(self, telephone: str):
        return await self.__service.get_by_telephone(telephone)

    async def update(self, id: UUID, user: UserSchema):
        return await self.__service.update(id, user)

    async def delete(self, id: UUID):
        return await self.__service.delete(id)
    
    async def list(self):
        return await self.__service.list()
