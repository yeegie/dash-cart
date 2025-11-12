from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from app.repositories.models.shift_statuses import ShiftStatuses
from datetime import datetime, date


class ShiftSchema(BaseModel):
    employee_id: UUID
    desired_start_time: datetime
    desired_end_time: datetime
    confirmed_start_time: Optional[datetime] = None
    confirmed_end_time: Optional[datetime] = None
    date: date
    status: ShiftStatuses = ShiftStatuses.SCHEDULED


class GetShiftSchema(ShiftSchema):
    id: UUID


class GetShiftsListSchema(BaseModel):
    shifts: List[GetShiftSchema]
