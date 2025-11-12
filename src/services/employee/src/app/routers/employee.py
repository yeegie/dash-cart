from fastapi import APIRouter, status, Body
from app.services.employee import EmployeeService
from app.repositories.schemas.employee import EmployeeSchema, GetEmployeeSchema, GetEmployeesListSchema
from uuid import UUID


class EmployeeRouter(APIRouter):
    def __init__(
            self,
            service: EmployeeService
        ):
        super().__init__()
        self.__service = service

        self.add_api_route("/", self.create, methods=["POST"], response_model=GetEmployeeSchema, status_code=status.HTTP_201_CREATED)

        self.add_api_route("/{id}", self.get_by_id, methods=["GET"], response_model=GetEmployeeSchema)
        self.add_api_route("/{id}", self.update, methods=["PUT"])
        self.add_api_route("/{id}", self.delete, methods=["DELETE"])

        self.add_api_route("/", self.list, methods=["GET"], response_model=GetEmployeesListSchema)

    async def create(self, employee: EmployeeSchema = Body(..., embed=True)):
        return await self.__service.create(employee)

    async def get_by_id(self, id: UUID):
        return await self.__service.get_by_id(id)

    async def update(self, id: UUID, employee: EmployeeSchema = Body(..., embed=True)):
        return await self.__service.update(id, employee)
    
    async def delete(self, id: UUID):
        return await self.__service.delete(id)
    
    async def list(self):
        return await self.__service.list()
