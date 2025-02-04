from fastapi import Depends, Request, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.service_layer.unit_of_work import AbstractUnitOfWork, get_uow
from src.adapters.orm.models import Session


async def get_current_user(request: Request):
    user = getattr(request.state, "user", None)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    return user
