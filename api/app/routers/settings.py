import shutil

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


class RequirementStatus(SQLModel):
    name: str
    available: bool
    path: str | None


class RequirementsCheckResult(SQLModel):
    ffmpeg: RequirementStatus
    ffprobe: RequirementStatus

@router.get("/settings/requirements", response_model=RequirementsCheckResult)
async def check_requirements():
    # Function to check if a command is available
    def check_command(command: str) -> RequirementStatus:
        path = shutil.which(command)
        return RequirementStatus(
            name=command,
            available=path is not None,
            path=path
        )
    
    # Check ffmpeg and ffprobe
    ffmpeg_status = check_command("ffmpeg")
    ffprobe_status = check_command("ffprobe")
    
    # Return the results
    return RequirementsCheckResult(
        ffmpeg=ffmpeg_status,
        ffprobe=ffprobe_status
    )
