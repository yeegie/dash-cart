from pydantic import BaseModel, SecretStr

from typing import Optional


class DatabaseConfig(BaseModel):
    driver: str = "postgresql+asyncpg"
    user: str
    password: SecretStr
    host: str = "0.0.0.0"
    port: int = 5432
    container_name: Optional[str] = None
    database: str = "dashcart"

    def __url(self) -> str:
        if self.container_name:
            return self.container_name
        
        return f"{self.host}:{self.port}"

    @property
    def connection_string(self) -> str:
        return f"{self.driver}://{self.user}:{self.password.get_secret_value()}@{self.__url()}/{self.database}"
