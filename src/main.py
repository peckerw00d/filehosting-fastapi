from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from config import settings
from api import router as file_router
from service_layer.unit_of_work import DEFAULT_ASYNC_ENGINE


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    print("dispose database")
    await DEFAULT_ASYNC_ENGINE.dispose()


app = FastAPI()

app.include_router(file_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
