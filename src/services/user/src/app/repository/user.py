from .IRepository import IRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from .models.User import User
from .scheams.user import UserSchema, GetUserSchema, GetUsersSchema

from logging import Logger

from typing import Optional


class UserRepository(IRepository):
    def __init__(self, session: AsyncSession, logger: Logger) -> None:
        self.__session = session
        self.__logger = logger

    async def create(self, user: UserSchema) -> GetUserSchema:
        new_user = User(**user.model_dump(exclude_unset=True))
        self.__session.add(new_user)
        await self.__session.commit()
        await self.__session.refresh(new_user)

        self.__logger.info(f"New user created - {new_user.id}\n data: {new_user.__dict__}")
        return GetUserSchema(**new_user.to_dict())

    async def get(self, id: str) -> Optional[GetUserSchema]:
        result = await self.__session.execute(
            select(User)
            .where(User.id == id)
        )
        result = result.scalar_one_or_none()

        if result is None:
            return None
        
        return GetUserSchema(**result.to_dict())

    async def get_by_telephone(self, telephone: str) -> Optional[GetUserSchema]:
        result = await self.__session.execute(
            select(User)
            .where(User.telephone == telephone)
        )
        result = result.scalar_one_or_none()

        if result is None:
            return None
        
        return GetUserSchema(**result.to_dict())

    async def update(self, id: str, user: UserSchema) -> bool:
        old_user = await self.get(id)

        if not old_user:
            return False
        
        for field, value in user.model_dump(exclude_unset=True).items():
            setattr(old_user, field, value)

        try:
            await self.__session.commit()
            await self.__session.refresh(old_user)
            self.__logger.info(f"User updated. ID={id}")
            return True
        except SQLAlchemyError as ex:
            self.__logger.error(f"An error occurred during update error. User id={id}: {ex}")
            await self.__session.rollback()
            return False

    async def delete(self, id: str) -> bool:
        try:
            result = await self.__session.execute(
                delete(User).where(User.id == id)
            )
            await self.__session.commit()
            return result.rowcount > 0  # Return True if deleted
        except SQLAlchemyError as ex:
            self.__logger.error(f"An error occurred during deletion user: {ex}")
            await self.__session.rollback()
            return False
        
    async def list(self) -> GetUsersSchema:
        try:
            result = await self.__session.execute(select(User))
            users = result.scalars().all()
            users_schemas = [GetUserSchema(**user.to_dict()) for user in users]
            return GetUsersSchema(users=users_schemas)
        except SQLAlchemyError as ex:
            self.__logger.error(f"Failed to retrieve the users list: {ex}")
            return GetUsersSchema(users=[])
