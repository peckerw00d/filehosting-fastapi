from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI

from core.config import settings
from core.models import db_helper

from api import router as file_router
from api import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    print("dispose database")
    await db_helper.dispose()


app = FastAPI()

app.include_router(file_router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
