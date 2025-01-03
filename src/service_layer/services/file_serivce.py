from tempfile import NamedTemporaryFile
from typing import Annotated

from minio import Minio

from fastapi import File, HTTPException, UploadFile, status, Depends, Path
from fastapi.responses import FileResponse as FastApiFileResponse

from adapters.orm.models import FileModel
from api.schemas import FileResponse
from config import settings
from service_layer.unit_of_work import AbstractUnitOfWork, get_uow


client = Minio(
    endpoint=settings.minio.endpoint,
    access_key=settings.minio.access_key,
    secret_key=settings.minio.secret_key,
    secure=settings.minio.secure,
)


async def file_by_id(
    file_id: Annotated[int, Path],
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> FileModel:
    async with uow:
        file = await uow.repo.get(entity=FileModel, entity_id=file_id)
        if file is not None:
            return file

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"File {file_id} not found!",
    )


def get_file_path(file: UploadFile) -> str:
    temp = NamedTemporaryFile(delete=False)
    content = file.file.read()

    with temp as f:
        f.write(content)

    return temp.name


async def upload_file(
    uow: AbstractUnitOfWork,
    file: UploadFile = File(...),
):
    file.filename = file.filename.lower()

    file_path = get_file_path(file)

    client.fput_object(
        "main-bucket",
        file.filename,
        file_path,
    )

    stat = client.stat_object("main-bucket", file.filename)

    file_metadata = FileModel(
        filename=stat.object_name,
        filesize=stat.size,
        last_modified=stat.last_modified,
        etag=stat.etag,
        content_type=stat.content_type,
    )

    async with uow:
        await uow.repo.add(file_metadata)

    return FileResponse.model_validate(file_metadata.__dict__)


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


async def delete_file(file_id: int, uow: AbstractUnitOfWork):
    async with uow:
        object = await uow.repo.get(entity=FileModel, entity_id=file_id)
        if not object:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File {file_id} not found!",
            )
        await uow.repo.delete(object)

    client.remove_object("main-bucket", object.filename)
