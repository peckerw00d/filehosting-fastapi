import os
from pathlib import Path
from pyclbr import Class
from typing import ClassVar
from pydantic_settings import BaseSettings
from pydantic import BaseModel

class StaticDirConfig(BaseModel):
    media_dir: str = Path(__file__).resolve().parents[1] / "media"


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     case_sensitive=False,
    #     env_nested_delimiter="__",
    #     env_prefix="APP_CONFIG__",
    # )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig = DatabaseConfig()
    static: StaticDirConfig = StaticDirConfig()
    

settings = Settings()
