from abc import ABC, abstractmethod
from typing import Any, Optional, List


class IService(ABC):
    @abstractmethod
    async def create(self) -> Any:
        pass

    @abstractmethod
    async def get_by_id(self, id) -> Optional[Any]:
        pass

    @abstractmethod
    async def get_or_create(self, id) -> Any:
        pass

    @abstractmethod
    async def update(self, id, dto) -> bool:
        pass

    @abstractmethod
    async def delete(self, id) -> bool:
        pass

    @abstractmethod
    async def list(self) -> List[Any]:
        pass
