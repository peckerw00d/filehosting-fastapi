from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.files import services
from core.models import db_helper, FileModel


async def file_by_id(
        file_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_getter)
) -> FileModel:
    file = await services.get_file(session=session, file_id=file_id)
    if file is not None:
        return file
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"File {file_id} not found!",
    )
