import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings
from src.adapters.orm.models import Base
from src.adapters.repository import SqlAlchemyRepository


@pytest_asyncio.fixture()
async def engine():
    engine = create_async_engine(url=settings.test_db.url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
    async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            yield session


@pytest_asyncio.fixture
def repository(session):
    repository = SqlAlchemyRepository(session)
    return repository
