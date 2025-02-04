from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request, HTTPException, status

from config import settings
from api import router
from api.middleware import session_middleware
from service_layer.unit_of_work import DEFAULT_ASYNC_ENGINE


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    print("dispose database")
    await DEFAULT_ASYNC_ENGINE.dispose()


app = FastAPI()


app.middleware("http")(session_middleware)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
