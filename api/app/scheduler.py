import logging
from datetime import datetime, timedelta
from typing import cast

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import or_, select

from app.database.session import get_session
from app.filters import apply_filters
from app.models.plex import Plex
from app.models.subscription import Subscription, Video, VideoStatus
from app.routers.subscription import sync_subscription
from app.yt_downloader import (
    MetadataError,
    MetadataErrorType,
    MetadataResult,
    MetadataSuccess,
    get_metadata,
)

logger = logging.getLogger(__name__)
SUBSCRIPTION_UPDATE_INTERVAL = 15


def update_video_status(video: Video, video_results: MetadataResult) -> Video:
    updates = {}
    match video_results:
        case MetadataSuccess():
            updates = {
                "thumbnail_url": video_results.metadata.thumbnail_url,
                "duration": video_results.metadata.duration_in_seconds,
                "status": VideoStatus.OBTAINED_METADATA,
            }
        case MetadataError(error_type=MetadataErrorType.LIVE_EVENT_NOT_STARTED | MetadataErrorType.VIDEO_UNAVAILABLE):
            updates = {"status": VideoStatus.EXCLUDED}
        case MetadataError(error_type=MetadataErrorType.COPYRIGHT_STRIKE):
            updates = {"status": VideoStatus.COPYRIGHT_STRIKE}
        case MetadataError(error_type=MetadataErrorType.UNKNOWN_ERROR):
            updates = {"status": VideoStatus.FAILED, "retry_count": video.retry_count + 1}
        case _:
            updates = {"status": VideoStatus.FAILED, "retry_count": video.retry_count + 1}

    for key, value in updates.items():
        setattr(video, key, value)
    return video


async def get_subscriptions_to_update(session: AsyncSession) -> list[Subscription]:
    fifteen_minutes_ago: datetime = datetime.now(utc) - timedelta(minutes=SUBSCRIPTION_UPDATE_INTERVAL)

    subscriptions_to_update = cast(
        list[Subscription],
        (
            await session.execute(  # pyright: ignore
                select(Subscription)
                .options(selectinload(Subscription.filters))
                .where(  # pyright: ignore
                    or_(
                        Subscription.last_updated == None,  # noqa: E711 pylint: disable=singleton-comparison
                        Subscription.last_updated < fifteen_minutes_ago,  # pyright: ignore
                    )
                )
            )
        )
        .scalars()
        .all(),
    )
    assert isinstance(subscriptions_to_update, list), "Should have received a list of subscriptions"
    return subscriptions_to_update


async def get_pending_videos(session: AsyncSession) -> list[Video]:
    results: list[Video] = (
        (
            await session.execute(  # pyright: ignore
                select(Video).where(Video.status == VideoStatus.PENDING).options(selectinload(Video.subscription))
            )
        )
        .scalars()
        .all()
    )  # pyright: ignore
    return results


async def get_videos_for_subscription(subscription_id: int, status: VideoStatus, session: AsyncSession) -> list[Video]:
    results: list[Video] = (
        (
            await session.execute(  # pyright: ignore
                select(Video)
                .where(Video.status == status)
                .where(Video.subscription_id == subscription_id)
                .options(selectinload(Video.subscription))
            )
        )
        .scalars()
        .all()
    )  # pyright: ignore
    return results


async def handle_videos_for_subscription(subscription: Subscription, session: AsyncSession) -> None:
    await sync_subscription(subscription.id, session)
    videos_with_metadata = await get_videos_for_subscription(subscription.id, VideoStatus.OBTAINED_METADATA, session)
    video_urls = [video.link for video in videos_with_metadata]
    metadata_results: list[MetadataResult] = await get_metadata(video_urls)
    video_dict: dict[str, Video] = {video.link: video for video in videos_with_metadata}
    for video_results in metadata_results:
        video = video_dict[video_results.url]
        update_video_status(video, video_results)


async def sync_and_update_videos():
    async for session in get_session():
        try:
            subscriptions_to_update = await get_subscriptions_to_update(session)

            if len(subscriptions_to_update) < 1:
                logger.info("No subscriptions to update")
            else:
                logger.info("Found %d subscriptions to update", len(subscriptions_to_update))

            for subscription in subscriptions_to_update:
                await sync_subscription(subscription.id, session)
                videos_to_obtain_metadata = await get_videos_for_subscription(
                    subscription.id, VideoStatus.PENDING, session
                )

                video_urls = [video.link for video in videos_to_obtain_metadata]
                metadata_results = await get_metadata(video_urls)

                updated_videos: list[Video] = []
                for video, metadata_result in zip(videos_to_obtain_metadata, metadata_results):
                    updated_video = update_video_status(video, metadata_result)
                    updated_videos.append(updated_video)

                # Apply filters to the updated videos
                filtered_videos = apply_filters(updated_videos, subscription.filters)

                for video in filtered_videos:
                    if video.status == VideoStatus.OBTAINED_METADATA:
                        video.status = VideoStatus.PENDING_DOWNLOAD
                    session.add(video)

                subscription.last_updated = datetime.now(utc)
                session.add(subscription)

            await session.commit()

        except Exception as e:
            logger.error("Error in sync_and_update_videos: %s", str(e))
            await session.rollback()
            raise


async def update_plex_library(session: AsyncSession) -> None:
    # updated_video_subscriptions = {video.subscription_id for video in pending_videos}
    # logger.warning("Acted on videos from subscription ids: %s", updated_video_subscriptions)
    result = await session.execute(select(Plex).limit(1))
    plex: Plex | None = result.scalars().first()

    if plex is None:
        logging.warning("Not refreshing Plex library as no Plex server is added.")
        return

    plex_endpoint = plex.endpoint
    plex_token = plex.token
    plex_port = plex.port
    library_key = "15"  # TODO: Obtain the real library keys

    url = f"http://{plex_endpoint}:{plex_port}/library/sections/{library_key}/refresh?X-Plex-Token={plex_token}"

    async with httpx.AsyncClient() as http_session:
        response = await http_session.get(url)
        if response.status_code == 200:
            logging.info("Updated Plex Library")
        else:
            raise ValueError(f"Failed to fetch data from {url}, status code: {response.status_code}")


scheduler = AsyncIOScheduler(timezone=utc)

scheduler.add_job(  # type: ignore
    sync_and_update_videos,
    "interval",
    seconds=10,
)
