from fastapi import APIRouter
from sqlmodel import SQLModel

from app.database.session import engine

router = APIRouter()

@router.post("/settings/reset")
async def reset_database():
    try:
        # Drop all tables
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
        
        # Recreate all tables
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        
        return {"message": "Database reset successfully"}
    except Exception as e:  # pylint: disable=broad-except
        # Log the error (you might want to use a proper logging system)
        print(f"Error resetting database: {str(e)}")
