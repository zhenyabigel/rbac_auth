from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Configuration:
    secret_key = ""


class DatabaseConfig(BaseModel):
    dsn: str = "postgresql://postgres:root@localhost:5432/myapi"

class Config(BaseSettings):
    database: DatabaseConfig = DatabaseConfig()
    token_key: str = "!#!my123super123mega123secret123string!#!"
    salt: str = "salt#_#"


config = Config()
