import concurrent.futures
from collections.abc import Callable
from datetime import datetime
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import yt_dlp

from app.yt_downloader import (
    MetadataError,
    MetadataErrorType,
    MetadataSuccess,
    VideoMetadata,
    extract_info,
    get_metadata,
)


class MockExecutor:
    def __init__(self, func: Callable[..., Any]) -> None:
        self.func: Callable[..., Any] = func

    def __enter__(self) -> "MockExecutor":
        return self

    def __exit__(self, exc_type: BaseException | None, exc_val: BaseException | None, exc_tb: Any | None) -> None:
        pass

    def submit(
        self, fn: Callable[..., Any], *args: Any, **kwargs: Any  # pylint: disable=unused-argument
    ) -> concurrent.futures.Future[Any]:
        future: concurrent.futures.Future[Any] = concurrent.futures.Future()
        future.set_result(self.func(*args, **kwargs))
        return future


@pytest.mark.asyncio
async def test_get_metadata_success():

    expected_metadata = VideoMetadata(
        id="test_id",
        title="Test Video",
        uploader="Test Uploader",
        upload_date=datetime(2023, 1, 1),
        duration_in_seconds=300,
        description="Test description",
        thumbnail_url="http://example.com/thumbnail.jpg",
    )

    def mock_extract_info(url: str):
        return MetadataSuccess(url=url, metadata=expected_metadata)

    mock_executor = MockExecutor(mock_extract_info)

    with patch("concurrent.futures.ProcessPoolExecutor", return_value=mock_executor):
        result = await get_metadata(["http://example.com/video"])

        assert len(result) == 1
        assert isinstance(result[0], MetadataSuccess)
        assert result[0].url == "http://example.com/video"
        assert result[0].metadata == expected_metadata
        assert result[0].metadata == VideoMetadata(
            id="test_id",
            title="Test Video",
            uploader="Test Uploader",
            upload_date=datetime(2023, 1, 1),
            duration_in_seconds=300,
            description="Test description",
            thumbnail_url="http://example.com/thumbnail.jpg",
        )


@pytest.mark.parametrize(
    "error_message, expected_error_type",
    [
        ("This live event will begin in a few moments", MetadataErrorType.LIVE_EVENT_NOT_STARTED),
        ("This video is unavailable", MetadataErrorType.VIDEO_UNAVAILABLE),
        ("This video contains content from Sony", MetadataErrorType.COPYRIGHT_STRIKE),
        ("Some other error", MetadataErrorType.UNKNOWN_ERROR),
    ],
)
def test_extract_info_errors(error_message: str, expected_error_type: MetadataErrorType):
    with patch("app.yt_downloader.yt_dlp.YoutubeDL") as mock_ydl_class:
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.extract_info.side_effect = yt_dlp.utils.DownloadError(error_message)  # type:ignore
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl_instance

        result = extract_info("http://example.com/video")

        assert isinstance(result, MetadataError)
        assert result.url == "http://example.com/video"
        assert result.error_type == expected_error_type
        assert result.message == error_message

        mock_ydl_instance.extract_info.assert_called_once_with("http://example.com/video", download=False)
