from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import FileModel, db_helper
from core.schemas import FileResponse
from . import services


router = APIRouter(tags=["Files"])


@router.post("/read-file")
async def read_file(file: bytes = File(...)):
    return await services.read_file(file=file)


@router.get("/", response_model=List[FileResponse])
async def get_files(session: AsyncSession = Depends(db_helper.session_getter)):
    return await services.get_files(session=session)


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: int, session: AsyncSession = Depends(db_helper.session_getter)
):
    return await services.get_file(file_id=file_id, session=session)


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
