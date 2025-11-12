from fastapi import APIRouter, status, Body
from app.services.shift import ShiftService
from app.repositories.schemas.shift import ShiftSchema, GetShiftSchema, GetShiftsListSchema
from uuid import UUID


class ShiftRouter(APIRouter):
    def __init__(
            self,
            service: ShiftService
        ):
        super().__init__()
        self.__service = service

        self.add_api_route("/", self.create, methods=["POST"], response_model=GetShiftSchema, status_code=status.HTTP_201_CREATED)

        self.add_api_route("/{id}", self.get_by_id, methods=["GET"], response_model=GetShiftSchema)
        self.add_api_route("/{id}", self.update, methods=["PUT"])
        self.add_api_route("/{id}", self.delete, methods=["DELETE"])

        self.add_api_route("/", self.list, methods=["GET"], response_model=GetShiftsListSchema)

    async def create(self, shift: ShiftSchema = Body(..., embed=True)):
        return await self.__service.create(shift)

    async def get_by_id(self, id: UUID):
        return await self.__service.get_by_id(id)

    async def update(self, id: UUID, shift: ShiftSchema = Body(..., embed=True)):
        return await self.__service.update(id, shift)
    
    async def delete(self, id: UUID):
        return await self.__service.delete(id)
    
    async def list(self):
        return await self.__service.list()