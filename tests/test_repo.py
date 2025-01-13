import pytest
import asyncio
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.orm.models import FileModel
from src.adapters.repository import SqlAlchemyRepository


@pytest.mark.asyncio
async def test_repo_add(session, repository):
    file = FileModel(
        filename="test_file.txt",
        filesize=308,
        content_type="application/octet-stream",
        last_modified=datetime.now(),
        etag="etag",
    )

    added_file = await repository.add(file)
    await session.flush()

    assert added_file.id is not None
    assert added_file.filename == "test_file.txt"


@pytest.mark.asyncio
async def test_repo_get_exist_entity(session, repository):
    file = FileModel(
        filename="test_file.txt",
        filesize=308,
        content_type="application/octet-stream",
        last_modified=datetime.now(),
        etag="etag",
    )

    added_file = await repository.add(file)
    await session.flush()

    retrieved_file = await repository.get(FileModel, added_file.id)

    assert retrieved_file.id is not None
    assert retrieved_file.id == added_file.id
    assert retrieved_file.filename == "test_file.txt"


@pytest.mark.asyncio
async def test_repo_list(session, repository):
    file_1 = FileModel(
        filename="first_file.txt",
        filesize=308,
        content_type="application/octet-stream",
        etag="etag",
        last_modified=datetime.now(),
    )
    file_2 = FileModel(
        filename="second_file.txt",
        filesize=308,
        content_type="application/octet-stream",
        etag="etag",
        last_modified=datetime.now(),
    )
    file_3 = FileModel(
        filename="third_file.txt",
        filesize=308,
        content_type="application/octet-stream",
        etag="etag",
        last_modified=datetime.now(),
    )

    await repository.add(file_1)
    await repository.add(file_2)
    await repository.add(file_3)
    session.flush()

    entities = await repository.list(FileModel)

    assert len(entities) == 3
    assert entities[0].id == file_1.id
    assert entities[1].id == file_2.id
    assert entities[2].id == file_3.id
    assert entities[0].filename == "first_file.txt"
    assert entities[1].filename == "second_file.txt"
    assert entities[2].filename == "third_file.txt"


@pytest.mark.asyncio
async def test_repo_delete(session, repository):
    file = FileModel(
        filename="test_file.txt",
        filesize=308,
        content_type="application/octet-stream",
        last_modified=datetime.now(),
        etag="etag",
    )

    added_file = await repository.add(file)
    await session.flush()

    retrieved_file = await repository.get(FileModel, added_file.id)

    await repository.delete(retrieved_file)
    await session.flush()

    deleted_file = await repository.get(FileModel, added_file.id)

    assert deleted_file is None
