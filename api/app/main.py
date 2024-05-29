from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from routers import youtube, plex

# from app.routers import plex, youtube

# Database setup
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=unused-argument
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(plex.router, prefix="/api")
app.include_router(youtube.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# from contextlib import asynccontextmanager

# from fastapi import FastAPI

# from .database import engine
# from .models import plex, youtube
# from .routers import plex


# @asynccontextmanager
# async def lifespan(app: FastAPI):  # pylint: disable=unused-argument
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)
#     yield
#     await engine.dispose()


# app = FastAPI(lifespan=lifespan)
# app.include_router(plex.router, prefix="/api")
