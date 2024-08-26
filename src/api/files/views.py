from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import services  


router = APIRouter(tags=["Files"])


@router.post("/")
async def get_file(
    file: bytes = File(...),
):
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"data": lines}
