from fastapi import Depends
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


async def get_user_db(session: AsyncSession = Depends(db_helper.session_getter)):
    yield SQLAlchemyUserDatabase(session, User)
