from typing import List
import aiofiles

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models.db_helper import db_helper
from core.models.files import FileModel
from core.schemas.files import FileResponse


router = APIRouter(tags=["Files"])


@router.post("/read-file")
async def read_file(file: bytes = File(...)):
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"data": lines}


@router.post("/upload-file")
async def upload_file(
    upload_file: UploadFile = File(...), 
    session: AsyncSession = Depends(db_helper.session_getter),
):
    upload_file.filename = upload_file.filename.lower()

    path = f"{settings.static.media_dir}/{upload_file.filename}"

    async with aiofiles.open(path, "wb") as out_file:
        content = await upload_file.read()
        await out_file.write(content)

    file_metadata = FileModel(
        filename=upload_file.filename,
        path=path,
        content_type=upload_file.content_type
    )    

    session.add(file_metadata)
    await session.commit()
    await session.refresh(file_metadata)
    
    return file_metadata


@router.post("/upload-multiple-files")
async def upload_multiple_files(
    uploaded_files: List[UploadFile] = File(...), 
    session: AsyncSession = Depends(db_helper.session_getter),
):
    res = []
    
    for upload_file in uploaded_files:
        upload_file.filename = upload_file.filename.lower()

        path = f"{settings.static.media_dir}/{upload_file.filename}"

        async with aiofiles.open(path, "wb") as out_file:
            content = await upload_file.read()
            await out_file.write(content)

        file_metadata = FileModel(
            filename=upload_file.filename,
            path=path,
            content_type=upload_file.content_type
        )    

        session.add(file_metadata)
        await session.commit()
        await session.refresh(file_metadata)
        

        res.append(file_metadata)

    return res
