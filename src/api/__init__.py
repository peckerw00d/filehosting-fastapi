from fastapi import APIRouter
from api.file_routes import router as files_router

router = APIRouter()
router.include_router(files_router, prefix="/files")
