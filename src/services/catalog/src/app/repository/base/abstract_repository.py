from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Dict, TypeVar, Generic
from uuid import UUID


TCreate = TypeVar("TCreate")
TUpdate = TypeVar("TUpdate")
TEntity = TypeVar("TEntity")


class AbstractRepository(ABC, Generic[TCreate, TUpdate, TEntity]):
    # Base CRUD
    @abstractmethod
    async def create(self, dto: TCreate) -> TEntity:
        pass

    @abstractmethod
    async def get(self, id: UUID) -> Optional[TEntity]:
        pass

    @abstractmethod
    async def update(self, id: UUID, dto: TUpdate) -> Optional[TEntity]:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        pass

    # Useful operation
    @abstractmethod
    async def list(
        self,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[TEntity], int]:
        """List of objects with pagination"""
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """Check existence without loading the object"""
        pass

    @abstractmethod
    async def get_many(self, ids: List[UUID]) -> List[TEntity]:
        pass

    @abstractmethod
    async def partial_update(self, id: UUID, **fields) -> Optional[TEntity]:
        pass
