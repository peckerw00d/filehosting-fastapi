from fastapi import Request, Depends, HTTPException, status

from src.service_layer.unit_of_work import (
    AbstractUnitOfWork,
    get_uow,
    SqlAlchemyUnitOfWork,
)
from src.adapters.orm.models import Session


async def get_user_from_session(session_id: str, uow: AbstractUnitOfWork):
    async with uow:
        session = await uow.repo.get_session_by_id(Session, session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session"
            )
        return session.user


async def session_middleware(request: Request, call_next):
    if request.url.path in ["/register", "/login"]:
        return await call_next(request)

    session_id = request.cookies.get("session_id")

    if session_id:
        uow = SqlAlchemyUnitOfWork()
        try:
            user = await get_user_from_session(session_id, uow)
            request.state.user = user
        except HTTPException as e:
            raise e

    response = await call_next(request)
    return response
