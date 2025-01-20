from abc import ABC, abstractmethod

from minio import Minio, S3Error

from src.config import settings


class AbstractStorageClient(ABC):
    client: Minio

    @abstractmethod
    async def get_file_metadata(self, bucket, filename):
        raise NotImplementedError

    @abstractmethod
    async def upload_file(self, bucket, filename, filepath):
        raise NotImplementedError

    @abstractmethod
    async def download_file(self, bucket, filename):
        raise NotImplementedError

    @abstractmethod
    async def delete_file(self, bucket, filename):
        raise NotImplementedError


class StorageClient(AbstractStorageClient):
    def __init__(self):
        self.client = Minio(
            endpoint=settings.minio.endpoint,
            access_key=settings.minio.access_key,
            secret_key=settings.minio.secret_key,
            secure=settings.minio.secure,
        )

    async def get_file_metadata(self, bucket, filename):
        try:
            return self.client.stat_object(bucket, filename)

        except S3Error as e:
            raise Exception(f"Failed to get metadata of the object: {e}")

    async def upload_file(self, bucket, filename, filepath):
        try:
            self.client.fput_object(bucket, filename, filepath)

        except S3Error as e:
            raise Exception(f"Failed to upload file: {e}")

    async def download_file(self, bucket, filename):
        try:
            return self.client.get_object(bucket, filename)

        except S3Error as e:
            raise Exception(f"Failed to download file: {e}")

    async def delete_file(self, bucket, filename):
        try:
            self.client.remove_object(bucket, filename)

        except S3Error as e:
            raise Exception(f"Failed to delete file: {e}")


async def get_storage_client():
    return StorageClient()
