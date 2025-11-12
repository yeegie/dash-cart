from sqlalchemy import Column, UUID, String, Boolean, Date, Enum
from sqlalchemy.orm import relationship, backref
from .BaseModel import BaseModel, generate_uuid
from .roles import EmployeeRoles


class Employee(BaseModel):
    __tablename__ = "employees"

    id = Column(UUID, primary_key=True, default=generate_uuid)

    fio = Column(String, nullable=False)
    role = Column(Enum(EmployeeRoles), nullable=False)
    telephone = Column(String(20), nullable=False, unique=True, index=True)
    hire_date = Column(Date, nullable=False)
    termination_date = Column(Date)
    birth_date = Column(Date)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    last_login = Column(Date)

    shifts = relationship("Shift", back_populates=backref("employee"))
    