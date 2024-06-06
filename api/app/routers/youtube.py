from fastapi import APIRouter

from app.models.youtube import ChannelInfo, Video, Youtube

router = APIRouter()


@router.post("/get_channel_info")
async def fetch_rss_route(channel_url: str) -> ChannelInfo:
    return Youtube.fetch_rss_feed(channel_url)


@router.get("/get_videos")
async def get_videos_route(rss_url: str) -> list[Video]:
    return Youtube.fetch_videos_from_rss_feed(rss_url)
