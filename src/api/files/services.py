from tempfile import NamedTemporaryFile
from typing import List

from minio import Minio

from fastapi import File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse as FastApiFileResponse

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import FileModel
from core.schemas import FileCreate, FileResponse
from core.config import settings


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


async def get_file(file_id: int, session: AsyncSession):
    return await session.get(FileModel, file_id)


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

    temp = NamedTemporaryFile(delete=False)
    content = file.file.read()

    with temp as f:
        f.write(content)

    result = client.fput_object(
        "main-bucket",
        file.filename,
        temp.name,
    )

    stat = client.stat_object("main-bucket", file.filename)

    file_metadata = FileModel(
        filename=stat.object_name,
        filesize=stat.size,
        last_modified=stat.last_modified,
        etag=stat.etag,
        content_type=stat.content_type,
    )

    file_create_data = FileCreate(
        filename=stat.object_name,
        filesize=stat.size,
        last_modified=stat.last_modified,
        etag=stat.etag,
        content_type=stat.content_type,
    )

    session.add(file_metadata)
    await session.commit()
    await session.refresh(file_metadata)

    return FileResponse.model_validate(file_metadata.__dict__)


async def upload_multiple_files(
    session: AsyncSession,
    files: List[UploadFile] = File(...),
):
    res = []

    for upload_file in files:

        upload_file.filename = upload_file.filename.lower()

        temp = NamedTemporaryFile(delete=False)
        content = upload_file.file.read()

        with temp as f:
            f.write(content)

        client.fput_object(
            "main-bucket",
            upload_file.filename,
            temp.name,
        )

        stat = client.stat_object("main-bucket", upload_file.filename)

        file_metadata = FileModel(
            filename=stat.object_name,
            filesize=stat.size,
            last_modified=stat.last_modified,
            etag=stat.etag,
            content_type=stat.content_type,
        )

        file_create_data = FileCreate(
            filename=stat.object_name,
            filesize=stat.size,
            last_modified=stat.last_modified,
            etag=stat.etag,
            content_type=stat.content_type,
        )

        session.add(file_metadata)
        await session.commit()
        await session.refresh(file_metadata)

        res.append(FileResponse.model_validate(file_metadata.__dict__))

    return res


async def download_file(file: FileResponse):
    object_name = file.filename

    s3_object = client.get_object("main-bucket", object_name)
    content = s3_object.read()

    temp = NamedTemporaryFile(delete=False)
    with temp as f:
        f.write(content)

    response = FastApiFileResponse(
        path=temp.name, filename=object_name, media_type="application/octet-stream"
    )
    temp.close()

    return response


async def delete_file(file_id: int, session: AsyncSession):
    object = await session.get(FileModel, file_id)
    if not object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File {file_id} not found!",
        )

    client.remove_object("main-bucket", object.filename)

    await session.delete(object)
    await session.commit()
