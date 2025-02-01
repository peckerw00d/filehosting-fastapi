from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse

from minio import S3Error

from src.service_layer.services import user_service
from src.service_layer.unit_of_work import AbstractUnitOfWork, get_uow

from src.adapters.storage_client import AbstractStorageClient, get_storage_client

from api.schemas import UserCreate, UserLogin


router = APIRouter(tags=["Users"])


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
        return RedirectResponse("/files/", status_code=302)

    except S3Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {err}",
        )


@router.post("/login")
async def login(user_data: UserLogin, uow: AbstractUnitOfWork = Depends(get_uow)):
    try:
        user = await user_service.check_user_credentials(uow=uow, user_data=user_data)

    except user_service.LoginError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    session = await user_service.create_session(uow=uow, user_id=user.id)

    response = RedirectResponse("/files/", status_code=302)
    response.set_cookie(
        key="Authorization", value=str(session.session_id), httponly=True
    )

    return response
