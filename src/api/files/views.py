from pathlib import Path

import aiofiles
from fastapi import APIRouter, File, UploadFile
from core.config import settings


router = APIRouter(tags=["Files"])


@router.post("/get_file")
async def get_file(file: bytes = File(...)):
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"data": lines}


@router.post("/upload_file")
async def upload_file(upload_file: UploadFile = File(...)):
    upload_file.filename = upload_file.filename.lower()

    path = f"{settings.static.media_dir}/{upload_file.filename}"

    async with aiofiles.open(path, "wb") as out_file:
        content = await upload_file.read()  # async read
        await out_file.write(content)  # async write
    
    return {
        "file": upload_file.filename,
        "filename": upload_file.filename,
        "path": path,
        "type": upload_file.content_type
    }