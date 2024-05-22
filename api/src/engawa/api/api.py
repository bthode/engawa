import logging
from collections.abc import Callable

from engawa.api.plex_service import PlexService, Video
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows CORS for this specific origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class ChannelURL(BaseModel):
    channel_url: str


class RSS_URL(BaseModel):
    rss_url: str


@app.get("/read")
async def read_route(response_generator: Callable[[], str] = PlexService.read_from_plex_server) -> str:
    return response_generator()


@app.post("/update")
async def update_route(response_generator: Callable[[], str] = PlexService.update_plex_server) -> str:
    return response_generator()


@app.post("/fetch_rss")
async def fetch_rss_route(channel_url: ChannelURL) -> dict[str, str]:
    return PlexService.fetch_rss_feed(channel_url.channel_url)


@app.get("/get_videos")  # Pretty sure we should be using the callable pattern here as well
async def get_videos_route(rss_url: RSS_URL) -> list[Video]:
    return PlexService.fetch_videos_from_rss_feed(rss_url.rss_url)


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)
