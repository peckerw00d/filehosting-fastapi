import pytest
import asyncio
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.orm.models import FileModel
from src.adapters.repository import SqlAlchemyRepository


@pytest.mark.asyncio
async def test_repo_add(session, repository, test_file):
    added_file = await repository.add(test_file)
    await session.flush()

    assert added_file.id is not None
    assert added_file.filename == test_file.filename


@pytest.mark.asyncio
async def test_repo_get_exist_entity(session, repository, test_file):
    added_file = await repository.add(test_file)
    await session.flush()

    retrieved_file = await repository.get(FileModel, added_file.id)

    assert retrieved_file.id is not None
    assert retrieved_file.id == added_file.id
    assert retrieved_file.filename == "test_file.txt"


@pytest.mark.asyncio
async def test_repo_list(session, repository, test_files_list):
    await repository.add(test_files_list[0])
    await repository.add(test_files_list[1])
    await repository.add(test_files_list[2])
    session.flush()

    entities = await repository.list(FileModel)

    assert len(entities) == 3
    assert entities[0].id == test_files_list[0].id
    assert entities[1].id == test_files_list[1].id
    assert entities[2].id == test_files_list[2].id
    assert entities[0].filename == test_files_list[0].filename
    assert entities[1].filename == test_files_list[1].filename
    assert entities[2].filename == test_files_list[2].filename


@pytest.mark.asyncio
async def test_repo_delete(session, repository, test_file):
    added_file = await repository.add(test_file)
    await session.flush()

    retrieved_file = await repository.get(FileModel, added_file.id)

    await repository.delete(retrieved_file)
    await session.flush()

    deleted_file = await repository.get(FileModel, added_file.id)

    assert deleted_file is None
