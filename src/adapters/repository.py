from abc import ABC, abstractmethod

import uuid

from src.adapters.orm.models import FileModel, User, Session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.orm import selectinload


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, entity):
        raise NotImplementedError

    @abstractmethod
    def get(self, entity, entity_id):
        raise NotImplementedError


class FileRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, file: FileModel):
        self.session.add(file)
        return file

    async def get(self, file: FileModel, file_id: int):
        return await self.session.get(entity=file, ident=file_id)

    async def get_by_url(self, file_url: str):
        stmt = select(FileModel).where(FileModel.file_url == file_url)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list(self):
        stmt = select(FileModel).order_by(FileModel.id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete(self, file: FileModel):
        await self.session.delete(file)


class UserRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User):
        self.session.add(user)
        return user

    async def get(self, user: User, user_id: uuid.UUID):
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list(self):
        stmt = select(User).order_by(User.id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete(self, user: User):
        await self.session.delete(user)


class SessionRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, session: Session):
        self.session.add(session)
        return session

    async def get(self, session: Session, session_id: uuid.UUID):
        stmt = select(Session).where(Session.session_id == session_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list(self):
        stmt = select(Session).order_by(Session.session_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
