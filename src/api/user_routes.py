from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse, Response
from fastapi.security import HTTPBasic

from sqlalchemy import select

from typing import Annotated
from minio import S3Error

from src.service_layer.services import user_service
from src.service_layer.unit_of_work import AbstractUnitOfWork, get_uow

from src.adapters.orm.models import User, Session
from src.adapters.storage_client import AbstractStorageClient, get_storage_client

from api.schemas import UserCreate, UserLogin
from api.dependencies import get_current_user


router = APIRouter(tags=["Users"])

security = HTTPBasic()


@router.post("/register")
async def register(
    user_data: UserCreate,
    uow: AbstractUnitOfWork = Depends(get_uow),
    storage_client: AbstractStorageClient = Depends(get_storage_client),
):
    try:
        await user_service.create_user(
            uow=uow, user_data=user_data, storage_client=storage_client
        )
        return {"message": "User registered successfully"}
    except S3Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user storage: {err}",
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )


@router.post("/login")
async def login(
    user_credentials: Annotated[UserLogin, Depends(security)],
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    try:
        user = await user_service.check_user_credentials(
            uow=uow, user_credentials=user_credentials
        )
        session = await user_service.create_session(uow=uow, user_id=user.id)
        response = Response(content="Logged in successfully", media_type="text/plain")
        response.set_cookie(
            key="session_id", value=str(session.session_id), httponly=True
        )
        return response

    except user_service.LoginError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err))


@router.post("/logout")
async def logout(
    response: Response,
    uow: AbstractUnitOfWork = Depends(get_uow),
    current_user: User = Depends(get_current_user),
):
    async with uow:
        session = await uow.sessions.get_by_user_fk(current_user.id)

        if session:
            await uow.sessions.delete(session)

    response.delete_cookie(key="session_id")
    return {"message": "Logged out successfully"}
