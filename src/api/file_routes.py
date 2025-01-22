from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status

from minio import S3Error

from adapters.orm.models import FileModel
from adapters.storage_client import (
    get_storage_client,
    StorageClient,
    AbstractStorageClient,
)
from api.schemas import FileResponse, FileCreate
from service_layer.services import file_serivce
from service_layer.unit_of_work import AbstractUnitOfWork, get_uow


router = APIRouter(tags=["Files"])


@router.get("/", response_model=List[FileResponse])
async def get_files(
    uow: AbstractUnitOfWork = Depends(get_uow),
    client: AbstractStorageClient = Depends(get_storage_client),
):
    return await file_serivce.get_files(uow=uow, client=client)


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: int,
    uow: AbstractUnitOfWork = Depends(get_uow),
    client: AbstractStorageClient = Depends(get_storage_client),
):
    try:
        return await file_serivce.get_file(file_id=file_id, client=client, uow=uow)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File {file_id} not found!",
        )


@router.get("/download/{file_id}")
async def download_file(
    file_url: str,
    client: AbstractStorageClient = Depends(get_storage_client),
):
    try:
        return await file_serivce.download_file(file_url=file_url, client=client)

    except S3Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download file: {err}",
        )


@router.post("/upload-file", response_model=FileCreate)
async def upload_file(
    file: UploadFile = File(...),
    uow: AbstractUnitOfWork = Depends(get_uow),
    client: AbstractStorageClient = Depends(get_storage_client),
):
    try:
        return await file_serivce.upload_file(
            file=file,
            uow=uow,
            client=client,
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
    file_id: int,
    uow: AbstractUnitOfWork = Depends(get_uow),
    client: StorageClient = Depends(get_storage_client),
):
    try:
        return await file_serivce.delete_file(
            file_id=file_id,
            uow=uow,
            client=client,
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
