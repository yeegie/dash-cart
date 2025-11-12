__all__ = ["SqlalchemySessionCreator"]

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker


class SqlalchemySessionCreator:
    def __init__(self, db_url: str, echo: bool = False) -> None:
        self._db_url = db_url
        self._engine = create_async_engine(self._db_url, echo=echo)
        self._SessionLocal = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    def create_session(self) -> AsyncSession:
        return self._SessionLocal()
    
    @property
    def get_engine(self) -> AsyncEngine:
        return self._engine