from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.models import db_helper

from api import router as file_router

import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    print("dispose database")
    await db_helper.dispose()


app = FastAPI()

app.include_router(file_router)


base_dir = os.path.dirname(os.path.abspath(__file__))
media_dir = os.path.join(base_dir, "media")


app.mount('/media', StaticFiles(directory=media_dir), name="media")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
)
