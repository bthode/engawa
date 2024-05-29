from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

sqlite_file_name = "test.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"
engine = create_async_engine(sqlite_url, echo=True)


# Setup dependency for getting a session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session_local = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
    async with session_local() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def dispose_db():
    await engine.dispose()
