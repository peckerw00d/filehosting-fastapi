from abc import ABC, abstractmethod

from minio import Minio, S3Error

from src.config import settings


class AbstractStorageClient(ABC):
    client: Minio

    @abstractmethod
    async def get_file_metadata(self, bucket, file_url):
        raise NotImplementedError

    @abstractmethod
    async def upload_file(self, bucket, file_url, file_path, filename):
        raise NotImplementedError

    @abstractmethod
    async def download_file(self, bucket, file_url):
        raise NotImplementedError

    @abstractmethod
    async def delete_file(self, bucket, file_url):
        raise NotImplementedError


class StorageClient(AbstractStorageClient):
    def __init__(self):
        self.client = Minio(
            endpoint=settings.minio.endpoint,
            access_key=settings.minio.access_key,
            secret_key=settings.minio.secret_key,
            secure=settings.minio.secure,
        )

    async def get_file_metadata(self, bucket, file_url):
        try:
            obj_stat = self.client.stat_object(bucket, file_url)
            return {
                "filename": obj_stat.metadata.get("x-amz-meta-filename"),
                "file_url": file_url,
                "file_size": obj_stat.size,
                "file_type": obj_stat.content_type,
                "last_modified": obj_stat.last_modified,
            }

        except S3Error as e:
            raise Exception(f"Failed to get metadata of the object: {e}")

    async def upload_file(self, bucket, file_url, file_path, filename):
        try:
            self.client.fput_object(
                bucket, file_url, file_path, metadata={"filename": filename}
            )

        except S3Error as e:
            raise Exception(f"Failed to upload file: {e}")

    async def download_file(self, bucket, file_url):
        try:
            return self.client.get_object(bucket, file_url)

        except S3Error as e:
            raise Exception(f"Failed to download file: {e}")

    async def delete_file(self, bucket, file_url):
        try:
            self.client.remove_object(bucket, file_url)

        except S3Error as e:
            raise Exception(f"Failed to delete file: {e}")


async def get_storage_client():
    return StorageClient()
