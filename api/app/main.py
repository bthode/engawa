import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.database.session import engine
from app.routers.router import base_router as router
from app.scheduler import scheduler

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s")
logging.getLogger("uvicorn.access").setLevel(logging.INFO)
logging.getLogger("aiosqlite").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
logging.getLogger("apscheduler").setLevel(logging.ERROR)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    if not scheduler.running:
        scheduler.start()  # type: ignore

    yield

    if scheduler.running:
        scheduler.shutdown()  # type: ignore

    await engine.dispose()


app = FastAPI(title="Engawa", lifespan=lifespan)
app.include_router(router=router, prefix="/api")

ENDPOINT = "http://localhost"
PORT = "3000"
url = f"{ENDPOINT}:{PORT}"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
