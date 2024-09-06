import os
from typing import List
from fastapi import File, UploadFile
from minio import Minio
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import FileModel
from core.config import settings

import aiofiles


client = Minio(
    endpoint=settings.minio.endpoint,
    access_key=settings.minio.access_key,
    secret_key=settings.minio.secret_key,
    secure=settings.minio.secure,
)


async def read_file(file: bytes = File(...)):
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"data": lines}


async def get_files(session: AsyncSession):
    stmt = select(FileModel).order_by(FileModel.id)
    result: Result = await session.execute(stmt)
    files = Result.scalars(result).all()
    return list(files)


async def upload_file(
    session: AsyncSession,
    file: UploadFile = File(...),
):
    file.filename = file.filename.lower()

    if not isinstance(settings.static.media_dir, str):
        raise TypeError("settings.static.media_dir должен быть строкой")

    path = os.path.join(settings.static.media_dir, file.filename)

    async with aiofiles.open(path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    client.fput_object(
        "main-bucket",
        file.filename,
        path,
    )

    file_metadata = FileModel(
        filename=file.filename, path=path, content_type=file.content_type
    )

    session.add(file_metadata)
    await session.commit()
    await session.refresh(file_metadata)
    
    os.remove(path=path)

    return file_metadata


async def upload_multiple_files(
    session: AsyncSession,
    files: List[UploadFile] = File(...),
):
    res = []

    for upload_file in files:
        upload_file.filename = upload_file.filename.lower()

        path = f"{settings.static.media_dir}/{upload_file.filename}"

        file_metadata = FileModel(
            filename=upload_file.filename,
            path=path,
            content_type=upload_file.content_type,
        )

        session.add(file_metadata)
        await session.commit()
        await session.refresh(file_metadata)

        res.append(file_metadata)

    return res
