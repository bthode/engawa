import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any

import yt_dlp

logger = logging.getLogger(__name__)


@dataclass
class VideoFormat:  # ignore:too-many-instance-attributes
    format_id: str
    format_note: str | None
    ext: str
    resolution: str | None
    fps: int | None
    vcodec: str | None
    acodec: str | None
    filesize: int | None


@dataclass
class VideoMetadata:
    id: str
    title: str
    uploader: str
    upload_date: datetime
    duration_in_seconds: int
    description: str
    thumbnail_url: str | None


class VideoError(Enum):
    LIVE_EVENT_NOT_STARTED = auto()
    VIDEO_UNAVAILABLE = auto()
    UNKNOWN_ERROR = auto()
    COPYRIGHT_STRIKE = auto()


class VideoMetadataError(Exception):
    def __init__(self, error_type: VideoError, message: str):
        self.error_type = error_type
        self.message = message
        super().__init__(self.message)


async def download_content(video_url: str, output_path: str) -> str:
    print(f"Downloading content from {video_url} to {output_path}")
    ydl_opts: dict[str, Any] = {
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        "format": "best",
        "postprocessors": [
            {
                "key": "FFmpegVideoConvert",
                "preferredquality": "135",
                "preferredformat": "mp4",
            }
        ],
        "logger": logger,  # type: ignore
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
        ydl.download([video_url])
    return f"{output_path}/example_video.mp4"


async def get_metadata(video_url: str) -> VideoMetadata:
    try:
        # Initialize yt_dlp options
        ydl_opts: dict[str, Any] = {
            "logger": logger,
        }

        # Extract video information
        loop = asyncio.get_running_loop()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
            video_metadata: dict[str, Any] = await loop.run_in_executor(  # type: ignore
                None, 
                lambda: ydl.extract_info(video_url, False)  # type: ignore
            )

        # Check for required fields
        required_fields = ["id", "title", "uploader", "upload_date", "duration", "description"]
        for field in required_fields:
            if field not in video_metadata:
                raise KeyError(f"Required field '{field}' is missing from video metadata")

        return VideoMetadata(
            id=video_metadata["id"],  # pyright: ignore
            title=video_metadata["title"],  # pyright: ignore
            uploader=video_metadata["uploader"],  # pyright: ignore
            upload_date=datetime.strptime(video_metadata["upload_date"], "%Y%m%d"),  # pyright: ignore
            duration_in_seconds=int(video_metadata["duration"]),  # pyright: ignore
            description=video_metadata["description"],  # pyright: ignore
            thumbnail_url=video_metadata["thumbnail"],  # pyright: ignore
        )
    
    except KeyError as e:
        logger.error("Missing required metadata for %s: %s", video_url, str(e))
        raise VideoMetadataError(
            VideoError.UNKNOWN_ERROR, f"Missing required metadata for {video_url}: {str(e)}"
        ) from e
    except yt_dlp.utils.DownloadError as e:  # type: ignore
        error_message = str(e)  # type: ignore
        match error_message:
            case _ if "This live event will begin in a few moments" in error_message:
                raise VideoMetadataError(
                    VideoError.LIVE_EVENT_NOT_STARTED, f"Live event hasn't started yet for {video_url}"
                ) from e
            case _ if "This video is unavailable" in error_message:
                raise VideoMetadataError(VideoError.VIDEO_UNAVAILABLE, f"Video is unavailable for {video_url}") from e
            case _ if "This video contains content from" in error_message:
                raise VideoMetadataError(VideoError.COPYRIGHT_STRIKE, f"Video is unavailable for {video_url}") from e
            case _:
                logger.error("Error obtaining metadata for %s: %s", video_url, error_message)
                raise VideoMetadataError(
                    VideoError.UNKNOWN_ERROR, f"Error obtaining metadata for {video_url}: {error_message}"
                ) from e
    except Exception as e:
        logger.error("Unexpected error obtaining metadata for %s: %s", video_url, str(e))
        raise VideoMetadataError(
            VideoError.UNKNOWN_ERROR, f"Unexpected error occurred for {video_url}: {str(e)}"
        ) from e
