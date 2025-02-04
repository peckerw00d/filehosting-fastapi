from abc import ABC, abstractmethod

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from adapters.repository import (
    AbstractRepository,
    FileRepository,
    UserRepository,
    SessionRepository,
)
from config import settings


class AbstractUnitOfWork(ABC):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


DEFAULT_ASYNC_ENGINE = create_async_engine(
    url=settings.db.url,
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)

DEFAULT_ASYNC_SESSION_MAKER = async_sessionmaker(
    bind=DEFAULT_ASYNC_ENGINE, autoflush=False, autocommit=False, expire_on_commit=False
)


class UnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] = DEFAULT_ASYNC_SESSION_MAKER,
    ):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.files = FileRepository(self.session)
        self.sessions = SessionRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


async def get_uow() -> AbstractUnitOfWork:
    return UnitOfWork()
