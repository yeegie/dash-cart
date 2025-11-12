from .IService import IService
from app.repositories.shift import ShiftRepository
from app.repositories.schemas.shift import ShiftSchema, GetShiftSchema, GetShiftsListSchema
from logging import Logger
from uuid import UUID

class ShiftService(IService):
    def __init__(
        self,
        repository: ShiftRepository,
        logger: Logger,
    ):
        self.__repository = repository
        self.__logger = logger

    async def create(self, shift: ShiftSchema) -> GetShiftSchema:
        return await self.__repository.create(shift)

    async def get_by_id(self, id: UUID) -> GetShiftSchema:
        return await self.__repository.get(id)

    async def get_or_create(self, id):
        # result = await self.__repository.get(id)
        
        # if result is None:
        #     self.create()
        pass 

    async def update(self, id: UUID, shift: ShiftSchema) -> bool:
        return await self.__repository.update(id, shift)

    async def delete(self, id) -> bool:
        return await self.__repository.delete(id)

    async def list(self) -> GetShiftsListSchema:
        return await self.__repository.list()
