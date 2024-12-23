from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.orm import db_helper
from adapters.repository import SqlAlchemyRepository
from adapters.orm.models import FileModel
from core.schemas import FileResponse
from . import services, dependencies


router = APIRouter(tags=["Files"])


@router.get("/", response_model=List[FileResponse])
async def get_files(session: AsyncSession = Depends(db_helper.session_getter)):
    repo = SqlAlchemyRepository(session=session)
    return await repo.list(FileModel)


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(file: FileResponse = Depends(dependencies.file_by_id)):
    return file


@router.get("/download/{file_id}")
async def download_file(file: FileResponse = Depends(dependencies.file_by_id)):
    return await services.download_file(file=file)


@router.post("/upload-file", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await services.upload_file(
        file=file,
        session=session,
    )


@router.post("/upload-multiple-files", response_model=List[FileResponse])
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await services.upload_multiple_files(
        files=files,
        session=session,
    )


@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await services.delete_file(
        file_id=file_id,
        session=session,
    )
