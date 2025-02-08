import os
import uuid
from tempfile import NamedTemporaryFile
from typing import Annotated

from minio import Minio, S3Error

from fastapi import HTTPException, UploadFile, status, Depends, Path
from fastapi.responses import FileResponse as FastApiFileResponse

from adapters.orm.models import FileModel, User
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


class StorageError(Exception):
    pass


async def get_files(client: AbstractStorageClient, user: User):
    if not user.storage:
        raise StorageError("User has no storage associated")

    storage_files = user.storage.files
    if not storage_files:
        raise FileNotFound("No files found in the user's storage")

    file_list = [
        FileResponse.model_validate(
            await client.get_file_metadata(str(user.id), file.file_url)
        )
        for file in storage_files
    ]

    return file_list


async def get_file_from_storage(file_url: str, storage_files):
    for file in storage_files:
        if file.file_url == file_url:
            return file
    raise FileNotFound(f"File with URL '{file_url}' not found in the user's storage")


async def get_file(
    file_url: Annotated[str, Path],
    client: AbstractStorageClient,
    user: User,
) -> FileResponse:
    if not user.storage:
        raise StorageError("User has no storage associated")

    storage_files = user.storage.files
    if not storage_files:
        raise FileNotFound("No files found in the user's storage")

    file = await get_file_from_storage(file_url, storage_files)
    file_metadata = FileResponse.model_validate(
        await client.get_file_metadata(str(user.id), file.file_url)
    )
    return file_metadata


def save_temp_file(file: UploadFile) -> str:
    with NamedTemporaryFile(delete=False) as temp:
        content = file.file.read()
        temp.write(content)
        return temp.name


async def upload_file(
    uow: AbstractUnitOfWork, client: AbstractStorageClient, file: UploadFile, user: User
):
    file.filename = file.filename.lower()
    file_path = save_temp_file(file)

    try:
        file_metadata = FileModel(
            file_url=str(uuid.uuid4()), storage_id=user.storage.id
        )

        await client.upload_file(
            str(user.id),
            file_metadata.file_url,
            file_path,
            file.filename,
        )
        stat = await client.get_file_metadata(str(user.id), file_metadata.file_url)

        async with uow:
            await uow.files.add(file_metadata)

        return FileCreate.model_validate(stat)

    except S3Error as err:
        raise FileUploadError(f"Failed to upload file: {err}")

    finally:
        os.unlink(file_path)


async def download_file(file_url: str, client: AbstractStorageClient, user: User):
    if not user.storage:
        raise StorageError("User has no storage associated")

    storage_files = user.storage.files
    file = await get_file_from_storage(file_url, storage_files)

    s3_object = await client.download_file(str(user.id), file.file_url)
    content = s3_object.read()

    with NamedTemporaryFile(delete=False) as temp:
        temp.write(content)
        temp_path = temp.name

    file_metadata = await client.get_file_metadata(str(user.id), file.file_url)
    response = FastApiFileResponse(
        path=temp_path,
        filename=file_metadata["filename"],
        media_type="application/octet-stream",
    )
    temp.close()
    return response


async def delete_file(
    file_url: str, uow: AbstractUnitOfWork, client: AbstractStorageClient, user: User
):
    if not user.storage:
        raise StorageError("User has no storage associated")

    storage_files = user.storage.files
    file = await get_file_from_storage(file_url, storage_files)

    async with uow:
        try:
            await client.delete_file(str(user.id), file_url)
            await uow.files.delete(file)
            return {"message": f"File {file_url} deleted!"}

        except S3Error as err:
            raise FileDeletingError(err)
