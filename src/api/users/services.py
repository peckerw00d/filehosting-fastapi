from sqlalchemy import Result, Select
from sqlalchemy.ext.asyncio import AsyncSession


from core.models.users import User
from core.schemas.users import UserCreate, UserRead
from utils.password_hashing import get_hashed_password


async def create_user(session: AsyncSession, user_data: UserCreate):
    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        user_name=user_data.user_name,
        email_address=user_data.email_address,
        password=get_hashed_password(user_data.password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return UserRead.model_validate(user.__dict__)


async def get_users(session: AsyncSession):
    stmt = Select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = Result.scalars(result).all()
    return list(users)


async def get_user(session: AsyncSession, user_id: int):
    return await session.get(User, user_id)
