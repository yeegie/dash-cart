from sqlalchemy.orm.collections import InstrumentedList
import secrets
import uuid

from .base import Base


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


def generate_item_number() -> str:
    return str(secrets.randbelow(10**12))


class BaseModel(Base):
    __abstract__ = True

    def to_dict(self) -> dict:
        data = dict()
        for k, v in self.__dict__.items():
            if k.startswith("_"):
                continue
            elif isinstance(v, Base):
                v = v.to_dict()
            elif isinstance(v, InstrumentedList):
                v = [item.to_dict() for item in v]
            data[k] = v
        return data
