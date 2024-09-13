import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Protocol

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
    # view_count: int
    description: str
    thumbnail_url: str
    # formats: list[VideoFormat]


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


class Downloader(Protocol):
    def extract_info(self, url: str) -> dict[str, Any]: ...


class YoutubeDLDownloader:
    def __init__(self):
        self.ydl_opts: dict[str, Any] = {
            "logger": logger,
        }

    def extract_info(self, url: str) -> dict[str, Any]:
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:  # type: ignore
            return ydl.extract_info(url, download=False)  # type: ignore


# async def obtain_metadata(video_url: str, downloader: Downloader = YoutubeDLDownloader()) -> dict[str, Any]:
#     print(f"Obtaining metadata for {video_url}")
#     try:
#         info_dict = downloader.extract_info(video_url)
#         logger.info("Obtained metadata for %s: %s", video_url, info_dict)
#         return info_dict
#     except yt_dlp.utils.DownloadError as e:  # type: ignore
#         error_message = str(e)  # type: ignore
#         match error_message:
#             case _ if "This live event will begin in a few moments" in error_message:
#                 raise VideoMetadataError(
#                     VideoError.LIVE_EVENT_NOT_STARTED, f"Live event hasn't started yet for {video_url}"
#                 ) from e
#             case _ if "This video is unavailable" in error_message:
#                 raise VideoMetadataError(VideoError.VIDEO_UNAVAILABLE, f"Video is unavailable for {video_url}") from e
#             case _ if "This video contains content from" in error_message:
#                 raise VideoMetadataError(VideoError.COPYRIGHT_STRIKE, f"Video is unavailable for {video_url}") from e
#             case _:
#                 logger.error("Error obtaining metadata for %s: %s", video_url, error_message)
#                 raise VideoMetadataError(
#                     VideoError.UNKNOWN_ERROR, f"Error obtaining metadata for {video_url}: {error_message}"
#                 ) from e
#     except Exception as e:
#         logger.error("Unexpected error obtaining metadata for %s: %s", video_url, str(e))
#         raise VideoMetadataError(
#             VideoError.UNKNOWN_ERROR, f"Unexpected error occurred for {video_url}: {str(e)}"
#         ) from e


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


# async def extract_metadata(info_dict: dict[str, Any]) -> VideoMetadata:
# formats = [
#     VideoFormat(
#         format_id=format.get('format_id'),
#         format_note=format.get('format_note'),
#         ext=format.get('ext'),
#         resolution=format.get('resolution'),
#         fps=format.get('fps'),
#         vcodec=format.get('vcodec'),
#         acodec=format.get('acodec'),
#         filesize=format.get('filesize')
#     )
#     for format in info_dict.get('formats', [])
#     if isinstance(format, dict)
# ]

# return VideoMetadata(
#     id=info_dict["id"],
#     title=info_dict["title"],
#     uploader=info_dict["uploader"],
#     upload_date=datetime.strptime(info_dict["upload_date"], "%Y%m%d"),
#     duration_in_seconds=info_dict["duration"],
#     # view_count=info_dict['view_count'],
#     description=info_dict["description"],
#     thumbnail_url=info_dict["thumbnail"],
#     # formats=formats
# )


async def get_metadata(video_url: str, downloader: Downloader = YoutubeDLDownloader()) -> VideoMetadata:
    try:
        video_metadata: dict[str, Any] = downloader.extract_info(video_url)
        return VideoMetadata(
            id=video_metadata["id"],
            title=video_metadata["title"],
            uploader=video_metadata["uploader"],
            upload_date=datetime.strptime(video_metadata["upload_date"], "%Y%m%d"),
            duration_in_seconds=video_metadata["duration"],
            description=video_metadata["description"],
            thumbnail_url=video_metadata["thumbnail"],
        )
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
