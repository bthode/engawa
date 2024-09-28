import logging
from collections.abc import Callable
from datetime import datetime
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag
from fastapi import APIRouter, HTTPException
from result import Err, Ok, Result

from app.config import TIMEOUT_IN_SECONDS
from app.models.subscription import ChannelInfo, Video, VideoStatus

router = APIRouter()


logger = logging.getLogger(__name__)


class RssFeedErrorType(Enum):
    NETWORK_ERROR = "Network Error"
    PARSING_ERROR = "Parsing Error"
    EMPTY_FEED = "Empty Feed"
    UNKNOWN_ERROR = "Unknown Error"


class RssFeedError:
    def __init__(self, error_type: RssFeedErrorType, message: str):
        self.error_type = error_type
        self.message = message


RssFeedResult = Result[list[Video], RssFeedError]


@staticmethod
def make_request(url: str, timeout: int) -> str:
    response = requests.get(url, timeout=timeout)
    return response.content.decode("utf-8")


@staticmethod
def fetch_rss_feed(channel_url: str, request_maker: Callable[[str, int], str] = make_request) -> ChannelInfo:
    response_content = request_maker(channel_url, TIMEOUT_IN_SECONDS)
    soup = BeautifulSoup(response_content, "html.parser")

    # Fetch HTML title
    title = soup.title.string if soup.title else None
    if title is None:
        raise ValueError("Title not found")

    description = soup.find("meta", attrs={"name": "description"})
    if description is None:
        raise ValueError("Description not found")
    assert isinstance(description, Tag), "Description is not a Tag object"
    if not description.get("content"):
        raise ValueError("Description content not found")
    description_content = str(description["content"])

    # Fetch RSS link
    rss_link = soup.select_one('link[type="application/rss+xml"][title="RSS"]')
    if rss_link is None or not rss_link.get("href"):
        raise ValueError("RSS link not found")
    rss_href = rss_link["href"]
    rss_href = rss_href[0] if isinstance(rss_href, list) else rss_href

    # Fetch image link
    image_link = soup.select_one('link[rel="image_src"]')
    if image_link is None or not image_link.get("href"):
        raise ValueError("Image link not found")
    image_href = image_link["href"]
    image_href = image_href[0] if isinstance(image_href, list) else image_href

    return ChannelInfo(title=title, rss_link=rss_href, image_link=image_href, description=description_content)


@staticmethod
def fetch_videos_from_rss_feed(rss_url: str, request_maker: Callable[[str, int], str] = make_request) -> RssFeedResult:
    try:
        response_content = request_maker(rss_url, TIMEOUT_IN_SECONDS)
        soup = BeautifulSoup(response_content, "xml")

        entries = soup.find_all("entry")
        if not entries:
            # TODO: Is this actually an error case?
            return Err(RssFeedError(RssFeedErrorType.EMPTY_FEED, "No entries found in the RSS feed"))

        videos: list[Video] = []
        for entry in entries:
            video = Video(
                title=entry.find("title").text,
                published=datetime.fromisoformat(entry.find("published").text),
                video_id=entry.find("yt:videoId").text,
                link=entry.find("link").get("href"),
                author=entry.find("author").find("name").text,
                description=(
                    entry.find("media:group").find("media:description").text if entry.find("media:group") else ""
                ),
                thumbnail_url=entry.find("media:thumbnail").get("url"),
                status=VideoStatus.PENDING,
            )
            videos.append(video)

        return Ok(videos)

    except requests.RequestException as e:
        return Err(RssFeedError(RssFeedErrorType.NETWORK_ERROR, str(e)))
    except Exception as e:  # pylint: disable=broad-except
        return Err(RssFeedError(RssFeedErrorType.UNKNOWN_ERROR, str(e)))


@router.post("/get_channel_info")
async def fetch_rss_route(channel_url: str) -> ChannelInfo:
    return fetch_rss_feed(channel_url)


@router.get("/get_videos")
async def get_videos_route(rss_url: str) -> list[Video]:
    result: RssFeedResult = fetch_videos_from_rss_feed(rss_url)

    match result:
        case Ok(videos):
            return videos
        case Err(error):
            error_message = f"Failed to fetch videos: {error.error_type.value} - {error.message}"
            if error.error_type == RssFeedErrorType.NETWORK_ERROR:
                raise HTTPException(status_code=503, detail=error_message)
            elif error.error_type == RssFeedErrorType.EMPTY_FEED:
                return []
            else:
                raise HTTPException(status_code=500, detail=error_message)
