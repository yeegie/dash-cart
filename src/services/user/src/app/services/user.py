from app.repository.user import UserRepository
from app.repository.scheams.user import UserSchema, GetUserSchema, GetUsersSchema
from app.exceptions.user_exceptions import UserNotFound, UserAlreadyExists
from logging import Logger
from uuid import UUID


class UserService:
    def __init__(self, repository: UserRepository, logger: Logger) -> None:
        self.__repository = repository
        self.__logger = logger

    async def create(self, user: UserSchema) -> GetUserSchema:
        try:
            existing = await self.get_by_telephone(user.telephone)
        except UserNotFound:
            existing = None

        if existing:
            raise UserAlreadyExists(id=existing.id)

        return await self.__repository.create(user)

    async def get_by_id(self, id: UUID) -> GetUserSchema:
        user = await self.__repository.get(id)
        if user is None:
            raise UserNotFound(id=id)

        return user

    async def get_or_create(self, telephone: str) -> GetUserSchema:
        try:
            user = await self.get_by_telephone(telephone)

            if user is None:
                raise UserNotFound(telephone=telephone)

            return user
        except UserNotFound:
            return await self.create(UserSchema(telephone=telephone))
        except Exception as ex:
            raise

    async def get_by_telephone(self, telephone: str) -> GetUserSchema:
        user = await self.__repository.get_by_telephone(telephone)
        if user is None:
            raise UserNotFound(telephone=telephone)

        return user

    async def update(self, id: UUID, user: UserSchema) -> bool:
        return await self.__repository.update(id, user)

    async def delete(self, id: UUID) -> bool:
        return await self.__repository.delete(id)

    async def list(self) -> GetUsersSchema:
        return await self.__repository.list()
