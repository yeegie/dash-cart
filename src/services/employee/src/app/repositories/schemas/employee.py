from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from app.repositories.models.roles import EmployeeRoles
from datetime import date


class EmployeeSchema(BaseModel):
    fio: str
    role: EmployeeRoles
    telephone: str
    hire_date: date
    termination_date: date
    birth_date: date
    is_active: bool = True
    last_login: date


class GetEmployeeSchema(EmployeeSchema):
    id: UUID


class GetEmployeesListSchema(BaseModel):
    employees: List[GetEmployeeSchema]
