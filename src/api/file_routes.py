from typing import List

from fastapi import APIRouter, Depends, File, UploadFile

from adapters.orm.models import FileModel
from api.schemas import FileResponse
from service_layer.services import file_serivce
from service_layer.unit_of_work import AbstractUnitOfWork, get_uow


router = APIRouter(tags=["Files"])


@router.get("/", response_model=List[FileResponse])
async def get_files(uow: AbstractUnitOfWork = Depends(get_uow)):
    async with uow:
        return await uow.repo.list(FileModel)


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(file: FileResponse = Depends(file_serivce.file_by_id)):
    return file


@router.get("/download/{file_id}")
async def download_file(file: FileResponse = Depends(file_serivce.file_by_id)):
    return await file_serivce.download_file(file=file)


@router.post("/upload-file", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    return await file_serivce.upload_file(
        file=file,
        uow=uow,
    )


@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    return await file_serivce.delete_file(
        file_id=file_id,
        uow=uow,
    )
