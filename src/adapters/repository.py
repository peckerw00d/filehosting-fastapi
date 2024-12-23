from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, entity):
        raise NotImplementedError

    @abstractmethod
    def get(self, entity_id):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    async def add(self, entity):
        self.session.add(entity)
        await self.session.commit()
        return entity

    async def get(self, entity_id):
        entity = await self.session.get(entity_id)
        return entity
