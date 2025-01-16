import pytest_asyncio

from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings
from src.adapters.orm.models import Base, FileModel
from src.adapters.repository import SqlAlchemyRepository
from src.service_layer.unit_of_work import SqlAlchemyUnitOfWork


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
    test_file = FileModel(
        id=1,
        filename="test_file.txt",
        filesize=308,
        content_type="application/octet-stream",
        last_modified=datetime.now(),
        etag="etag",
    )
    return test_file
