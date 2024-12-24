from abc import ABC, abstractmethod

from adapters.repository import AbstractRepository, SqlAlchemyRepository
from adapters.orm import db_helper


class AbstractUnitOfWork(ABC):
    repo: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=db_helper.session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.repo = SqlAlchemyRepository(session=self.session)
        return await super().__enter__()

    async def __aexit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
