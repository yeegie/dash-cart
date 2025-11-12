from .IService import IService
from app.repositories.employee import EmployeeRepository
from app.repositories.schemas.employee import EmployeeSchema, GetEmployeeSchema, GetEmployeesListSchema
from logging import Logger
from uuid import UUID

class EmployeeService(IService):
    def __init__(
        self,
        repository: EmployeeRepository,
        logger: Logger,
    ):
        self.__repository = repository
        self.__logger = logger

    async def create(self, employee: EmployeeSchema) -> GetEmployeeSchema:
        return await self.__repository.create(employee)

    async def get_by_id(self, id: UUID) -> GetEmployeeSchema:
        return await self.__repository.get(id)

    async def get_or_create(self, id):
        # result = await self.__repository.get(id)
        
        # if result is None:
        #     self.create()
        pass 

    async def update(self, id: UUID, employee: EmployeeSchema) -> bool:
        return await self.__repository.update(id, employee)

    async def delete(self, id: UUID) -> bool:
        return await self.__repository.delete(id)

    async def list(self) -> GetEmployeesListSchema:
        return await self.__repository.list()