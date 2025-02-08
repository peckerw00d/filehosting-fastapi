from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status

from minio import S3Error

from adapters.orm.models import FileModel, User
from adapters.storage_client import (
    get_storage_client,
    StorageClient,
    AbstractStorageClient,
)

from api.schemas import FileResponse, FileCreate
from api.dependencies import get_current_user

from service_layer.services import file_serivce
from service_layer.unit_of_work import AbstractUnitOfWork, get_uow

from config import get_minio_settings, Settings

router = APIRouter(tags=["Files"])


@router.get("/", response_model=List[FileResponse])
async def get_files(
    client: AbstractStorageClient = Depends(get_storage_client),
    current_user: User = Depends(get_current_user),
):
    try:
        return await file_serivce.get_files(client=client, user=current_user)

    except file_serivce.StorageError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

    except file_serivce.FileNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {err}",
        )


@router.get("/{file_url}", response_model=FileResponse)
async def get_file(
    file_url: str,
    client: AbstractStorageClient = Depends(get_storage_client),
    current_user: User = Depends(get_current_user),
):
    try:
        return await file_serivce.get_file(
            file_url=file_url, client=client, user=current_user
        )

    except file_serivce.StorageError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

    except file_serivce.FileNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File {file_url} not found!",
        )

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {err}",
        )


@router.get("/download/{file_url}")
async def download_file(
    file_url: str,
    client: AbstractStorageClient = Depends(get_storage_client),
    current_user: User = Depends(get_current_user),
):
    try:
        return await file_serivce.download_file(
            file_url=file_url, client=client, user=current_user
        )

    except S3Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download file: {err}",
        )

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {err}",
        )


@router.post("/upload-file", response_model=FileCreate)
async def upload_file(
    file: UploadFile = File(...),
    uow: AbstractUnitOfWork = Depends(get_uow),
    client: AbstractStorageClient = Depends(get_storage_client),
    current_user: User = Depends(get_current_user),
):
    try:
        return await file_serivce.upload_file(
            file=file, uow=uow, client=client, user=current_user
        )
    except file_serivce.FileUploadError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {err}",
        )


@router.delete("/{file_id}")
async def delete_file(
    file_url: str,
    uow: AbstractUnitOfWork = Depends(get_uow),
    client: StorageClient = Depends(get_storage_client),
    current_user: User = Depends(get_current_user),
):
    try:
        return await file_serivce.delete_file(
            file_url=file_url, uow=uow, client=client, user=current_user
        )
    except file_serivce.FileDeletingError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file: {err}",
        )

    except file_serivce.FileNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File {file_id} not found!",
        )
