from app.repository.client import ClientRepository
from app.repository.scheams.client import ClientSchema, GetClientSchema, GetClientsSchema
from app.exceptions.client_exceptions import ClientNotFound, ClientAlreadyExists
from logging import Logger
from uuid import UUID


class ClientService:
    def __init__(self, repository: ClientRepository, logger: Logger) -> None:
        self.__repository = repository
        self.__logger = logger

    async def create(self, client: ClientSchema) -> GetClientSchema:
        try:
            existing = await self.get_by_telephone(client.telephone)
        except ClientNotFound:
            existing = None

        if existing:
            raise ClientAlreadyExists(id=existing.id)

        return await self.__repository.create(client)

    async def get_by_id(self, id: UUID) -> GetClientSchema:
        client = await self.__repository.get(id)
        if client is None:
            raise ClientNotFound(id=id)

        return client

    async def get_by_telephone(self, telephone: str) -> GetClientSchema:
        client = await self.__repository.get_by_telephone(telephone)
        if client is None:
            raise ClientNotFound(telephone=telephone)

        return client

    async def update(self, id: UUID, client: ClientSchema) -> bool:
        return await self.__repository.update(id, client)

    async def delete(self, id: UUID) -> bool:
        return await self.__repository.delete(id)

    async def list(self) -> GetClientsSchema:
        return await self.__repository.list()
