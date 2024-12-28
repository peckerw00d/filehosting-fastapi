from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result


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
        await self.session.commit()
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
        await self.session.commit()
