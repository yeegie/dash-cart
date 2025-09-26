from fastapi import APIRouter, status
from app.repository.scheams.client import ClientSchema, GetClientSchema, GetClientsSchema
from app.services.client_service import ClientService
from uuid import UUID


class ClientRouter(APIRouter):
    def __init__(self, service: ClientService):
        super().__init__()
        self.__service = service

        self.add_api_route("/", self.create, methods=["POST"], response_model=GetClientSchema, status_code=status.HTTP_201_CREATED)
        self.add_api_route("/{id}", self.get_by_id, methods=["GET"], response_model=GetClientSchema)
        self.add_api_route("/telephone/{telephone}", self.get_by_telephone, methods=["GET"], response_model=GetClientSchema)
        self.add_api_route("/{id}", self.update, methods=["PUT"])
        self.add_api_route("/{id}", self.delete, methods=["DELETE"], status_code=status.HTTP_204_NO_CONTENT)
        self.add_api_route("/", self.list, methods=["GET"])

    async def create(self, client: ClientSchema):
        return await self.__service.create(client)

    async def get_by_id(self, id: UUID):
        return await self.__service.get_by_id(id)

    async def get_by_telephone(self, telephone: str):
        return await self.__service.get_by_telephone(telephone)

    async def update(self, id: UUID, client: ClientSchema):
        return await self.__service.update(id, client)

    async def delete(self, id: UUID):
        return await self.__service.delete(id)
    
    async def list(self):
        return await self.__service.list()
