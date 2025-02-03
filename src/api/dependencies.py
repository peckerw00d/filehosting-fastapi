from fastapi import Depends, Request, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.service_layer.unit_of_work import AbstractUnitOfWork, get_uow
from src.adapters.orm.models import Session


async def get_current_user(
    request: Request, uow: AbstractUnitOfWork = Depends(get_uow)
):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Session not found"
        )

    async with uow:
        session = await uow.repo.get_session_by_id(Session, session_id)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session"
            )

        # Возвращаем пользователя внутри контекста
        return session.user
