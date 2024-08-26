# from fastapi import File, UploadFile
# from fastapi.responses import JSONResponse
# from sqlalchemy.ext.asyncio import AsyncSession
# from core.models import FileModel
# import aiofiles

# async def upload_file(session: AsyncSession, file: UploadFile = File(...)):
#     async with aiofiles.open(file.filename, mode="rb") as out_file:
#         content = await file.read()
#         await out_file.write(content)

#     file_model = FileModel(data=content)
#     session.add(file_model)
#     await session.commit()
#     await session.refresh(file_model)

#     return JSONResponse(content={"filename": file.filename, "status": "uploaded"})
