from .IRepository import IRepository
from sqlalchemy.ext.asyncio import AsyncSession
from logging import Logger
from .schemas.employee import EmployeeSchema, GetEmployeeSchema, GetEmployeesListSchema
from .models.Employee import Employee
from sqlalchemy import select, delete
from typing import Optional
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError


class EmployeeRepository(IRepository):
    def __init__(
        self,
        session: AsyncSession,
        logger: Logger
    ):
        self.__session = session
        self.__logger = logger

    async def create(self, employee: EmployeeSchema) -> GetEmployeeSchema:
        new_employee = Employee(**employee.model_dump(exclude_unset=True))
        
        self.__session.add(new_employee)
        await self.__session.commit()
        await self.__session.refresh(new_employee)

        self.__logger.info(f"New employee created - {new_employee.id}\n data: {new_employee.__dict__}")
        return GetEmployeeSchema(**new_employee.to_dict())

    async def get(self, id: UUID) -> Optional[GetEmployeeSchema]:
        result = await self.__session.execute(
            select(Employee)
            .where(Employee.id == id)
        )
        result = result.scalar_one_or_none()

        if result is None:
            return None
        
        return GetEmployeeSchema(**result.to_dict())

    async def update(self, id: UUID, employee: EmployeeSchema) -> bool:
        old_employee = await self.get(id)
        
        if old_employee is None:
            return False
        
        for field, value in employee.model_dump(exclude_unset=True).items():
            setattr(old_employee, field, value)

        try:
            await self.__session.commit()
            await self.__session.refresh(old_employee)
            self.__logger.info(f"Employee updated. ID={id}")
            return True
        except SQLAlchemyError as ex:
            self.__logger.error(f"An error occurred during update error. Employee id={id}: {ex}")
            await self.__session.rollback()
            return False

    async def delete(self, id: UUID) -> bool:
        try:
            result = await self.__session.execute(
                delete(Employee).where(Employee.id == id)
            )
            await self.__session.commit()
            return result.rowcount > 0  # Return True if deleted
        except SQLAlchemyError as ex:
            self.__logger.error(f"An error occurred during deletion employee: {ex}")
            await self.__session.rollback()
            return False

    async def list(self) -> GetEmployeesListSchema:
        try:
            result = await self.__session.execute(select(Employee))
            employees = result.scalars().all()
            employees_schemas = [GetEmployeeSchema(**employee.to_dict()) for employee in employees]
            return GetEmployeesListSchema(employees=employees_schemas)
        except SQLAlchemyError as ex:
            self.__logger.error(f"Failed to retrieve the employee list: {ex}")
            return GetEmployeesListSchema(employees=[])


