from collections.abc import Callable
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

from config import TIMEOUT_IN_SECONDS


@dataclass
class Thumbnail:
    url: str
    width: str
    height: str


@dataclass
class Video:
    title: str
    published: str
    video_id: str
    link: str
    author: str
    thumbnail: Thumbnail


class Youtube:

    @staticmethod
    def make_request(url: str, timeout: int) -> str:
        response = requests.get(url, timeout=timeout)
        return response.content.decode("utf-8")

    @staticmethod
    def fetch_rss_feed(channel_url: str, request_maker: Callable[[str, int], str] = make_request) -> dict[str, str]:
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

        return {"title": title, "rss_link": rss_href, "image_link": image_href, "description": description_content}

    @staticmethod
    def fetch_videos_from_rss_feed(
        rss_url: str, request_maker: Callable[[str, int], str] = make_request
    ) -> list[Video]:
        response_content = request_maker(rss_url, TIMEOUT_IN_SECONDS)
        soup = BeautifulSoup(response_content, "xml")

        entries = soup.find_all("entry")
        videos: list[Video] = []
        for entry in entries:
            title = entry.find("title")
            published = entry.find("published")
            video_id = entry.find("yt:videoId")
            author = entry.find("author").find("name")
            link = entry.find("link").get("href")
            thumbnail_link: str = entry.find("media:thumbnail").get("url")
            thumbnail_width: str = entry.find("media:thumbnail").get("width")
            thumbnail_height: str = entry.find("media:thumbnail").get("height")

            if title and published and video_id and author:
                videos.append(
                    Video(
                        title=title.text,
                        published=published.text,
                        video_id=video_id.text,
                        link=link,
                        author=author.text,
                        thumbnail=Thumbnail(url=thumbnail_link, width=thumbnail_width, height=thumbnail_height),
                    )
                )

        return videos
