from dotenv import load_dotenv
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import BaseModel


load_dotenv()


class MinIOConfig(BaseModel):
    endpoint: str = "localhost:9000"
    access_key: str = os.getenv("MINIO_ACCESS_KEY")
    secret_key: str = os.getenv("MINIO_SECRET_KEY")
    secure: bool = False


class StaticDirConfig(BaseModel):
    media_dir: str = str(Path(__file__).resolve().parents[1] / "media")


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8001
    reload: bool = True


class DatabaseConfig(BaseModel):
    url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig()
    static: StaticDirConfig = StaticDirConfig()
    minio: MinIOConfig = MinIOConfig()


settings = Settings()
