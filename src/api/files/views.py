from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from api.files import dependencies
from core.models.db_helper import db_helper
from core.models.files import FileModel
from . import services

router = APIRouter(tags=["Files"])


@router.post("/read-file")
async def read_file(file: bytes = File(...)):
    return await services.read_file(file=file)


@router.get("/get-file")
async def get_file(
    file: FileModel = Depends(dependencies.file_by_id)
):
    return await file


@router.post("/upload-file")
async def upload_file(
    file: UploadFile = File(...), 
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await services.upload_file(
        file=file,
        session=session,
)


@router.post("/upload-multiple-files")
async def upload_multiple_files(
    files: List[UploadFile] = File(...), 
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await services.upload_multiple_files(
        files=files,
        session=session,
    )
