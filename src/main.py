from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from config import settings
from adapters.orm import db_helper

from api import router as file_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    print("dispose database")
    await db_helper.dispose()


app = FastAPI()

app.include_router(file_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
