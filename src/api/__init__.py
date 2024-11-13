from fastapi import APIRouter
from .files.views import router as files_router
from .users.views import router as user_router

router = APIRouter()
router.include_router(files_router, prefix="/files")
router.include_router(user_router, prefix="/users")
