from src.adapters.orm.models import FileModel

import pytest


async def test_uow_context_manager(unit_of_work):
    async with unit_of_work as uow:
        assert uow.session is not None
        assert uow.repo is not None


async def test_uow_commit(unit_of_work, test_file):
    async with unit_of_work as uow:
        await uow.repo.add(test_file)
        await uow.commit()

    async with unit_of_work as uow:
        retrieved_file = await uow.repo.get(FileModel, test_file.id)
        assert retrieved_file is not None
        assert retrieved_file.filename == test_file.filename


async def test_uow_rollback(unit_of_work, test_file):
    async with unit_of_work as uow:
        await uow.repo.add(test_file)
        await uow.rollback()

    async with unit_of_work as uow:
        retrieved_file = await uow.repo.get(FileModel, test_file.id)
        assert retrieved_file is None


async def test_uow_exception_handling(unit_of_work, test_file):
    with pytest.raises(Exception):
        async with unit_of_work as uow:
            await uow.repo.add(test_file)
            raise Exception("Test exception")

        async with unit_of_work as uow:
            retrieved_file = await uow.repo.get(FileModel, test_file.id)
            assert retrieved_file is None


async def test_uow_repository_operation(unit_of_work, test_file):
    async with unit_of_work as uow:
        await uow.repo.add(test_file)
        await uow.commit()

    async with unit_of_work as uow:
        retrieved_file = await uow.repo.get(FileModel, test_file.id)
        assert retrieved_file is not None
        assert retrieved_file.filename == test_file.filename

    async with unit_of_work as uow:
        await uow.repo.delete(test_file)
        await uow.commit()

    async with unit_of_work as uow:
        deleted_file = await uow.repo.get(FileModel, test_file.id)
        assert deleted_file is None
