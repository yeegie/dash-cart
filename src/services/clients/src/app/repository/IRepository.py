from abc import ABC, abstractmethod
from typing import Optional, Any, List
from .scheams.client import ClientSchema, GetClientSchema, GetClientsSchema


class IRepository(ABC):
    @abstractmethod
    async def create(self, dto) -> Any:
        pass

    @abstractmethod
    async def get(self, id: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def update(self, id: str, dto) -> bool:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    async def list(self) -> List[Any]:
        pass
