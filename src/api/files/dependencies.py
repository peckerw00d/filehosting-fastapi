from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.files import services
from adapters.orm import db_helper
from adapters.orm.models import FileModel
from adapters.repository import SqlAlchemyRepository


async def file_by_id(
    file_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> FileModel:
    repo = SqlAlchemyRepository(session=session)
    file = await repo.get(entity=FileModel, entity_id=file_id)
    if file is not None:
        return file

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"File {file_id} not found!",
    )
