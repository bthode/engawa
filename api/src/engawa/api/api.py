import logging
from typing import Callable, Dict

import requests
from bs4 import BeautifulSoup, Tag
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows CORS for this specific origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

logger = logging.getLogger(__name__)

TIMEOUT_IN_SECONDS = 5


class ChannelURL(BaseModel):
    channel_url: str


def read_from_plex_server() -> str:
    logger.info("Making a read request to the Plex server...")
    return "Read data from Plex server"


def update_plex_server() -> str:
    logger.info("Making an update request to the Plex server...")
    return "Updated data on the Plex server"


def make_request(url: str, timeout: int) -> str:
    response = requests.get(url, timeout=timeout)
    return response.content.decode("utf-8")


def fetch_rss_feed(channel_url: str, request_maker: Callable[[str, int], str] = make_request) -> Dict[str, str]:
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


@app.get("/read")
async def read_route(response_generator: Callable[[], str] = read_from_plex_server) -> str:
    return response_generator()


@app.post("/update")
async def update_route(response_generator: Callable[[], str] = update_plex_server) -> str:
    return response_generator()


@app.post("/fetch_rss")
async def fetch_rss_route(channel_url: ChannelURL) -> Dict[str, str]:
    return fetch_rss_feed(channel_url.channel_url)


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)
