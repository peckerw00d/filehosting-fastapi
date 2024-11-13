from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.users import services
from core.models import db_helper
from core.schemas.users import UserCreate

router = APIRouter(tags=["Users"])


@router.post("/sign-up")
async def create_user(
    user_data: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)
):

    return await services.create_user(user_data=user_data, session=session)
