from fastapi import APIRouter
from api.file_routes import router as files_router
from api.user_routes import router as users_router

router = APIRouter()
router.include_router(files_router, prefix="/files")
router.include_router(users_router, prefix="/users")
