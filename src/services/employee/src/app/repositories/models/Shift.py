from .BaseModel import BaseModel, generate_uuid
from sqlalchemy import Column, DateTime, UUID, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .shift_statuses import ShiftStatuses


class Shift(BaseModel):
    __tablename__ = "shifts"

    id = Column(UUID, primary_key=True, default=generate_uuid)
    
    employee_id = Column(UUID, ForeignKey("employees.id"), nullable=False, index=True)
    employee = relationship("Employee", back_populates="shifts")

    desired_start_time = Column(DateTime, nullable=False, index=True)
    desired_end_time = Column(DateTime, nullable=False, index=True)

    confirmed_start_time = Column(DateTime, nullable=True, index=True)
    confirmed_end_time  = Column(DateTime, nullable=True, index=True)

    date = Column(Date, nullable=False, index=True)

    status = Column(Enum(ShiftStatuses), default=ShiftStatuses.SCHEDULED, nullable=False, index=True)

