from pydantic import BaseModel


class AppConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    sql_echo: bool = False
