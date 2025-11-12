from abc import abstractmethod
from typing import List, Tuple, TypeVar, Generic

from .abstract_repository import AbstractRepository
from .mixins.bulk import MixinBulk


TCreate = TypeVar("TCreate")
TUpdate = TypeVar("TUpdate")
TEntity = TypeVar("TEntity")


class AbstractProductRepository(
    AbstractRepository,
    MixinBulk,
    Generic[TCreate, TUpdate, TEntity],
):
    @abstractmethod
    async def get_by_item_number(self, item_number: str) -> TEntity:
        pass

    @abstractmethod
    async def search_with_total(
        self,
        limit: int = 20,
        offset: int = 0,
        **filters
    ) -> Tuple[List[TEntity], int]:
        pass
