from enum import Enum

class ShiftStatuses(Enum):
    SCHEDULED = "запланированный"
    WORKED_OUT = "отработано"
    NOT_WORKED = "невыход"
