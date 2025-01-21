import pytest_asyncio
import pathlib

from datetime import datetime
from httpx import AsyncClient, ASGITransport
from io import BytesIO

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from fastapi import UploadFile

from minio import Minio

from src.config import settings
from src.adapters.orm.models import Base, FileModel
from src.adapters.repository import SqlAlchemyRepository
from src.adapters.storage_client import StorageClient
from src.service_layer.unit_of_work import SqlAlchemyUnitOfWork, get_uow
from src.main import app


@pytest_asyncio.fixture(scope="function")
async def engine():
    engine = create_async_engine(url=settings.test_db.url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session_factory(engine):
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_factory


@pytest_asyncio.fixture(scope="function")
async def session(session_factory):
    async with session_factory() as session:
        async with session.begin():
            yield session


@pytest_asyncio.fixture(scope="function")
async def repository(session):
    repository = SqlAlchemyRepository(session)
    return repository


@pytest_asyncio.fixture(scope="function")
async def unit_of_work(session_factory):
    uow = SqlAlchemyUnitOfWork(session_factory)
    return uow


@pytest_asyncio.fixture(scope="function")
async def test_file():
    test_file = FileModel(id=1)
    return test_file


@pytest_asyncio.fixture(scope="function")
async def test_files_list():
    test_files = [
        FileModel(id=1),
        FileModel(id=2),
        FileModel(id=3),
    ]
    return test_files


@pytest_asyncio.fixture(scope="function")
async def client(unit_of_work):
    app.dependency_overrides[get_uow] = unit_of_work
    client = AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000/files"
    )
    yield client
    await client.aclose()
    app.dependency_overrides = {}


@pytest_asyncio.fixture(scope="function")
async def file_path():
    current_path = pathlib.Path(__file__).parent.absolute()
    file_path = current_path / "test_file.txt"
    return file_path


@pytest_asyncio.fixture(scope="function")
async def upload_file(file_path):
    file = open(file_path, "rb")
    file_name = file_path.name

    upload_file = UploadFile(filename=file_name, file=file)

    files = {"file": (file_name, upload_file.file, "text/plain")}

    yield files

    file.close()
    upload_file.file.close()


@pytest_asyncio.fixture(scope="function")
async def storage_client():
    storage_client = StorageClient()
    yield storage_client
    obj_list = storage_client.client.list_objects("test-bucket")
    storage_client.client.remove_objects("test-bucket", obj_list)
