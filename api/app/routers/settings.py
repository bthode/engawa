from fastapi import APIRouter
from sqlmodel import SQLModel

from app.database.session import engine

router = APIRouter()


@router.post("/settings/reset")
async def reset_database():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        return {"message": "Database reset successfully"}
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error resetting database: {str(e)}")
