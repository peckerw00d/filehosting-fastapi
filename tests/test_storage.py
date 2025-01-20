import pytest

from minio import S3Error


@pytest.mark.asyncio
async def test_upload_file(storage_client, file_path):
    await storage_client.upload_file("test-bucket", "test_file.txt", file_path)
    file_stat = await storage_client.get_file_metadata("test-bucket", "test_file.txt")

    assert file_stat is not None
    assert file_stat.object_name == "test_file.txt"
    assert file_stat.size > 0


@pytest.mark.asyncio
async def test_download_file(storage_client, file_path):
    storage_client.client.fput_object("test-bucket", "test_file.txt", file_path)

    obj = await storage_client.download_file("test-bucket", "test_file.txt")
    file_content = obj.read()

    with open(file_path, "rb") as f:
        expected_content = f.read()
    assert file_content == expected_content


@pytest.mark.asyncio
async def test_delete_file(storage_client, file_path):
    await storage_client.upload_file("test-bucket", "test_file.txt", file_path)
    file_stat = await storage_client.get_file_metadata("test-bucket", "test_file.txt")

    assert file_stat is not None

    await storage_client.delete_file("test-bucket", "test_file.txt")
    with pytest.raises(Exception) as exc_info:
        file_stat = await storage_client.get_file_metadata(
            "test-bucket", "test_file.txt"
        )

    assert "NoSuchKey" in str(exc_info.value)
