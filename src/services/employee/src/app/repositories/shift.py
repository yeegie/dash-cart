from .IRepository import IRepository
from sqlalchemy.ext.asyncio import AsyncSession
from logging import Logger
from .schemas.shift import ShiftSchema, GetShiftSchema, GetShiftsListSchema
from .models.Shift import Shift
from sqlalchemy import select, delete
from typing import Optional
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError


class ShiftRepository(IRepository):
    def __init__(
        self,
        session: AsyncSession,
        logger: Logger
    ):
        self.__session = session
        self.__logger = logger

    async def create(self, shift: ShiftSchema) -> GetShiftSchema:
        new_shift = Shift(**shift.model_dump(exclude_unset=True))
        
        self.__session.add(new_shift)
        await self.__session.commit()
        await self.__session.refresh(new_shift)

        self.__logger.info(f"New shift scheduled - {new_shift.id}\n data: {new_shift.__dict__}")
        return GetShiftSchema(**new_shift.to_dict())

    async def get(self, id: UUID) -> Optional[GetShiftSchema]:
        result = await self.__session.execute(
            select(Shift)
            .where(Shift.id == id)
        )
        result = result.scalar_one_or_none()

        if result is None:
            return None
        
        return GetShiftSchema(**result.to_dict())

    async def update(self, id: UUID, shift: ShiftSchema) -> bool:
        old_shift = await self.get(id)
        
        if old_shift is None:
            return False
        
        for field, value in shift.model_dump(exclude_unset=True).items():
            setattr(old_shift, field, value)

        try:
            await self.__session.commit()
            await self.__session.refresh(old_shift)
            self.__logger.info(f"Shift updated. ID={id}")
            return True
        except SQLAlchemyError as ex:
            self.__logger.error(f"An error occurred during update error. Shift id={id}: {ex}")
            await self.__session.rollback()
            return False

    async def delete(self, id: UUID) -> bool:
        try:
            result = await self.__session.execute(
                delete(Shift).where(Shift.id == id)
            )
            await self.__session.commit()
            return result.rowcount > 0  # Return True if deleted
        except SQLAlchemyError as ex:
            self.__logger.error(f"An error occurred during deletion shift: {ex}")
            await self.__session.rollback()
            return False

    async def list(self) -> GetShiftsListSchema:
        try:
            result = await self.__session.execute(select(Shift))
            shifts = result.scalars().all()
            shifts_schemas = [GetShiftSchema(**shift.to_dict()) for shift in shifts]
            return GetShiftsListSchema(shifts=shifts_schemas)
        except SQLAlchemyError as ex:
            self.__logger.error(f"Failed to retrieve the shift list: {ex}")
            return GetShiftsListSchema(shifts=[])