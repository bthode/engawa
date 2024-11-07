import asyncio
import concurrent.futures
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import yt_dlp

from app.models.subscription import MetadataErrorType

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


async def mock_download_content(video_url: str, output_path: str) -> str:
    print(f"Downloading content from {video_url} to {output_path}")
    return f"{output_path}/example_video.mp4"


async def download_content(video_url: str, output_path: str) -> str:
    print(f"Downloading content from {video_url} to {output_path}")
    ydl_opts: dict[str, Any] = {
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        "format": "best",
        "postprocessing": [
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


def obtain_channel_data(channel_url: str) -> dict[str, Any]:
    ydl_opts: dict[str, Any] = {
        "logger": logger,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
        channel_info = ydl.extract_info(channel_url, download=False, process=True)  # pyright: ignore
    return channel_info  # type: ignore


def extract_info(url: str) -> MetadataResult:
    try:
        ydl_opts: dict[str, Any] = {
            "logger": logger,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
            video_info = ydl.extract_info(url, download=False)  # pyright: ignore

        # TODO: Validate field values
        metadata = VideoMetadata(
            id=video_info["id"],  # type:ignore
            title=video_info["title"],  # type:ignore
            uploader=video_info["uploader"],  # type:ignore
            upload_date=datetime.strptime(video_info["upload_date"], "%Y%m%d"),  # type:ignore
            duration_in_seconds=int(video_info["duration"]),  # type:ignore
            description=video_info["description"],  # type:ignore
            thumbnail_url=video_info["thumbnail"],  # type:ignore
        )
        return MetadataSuccess(url=url, metadata=metadata)
    except yt_dlp.utils.DownloadError as e:  # type: ignore[arg-type]
        error_message: str = str(e)  # type: ignore[arg-type]
        if "This live event will begin in a few moments" in error_message:
            return MetadataError(url, MetadataErrorType.LIVE_EVENT_NOT_STARTED, error_message)
        if "This video is unavailable" in error_message:
            return MetadataError(url, MetadataErrorType.VIDEO_UNAVAILABLE, error_message)
        if "This video contains content from" in error_message:
            return MetadataError(url, MetadataErrorType.COPYRIGHT_STRIKE, error_message)
        if "inappropriate for some users" in error_message:
            return MetadataError(url, MetadataErrorType.AGE_RESTRICTED, error_message)
        else:
            return MetadataError(url, MetadataErrorType.UNKNOWN_ERROR, error_message)
    except Exception as e:  # pylint: disable=broad-except
        logging.error(e)
        return MetadataError(url, MetadataErrorType.UNKNOWN_ERROR, str(e))


async def get_metadata(urls: list[str]) -> list[MetadataResult]:
    loop = asyncio.get_running_loop()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [loop.run_in_executor(executor, extract_info, url) for url in urls]
        results = await asyncio.gather(*futures)

    return results
