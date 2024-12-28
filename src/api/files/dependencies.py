from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.orm import db_helper
from adapters.orm.models import FileModel
from adapters.repository import SqlAlchemyRepository

from service_layer.unit_of_work import AbstractUnitOfWork, get_uow

from core.schemas import FileResponse


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
