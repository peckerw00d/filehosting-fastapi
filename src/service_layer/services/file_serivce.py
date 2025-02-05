import os
import uuid
from tempfile import NamedTemporaryFile
from typing import Annotated

from minio import Minio, S3Error

from fastapi import HTTPException, UploadFile, status, Depends, Path
from fastapi.responses import FileResponse as FastApiFileResponse

from adapters.orm.models import FileModel
from adapters.storage_client import AbstractStorageClient

from api.schemas import FileResponse, FileCreate
from config import settings, get_minio_settings, Settings
from service_layer.unit_of_work import AbstractUnitOfWork, get_uow


class FileNotFound(Exception):
    pass


class FileUploadError(Exception):
    pass


class FileDeletingError(Exception):
    pass


async def get_files(
    uow: AbstractUnitOfWork, client: AbstractStorageClient, minio_settings: Settings
):
    file_list = []
    async with uow:
        file_urls = await uow.files.list()
        for file in file_urls:
            file_list.append(
                FileResponse.model_validate(
                    await client.get_file_metadata(minio_settings.bucket, file.file_url)
                )
            )
    return file_list


async def get_file(
    file_id: Annotated[int, Path],
    client: AbstractStorageClient,
    uow: AbstractUnitOfWork,
    minio_settings: Settings,
) -> FileResponse:
    async with uow:
        file = await uow.repo.get(entity=FileModel, entity_id=file_id)
        if file is not None:
            file_metadata = await client.get_file_metadata(
                minio_settings.bucket,
                file.file_url,
            )
            return FileResponse.model_validate(file_metadata)

        raise Exception


def save_temp_file(file: UploadFile) -> str:
    with NamedTemporaryFile(delete=False) as temp:
        content = file.file.read()
        temp.write(content)
        return temp.name


async def upload_file(
    uow: AbstractUnitOfWork,
    client: AbstractStorageClient,
    file: UploadFile,
    minio_settings: Settings,
):
    file.filename = file.filename.lower()
    file_path = save_temp_file(file)

    try:
        file_metadata = FileModel(file_url=str(uuid.uuid4()))

        await client.upload_file(
            settings.minio.bucket,
            file_metadata.file_url,
            file_path,
            file.filename,
        )
        stat = await client.get_file_metadata(
            minio_settings.bucket, file_metadata.file_url
        )

        async with uow:
            await uow.repo.add(file_metadata)

        return FileCreate.model_validate(stat)

    except S3Error as err:
        raise FileUploadError(f"Failed to upload file: {err}")

    finally:
        os.unlink(file_path)


async def download_file(
    file_url: str, client: AbstractStorageClient, minio_settings: Settings
):
    s3_object = await client.download_file(settings.minio.bucket, file_url)
    content = s3_object.read()

    with NamedTemporaryFile(delete=False) as temp:
        temp.write(content)
        temp_path = temp.name

    file_metadata = await client.get_file_metadata(minio_settings.bucket, file_url)
    response = FastApiFileResponse(
        path=temp_path,
        filename=file_metadata["filename"],
        media_type="application/octet-stream",
    )
    temp.close()
    return response


async def delete_file(
    file_id: int,
    uow: AbstractUnitOfWork,
    client: AbstractStorageClient,
    minio_settings: Settings,
):
    async with uow:
        file = await uow.repo.get(entity=FileModel, entity_id=file_id)
        if not file:
            raise FileNotFound()
        try:
            await client.delete_file(settings.minio.bucket, file.file_url)
            await uow.repo.delete(file)
            return {"message": f"File {file_id} deleted!"}

        except S3Error as err:
            raise FileDeletingError(err)
