from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.database.session import engine
from app.routers.router import base_router as router

# # Database setup
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# engine = create_async_engine(DATABASE_URL, echo=True)
# SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


# # Dependency to get the session
# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#     async with SessionLocal() as session:
#         yield session


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Engawa", lifespan=lifespan)
app.include_router(router=router, prefix="/api")

endpoint = "http://localhost"
port = "3000"
url = f"{endpoint}:{port}"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
