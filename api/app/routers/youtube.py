import logging
from collections.abc import Callable
from datetime import datetime

import requests
from bs4 import BeautifulSoup, Tag
from fastapi import APIRouter

from app.config import TIMEOUT_IN_SECONDS
from app.models.subscription import ChannelInfo, Video, VideoStatus

router = APIRouter()


logger = logging.getLogger(__name__)


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
def fetch_videos_from_rss_feed(rss_url: str, request_maker: Callable[[str, int], str] = make_request) -> list[Video]:
    try:
        response_content = request_maker(rss_url, TIMEOUT_IN_SECONDS)
        soup = BeautifulSoup(response_content, "xml")

        entries = soup.find_all("entry")
        videos: list[Video] = []
        for entry in entries:
            try:
                title = entry.find("title")
                published = entry.find("published")
                video_id = entry.find("yt:videoId")
                author = entry.find("author").find("name")
                link = entry.find("link").get("href")
                thumbnail_link: str = entry.find("media:thumbnail").get("url")
                description_tag = entry.find("media:group").find("media:description")
                description: str = description_tag.text if description_tag else ""

                if title and published and video_id and author:
                    video: Video = Video(
                        title=title.text,
                        published=datetime.fromisoformat(published.text),
                        video_id=video_id.text,
                        link=link,
                        author=author.text,
                        description=description,
                        thumbnail_url=thumbnail_link,
                        status=VideoStatus.PENDING,
                    )
                    videos.append(video)
                else:
                    logging.warning("Skipping entry due to missing required fields: %s", entry)
            except Exception as e:  # pylint: disable=broad-except
                logging.error("Error processing entry: %s", e)

        return videos
    except Exception as e:  # pylint: disable=broad-except
        logging.error("Error fetching videos from RSS feed: %s", e)
        return []


@router.post("/get_channel_info")
async def fetch_rss_route(channel_url: str) -> ChannelInfo:
    return fetch_rss_feed(channel_url)


@router.get("/get_videos")
async def get_videos_route(rss_url: str) -> list[Video]:
    return fetch_videos_from_rss_feed(rss_url)
