from abc import ABC, abstractmethod
from uuid import UUID


class MixinSoftDeletable(ABC):
    """
    Note:
    The entity **must have** a "deleted_at" field.
    """
    @abstractmethod
    async def soft_delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    async def restore(self, id: UUID) -> bool:
        pass
