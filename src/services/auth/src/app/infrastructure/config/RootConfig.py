from pydantic import BaseModel

from .AppConfig import AppConfig
from .DatabaseConfig import DatabaseConfig


class RootConfig(BaseModel):
    app: AppConfig
    database: DatabaseConfig
