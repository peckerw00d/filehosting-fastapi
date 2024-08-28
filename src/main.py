from contextlib import asynccontextmanager
import os
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.models import db_helper

from api import router as file_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    print("dispose database")
    await db_helper.dispose()


app = FastAPI()

app.include_router(file_router)


app.mount('/media', StaticFiles(directory=settings.static.media_dir), name="media")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
)
