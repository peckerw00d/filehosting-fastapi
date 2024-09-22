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


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8001
    reload: bool = True


class DatabaseConfig(BaseModel):
    url: str = os.getenv("DB_URL")
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

class TestDatabaseConfig(BaseModel):
    url: str = os.getenv("TEST_DB_URL")


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig()
    test_db: TestDatabaseConfig = TestDatabaseConfig()
    minio: MinIOConfig = MinIOConfig()


settings = Settings()
