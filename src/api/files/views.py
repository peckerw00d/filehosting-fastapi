from distutils.command import upload
import shutil
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import services  


router = APIRouter(tags=["Files"])


@router.post("/get_file")
async def get_file(file: bytes = File(...)):
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"data": lines}


@router.post("/upload_file")
async def upload_file(upload_file: UploadFile = File(...)):
    upload_file.filename = upload_file.filename.lower()
    
    path = f"media/{upload_file.filename}"

    with open(path, "wb+") as buffer:
        shutil.copyfileobj(upload_file, buffer)
    
    return {
        "file": upload_file,
        "file": upload_file.filename,
        "path": path,
        "type": upload_file.content_type
    }