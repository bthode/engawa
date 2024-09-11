from typing import Any
from unittest.mock import Mock

import pytest
import yt_dlp

from app.yt_downloader import VideoError, VideoMetadataError, obtain_metadata


class MockDownloader:
    def __init__(self, mock_data: dict[str, dict[str, str | int]]):
        self.mock_data = mock_data

    def extract_info(self, url: str) -> dict[str, Any]:
        if url in self.mock_data:
            return self.mock_data[url]
        raise yt_dlp.utils.DownloadError("Video not found")  # type: ignore


def test_obtain_metadata_success():
    mock_data: dict[str, dict[str, str | int]] = {
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ": {
            "id": "dQw4w9WgXcQ",
            "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
            "uploader": "Rick Astley",
            "upload_date": "20091025",
            "duration": 212,
            "description": "The official video for Never Gonna Give You Up by Rick Astley",
            "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
        }
    }
    downloader = MockDownloader(mock_data)
    result = obtain_metadata("https://www.youtube.com/watch?v=dQw4w9WgXcQ", downloader)
    assert result == mock_data["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]


def test_obtain_metadata_live_event_not_started():
    downloader = Mock()
    downloader.extract_info.side_effect = yt_dlp.utils.DownloadError("This live event will begin in a few moments")  # type: ignore

    with pytest.raises(VideoMetadataError) as exc_info:
        obtain_metadata("https://www.youtube.com/watch?v=live", downloader)

    assert exc_info.value.error_type == VideoError.LIVE_EVENT_NOT_STARTED


def test_obtain_metadata_video_unavailable():
    downloader = Mock()
    downloader.extract_info.side_effect = yt_dlp.utils.DownloadError("This video is unavailable")  # type: ignore

    with pytest.raises(VideoMetadataError) as exc_info:
        obtain_metadata("https://www.youtube.com/watch?v=unavailable", downloader)

    assert exc_info.value.error_type == VideoError.VIDEO_UNAVAILABLE


def test_obtain_metadata_unknown_error():
    downloader = Mock()
    downloader.extract_info.side_effect = Exception("Unknown error")

    with pytest.raises(VideoMetadataError) as exc_info:
        obtain_metadata("https://www.youtube.com/watch?v=error", downloader)

    assert exc_info.value.error_type == VideoError.UNKNOWN_ERROR


def test_obtain_metadata_content_strike():
    downloader = Mock()
    downloader.extract_info.side_effect = yt_dlp.utils.DownloadError("This video contains content from")  # type: ignore

    with pytest.raises(VideoMetadataError) as exc_info:
        obtain_metadata("https://www.youtube.com/watch?v=content_strike", downloader)

    assert exc_info.value.error_type == VideoError.COPYRIGHT_STRIKE
