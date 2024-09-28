import json
import os
from datetime import datetime

import pytest
import requests
from result import Err, Ok

from app.models.subscription import VideoStatus
from app.routers import youtube


def mock_make_request(url: str, timeout: int) -> str:  # pylint: disable=W0613
    video_feed: str = os.path.join(os.path.dirname(__file__), "resources", "videos.xml")
    with open(video_feed, encoding="utf-8") as file:
        return file.read()


def test_fetch_videos_from_rss_feed() -> None:
    result = youtube.fetch_videos_from_rss_feed("http://test.com", request_maker=mock_make_request)

    match result:
        case Ok(videos):
            parsed_videos_path: str = os.path.join(os.path.dirname(__file__), "resources", "parsed_videos.json")
            with open(parsed_videos_path, encoding="utf-8") as f:
                expected_result = json.load(f)

            assert len(videos) == len(expected_result)

            for i, video in enumerate(videos):
                assert video.title == expected_result[i]["title"]
                assert video.published == datetime.fromisoformat(expected_result[i]["published"])
                assert video.video_id == expected_result[i]["video_id"]
                assert video.link == expected_result[i]["link"]
                assert video.author == expected_result[i]["author"]
                assert video.thumbnail_url == expected_result[i]["thumbnail"]["url"]
                assert video.status == VideoStatus.PENDING
        case Err(error):
            pytest.fail(f"Expected Ok result, but got Err: {error}")


def test_fetch_videos_from_empty_rss_feed() -> None:
    def mock_empty_feed(url: str, timeout: int) -> str:  # pylint: disable=W0613
        return """<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns="http://www.w3.org/2005/Atom">
        </feed>
        """

    result = youtube.fetch_videos_from_rss_feed("http://test.com", request_maker=mock_empty_feed)

    match result:
        case Ok(videos):
            pytest.fail(f"Expected Err result, but got Ok with {len(videos)} videos")
        case Err(error):
            assert isinstance(error, youtube.RssFeedError)
            assert error.error_type == youtube.RssFeedErrorType.EMPTY_FEED
            assert error.message == "No entries found in the RSS feed"


def test_fetch_videos_network_error() -> None:
    def mock_network_error(url: str, timeout: int) -> str:
        raise requests.RequestException("Network error occurred")

    result = youtube.fetch_videos_from_rss_feed("http://test.com", request_maker=mock_network_error)

    match result:
        case Ok(videos):
            pytest.fail(f"Expected Err result, but got Ok with {len(videos)} videos")
        case Err(error):
            assert isinstance(error, youtube.RssFeedError)
            assert error.error_type == youtube.RssFeedErrorType.NETWORK_ERROR
            assert "Network error occurred" in error.message
