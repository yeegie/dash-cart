from abc import ABC, abstractmethod
from typing import List, Dict, TypeVar, Generic
from uuid import UUID

TCreate = TypeVar("TCreate")
TUpdate = TypeVar("TUpdate")
TEntity = TypeVar("TEntity")


class MixinBulk(ABC, Generic[TCreate, TUpdate, TEntity]):
    @abstractmethod
    async def bulk_create(self, dto: List[TCreate]) -> List[TEntity]:
        pass

    @abstractmethod
    async def bulk_update(self, updates: Dict[UUID, TUpdate]) -> int:
        pass

    @abstractmethod
    async def bulk_delete(self, ids: List[UUID]) -> int:
        pass
