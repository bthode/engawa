import json
import os
import unittest

from app.models.subscription import Video
from app.routers import youtube


def mock_make_request(url: str, timeout: int) -> str:  # pylint: disable=W0613
    # Load the XML file
    video_feed: str = os.path.join(os.path.dirname(__file__), "resources", "videos.xml")
    with open(video_feed, encoding="utf-8") as file:
        return file.read()


class TestFetchVideosFromRssFeed(unittest.TestCase):
    def test_fetch_videos_from_rss_feed(self) -> None:
        result: list[Video] = youtube.fetch_videos_from_rss_feed("http://test.com", request_maker=mock_make_request)

        parsed_videos_path: str = os.path.join(os.path.dirname(__file__), "resources", "parsed_videos.json")
        with open(parsed_videos_path, encoding="utf-8") as f:
            expected_result = json.load(f)

        assert len(result) == len(expected_result)

        for i, video in enumerate(result):
            assert video.title == expected_result[i]["title"]
            assert video.published == expected_result[i]["published"]
            assert video.video_id == expected_result[i]["video_id"]
            assert video.link == expected_result[i]["link"]
            assert video.author == expected_result[i]["author"]
            assert video.thumbnail_url == expected_result[i]["thumbnail"]["url"]
