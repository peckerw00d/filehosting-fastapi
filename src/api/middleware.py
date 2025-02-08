import uuid

from fastapi import Request, Depends, HTTPException, status

import uuid

from src.service_layer.unit_of_work import (
    AbstractUnitOfWork,
    get_uow,
    UnitOfWork,
)
from src.adapters.orm.models import Session


async def get_user_from_session(session_id: str, uow: AbstractUnitOfWork):
    async with uow:
        user = await uow.users.get_user_by_session_id(session_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session"
            )
        return user


async def session_middleware(request: Request, call_next):
    if request.url.path in [
        "/users/register",
        "/users/login",
        "/docs",
        "/openapi.json",
    ]:
        return await call_next(request)

    session_id = request.cookies.get("session_id")

    if session_id:
        uow = UnitOfWork()
        try:
            user = await get_user_from_session(session_id, uow)
            request.state.user = user
        except HTTPException as err:
            raise err

    response = await call_next(request)
    return response
