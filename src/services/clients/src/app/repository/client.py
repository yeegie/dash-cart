from .IRepository import IRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from .models.Client import Client
from .scheams.client import ClientSchema, GetClientSchema, GetClientsSchema

from logging import Logger

from typing import Optional


class ClientRepository(IRepository):
    def __init__(self, session: AsyncSession, logger: Logger) -> None:
        self.__session = session
        self.__logger = logger

    async def create(self, client: ClientSchema) -> GetClientSchema:
        new_client = Client(**client.model_dump(exclude_unset=True))
        self.__session.add(new_client)
        await self.__session.commit()
        await self.__session.refresh(new_client)

        return new_client

    async def get(self, id: str) -> Optional[GetClientSchema]:
        result = await self.__session.execute(
            select(Client)
            .where(Client.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_telephone(self, telephone: str) -> Optional[GetClientSchema]:
        result = await self.__session.execute(
            select(Client)
            .where(Client.telephone == telephone)
        )
        return result.scalar_one_or_none()

    async def update(self, id: str, client: ClientSchema) -> bool:
        old_client = await self.get(id)

        if not old_client:
            return False
        
        for field, value in client.model_dump(exclude_unset=True).items():
            setattr(old_client, field, value)

        try:
            await self.__session.commit()
            await self.__session.refresh(old_client)
            self.__logger.info(f"[Client] client_id={id} UPDATED")
            return True
        except SQLAlchemyError as ex:
            self.__logger.error(f"[Client] UPDATE ERROR: {ex}")
            await self.__session.rollback()
            return False

    async def delete(self, id: str) -> bool:
        try:
            result = await self.__session.execute(
                delete(Client).where(Client.id == id)
            )
            await self.__session.commit()
            return result.rowcount > 0  # Return True if deleted
        except SQLAlchemyError as ex:
            self.__logger.error(f"[Client] DELETION ERROR: {ex}")
            await self.__session.rollback()
            return False
        
    async def list(self) -> GetClientsSchema:
        try:
            result = await self.__session.execute(select(Client))
            return result.scalars().all()
        except SQLAlchemyError as ex:
            self.__logger.error(f"[Client] FETCH ALL ERROR: {ex}")
            return [] 
