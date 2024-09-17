from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
import yt_dlp

from app.yt_downloader import (
    MetadataError,
    MetadataErrorType,
    MetadataSuccess,
    VideoMetadata,
    get_metadata,
)


# Custom exception to mock yt_dlp.utils.DownloadError
class MockDownloadError(Exception):
    pass


@pytest.mark.asyncio
async def test_get_metadata_success():
    mock_video_info = {
        "id": "test_id",
        "title": "Test Video",
        "uploader": "Test Uploader",
        "upload_date": "20230101",
        "duration": 300,
        "description": "Test description",
        "thumbnail": "http://example.com/thumbnail.jpg"
    }
    
    with patch('app.yt_downloader.yt_dlp.YoutubeDL') as mock_ydl_class:
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.extract_info.return_value = mock_video_info
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl_instance
        
        result = await get_metadata(["http://example.com/video"])
        
        assert len(result) == 1
        assert isinstance(result[0], MetadataSuccess)
        assert result[0].url == "http://example.com/video"
        assert result[0].metadata == VideoMetadata(
            id="test_id",
            title="Test Video",
            uploader="Test Uploader",
            upload_date=datetime(2023, 1, 1),
            duration_in_seconds=300,
            description="Test description",
            thumbnail_url="http://example.com/thumbnail.jpg",
        )


@pytest.mark.parametrize("error_message, expected_error_type", [
    ("This live event will begin in a few moments", MetadataErrorType.LIVE_EVENT_NOT_STARTED),
    ("This video is unavailable", MetadataErrorType.VIDEO_UNAVAILABLE),
    ("This video contains content from Sony", MetadataErrorType.COPYRIGHT_STRIKE),
    ("Some other error", MetadataErrorType.UNKNOWN_ERROR)
])
@pytest.mark.asyncio
async def test_get_metadata_errors(error_message: str, expected_error_type: MetadataError):
    with patch('app.yt_downloader.yt_dlp.YoutubeDL') as mock_ydl_class:
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.extract_info.side_effect = yt_dlp.utils.DownloadError(error_message)  # type:ignore
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl_instance
        
        result = await get_metadata(["http://example.com/video"])
        
        assert len(result) == 1
        assert isinstance(result[0], MetadataError)
        assert result[0].url == "http://example.com/video"
        assert result[0].error_type == expected_error_type
        assert result[0].message == error_message

@pytest.mark.asyncio
async def test_get_metadata_multiple_urls():
    mock_video_info1 = {
        "id": "test_id1",
        "title": "Test Video 1",
        "uploader": "Test Uploader 1",
        "upload_date": "20230101",
        "duration": 300,
        "description": "Test description 1",
        "thumbnail": "http://example.com/thumbnail1.jpg"
    }
    mock_video_info2 = {
        "id": "test_id2",
        "title": "Test Video 2",
        "uploader": "Test Uploader 2",
        "upload_date": "20230202",
        "duration": 400,
        "description": "Test description 2",
        "thumbnail": "http://example.com/thumbnail2.jpg"
    }
    
    with patch('app.yt_downloader.yt_dlp.YoutubeDL') as mock_ydl_class:
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.extract_info.side_effect = [
            mock_video_info1,
            yt_dlp.utils.DownloadError("This video is unavailable"),
            mock_video_info2
        ]
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl_instance
        
        result = await get_metadata([
            "http://example.com/video1",
            "http://example.com/video2",
            "http://example.com/video3"
        ])
        
        assert len(result) == 3
        assert isinstance(result[0], MetadataSuccess)
        assert isinstance(result[1], MetadataError)
        assert isinstance(result[2], MetadataSuccess)
        assert result[1].error_type == MetadataErrorType.VIDEO_UNAVAILABLE
