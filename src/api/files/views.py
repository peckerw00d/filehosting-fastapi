from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from .services import (
    read_file_service, 
    upload_file_service, 
    upload_multiple_files_service,
)

router = APIRouter(tags=["Files"])


@router.post("/read-file")
async def read_file(file: bytes = File(...)):
    return await read_file_service(file=file)


@router.post("/upload-file")
async def upload_file(
    file: UploadFile = File(...), 
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await upload_file_service(
        file=file,
        session=session,
)


@router.post("/upload-multiple-files")
async def upload_multiple_files(
    files: List[UploadFile] = File(...), 
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await upload_multiple_files_service(
        files=files,
        session=session,
    )
