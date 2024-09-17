import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
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


class MetadataErrorType(Enum):
    LIVE_EVENT_NOT_STARTED = "Live event not started"
    VIDEO_UNAVAILABLE = "Video unavailable"
    COPYRIGHT_STRIKE = "Copyright strike"
    UNKNOWN_ERROR = "Unknown error"


@dataclass
class MetadataError:
    url: str
    error_type: MetadataErrorType
    message: str


@dataclass
class MetadataSuccess:
    url: str
    metadata: VideoMetadata


MetadataResult = MetadataSuccess | MetadataError


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


async def get_metadata(urls: list[str]) -> list[MetadataResult]:
    async def process_url(url: str) -> MetadataResult:
        try:
            ydl_opts: dict[str, Any] = {
                "logger": logger,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # pyright: ignore
                video_info = await asyncio.to_thread(ydl.extract_info, url, download=False)  # pyright: ignore

            metadata = VideoMetadata(
                id=video_info["id"],
                title=video_info["title"],
                uploader=video_info["uploader"],
                upload_date=datetime.strptime(video_info["upload_date"], "%Y%m%d"),
                duration_in_seconds=int(video_info["duration"]),
                description=video_info["description"],
                thumbnail_url=video_info.get("thumbnail"),
            )
            return MetadataSuccess(url=url, metadata=metadata)

        except yt_dlp.utils.DownloadError as e:  # pyright: ignore
            error_message = str(e)
            if "This live event will begin in a few moments" in error_message:
                return MetadataError(url, MetadataErrorType.LIVE_EVENT_NOT_STARTED, error_message)
            elif "This video is unavailable" in error_message:
                return MetadataError(url, MetadataErrorType.VIDEO_UNAVAILABLE, error_message)
            elif "This video contains content from" in error_message:
                return MetadataError(url, MetadataErrorType.COPYRIGHT_STRIKE, error_message)
            else:
                return MetadataError(url, MetadataErrorType.UNKNOWN_ERROR, error_message)
        except Exception as e:  # pylint: disable=broad-except
            return MetadataError(url, MetadataErrorType.UNKNOWN_ERROR, str(e))

    return await asyncio.gather(*(process_url(url) for url in urls))
