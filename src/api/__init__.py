from fastapi import APIRouter
from .files.views import router as files_router

router = APIRouter()
router.include_router(files_router, prefix="/files")
