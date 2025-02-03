from abc import ABC, abstractmethod

import uuid

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


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, entity):
        self.session.add(entity)
        return entity

    async def get(self, entity, entity_id):
        return await self.session.get(entity=entity, ident=entity_id)

    async def list(self, entity):
        stmt = select(entity).order_by(entity.id)
        result: Result = await self.session.execute(stmt)
        entities = Result.scalars(result).all()
        return list(entities)

    async def delete(self, entity):
        await self.session.delete(entity)

    async def get_session_by_id(self, entity, session_id):
        stmt = stmt = (
            select(entity)
            .where(entity.session_id == uuid.UUID(session_id))
            .options(selectinload(entity.user))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
