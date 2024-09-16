from datetime import datetime
from typing import Any
from unittest.mock import Mock

import pytest
import yt_dlp

from app.yt_downloader import (
    VideoError,
    VideoMetadata,
    VideoMetadataError,
    get_metadata,
)


class MockDownloader:
    def __init__(self, mock_data: dict[str, dict[str, str | int]]):
        self.mock_data = mock_data

    async def extract_info(self, url: str) -> dict[str, Any]:
        if url in self.mock_data:
            return self.mock_data[url]
        raise yt_dlp.utils.DownloadError("Video not found")  # type: ignore


@pytest.mark.asyncio
async def test_obtain_metadata_success():
    mock_data: dict[str, dict[str, str]] = {
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ": {
            "id": "dQw4w9WgXcQ",
            "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
            "uploader": "Rick Astley",
            "upload_date": "20240529",
            "duration": "212",
            "description": "The official video for Never Gonna Give You Up by Rick Astley",
            "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
        }
    }

    expected_metadata: dict[str, str | int | datetime] = {
        "id": "dQw4w9WgXcQ",
        "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
        "uploader": "Rick Astley",
        "upload_date": datetime(2024, 5, 29),
        "duration_in_seconds": 212,
        "description": "The official video for Never Gonna Give You Up by Rick Astley",
        "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
    }
    
    downloader = MockDownloader(mock_data)
    result = await get_metadata("https://www.youtube.com/watch?v=dQw4w9WgXcQ", downloader)
    assert result == VideoMetadata(**expected_metadata)


@pytest.mark.asyncio
async def test_obtain_metadata_live_event_not_started():
    downloader = Mock()
    downloader.extract_info.side_effect = yt_dlp.utils.DownloadError("This live event will begin in a few moments")  # type: ignore

    with pytest.raises(VideoMetadataError) as exc_info:
        await get_metadata("https://www.youtube.com/watch?v=live", downloader)

    assert exc_info.value.error_type == VideoError.LIVE_EVENT_NOT_STARTED


@pytest.mark.asyncio
async def test_obtain_metadata_video_unavailable():
    downloader = Mock()
    downloader.extract_info.side_effect = yt_dlp.utils.DownloadError("This video is unavailable")  # type: ignore

    with pytest.raises(VideoMetadataError) as exc_info:
        await get_metadata("https://www.youtube.com/watch?v=unavailable", downloader)

    assert exc_info.value.error_type == VideoError.VIDEO_UNAVAILABLE


@pytest.mark.asyncio
async def test_obtain_metadata_unknown_error():
    downloader = Mock()
    downloader.extract_info.side_effect = Exception("Unknown error")

    with pytest.raises(VideoMetadataError) as exc_info:
        await get_metadata("https://www.youtube.com/watch?v=error", downloader)

    assert exc_info.value.error_type == VideoError.UNKNOWN_ERROR


@pytest.mark.asyncio
async def test_obtain_metadata_content_strike():
    downloader = Mock()
    downloader.extract_info.side_effect = yt_dlp.utils.DownloadError("This video contains content from")  # type: ignore

    with pytest.raises(VideoMetadataError) as exc_info:
        await get_metadata("https://www.youtube.com/watch?v=content_strike", downloader)

    assert exc_info.value.error_type == VideoError.COPYRIGHT_STRIKE

@pytest.mark.asyncio
@pytest.mark.skip(reason="Need to mock out the network call")
async def test_obtain_metadata_missing_required_fields(monkeypatch: pytest.MonkeyPatch):
    downloader = Mock()
    downloader.extract_info.return_value = {}

    with pytest.raises(VideoMetadataError) as exc_info:
        monkeypatch.setattr("app.yt_downloader.yt_dlp.YoutubeDL", MockDownloader)
        monkeypatch.setattr("app.yt_downloader.get_metadata", downloader)  # TODO: need to mock out the network call
        await get_metadata("https://www.youtube.com/watch?v=missing_fields")

    assert exc_info.value.error_type == VideoError.UNKNOWN_ERROR

@pytest.mark.asyncio
async def test_no_thumbnail_value(monkeypatch: pytest.MonkeyPatch):
    downloader = Mock()
    downloader.extract_info.return_value = {
        "id": "dQw4w9WgXcQ",
        "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
        "uploader": "Rick Astley",
        "upload_date": "20240529",
        "duration": "212",
        "description": "The official video for Never Gonna Give You Up by Rick Astley",
    }

    result: VideoMetadata = await get_metadata("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert result.thumbnail_url is None
