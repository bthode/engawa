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
    match video_results:
        case MetadataSuccess():
            return Video(
                **video.model_dump(),
                thumbnail_url=video_results.metadata.thumbnail_url,
                duration=video_results.metadata.duration_in_seconds,
                status=VideoStatus.OBTAINED_METADATA,
            )
        case MetadataError(error_type=MetadataErrorType.LIVE_EVENT_NOT_STARTED | MetadataErrorType.VIDEO_UNAVAILABLE):
            return Video(**video.model_dump(), status=VideoStatus.EXCLUDED)
        case MetadataError(error_type=MetadataErrorType.COPYRIGHT_STRIKE):
            return Video(**video.model_dump(), status=VideoStatus.COPYRIGHT_STRIKE)
        case MetadataError(error_type=MetadataErrorType.UNKNOWN_ERROR):
            return Video(**video.model_dump(), status=VideoStatus.FAILED, retry_count=video.retry_count + 1)
        case _:
            return Video(**video.model_dump(), status=VideoStatus.FAILED, retry_count=video.retry_count + 1)


async def get_subscriptions_to_update(session: AsyncSession) -> list[Subscription]:
    fifteen_minutes_ago: datetime = datetime.now(utc) - timedelta(minutes=SUBSCRIPTION_UPDATE_INTERVAL)

    subscriptions_to_update = cast(
        list[Subscription],
        (
            await session.execute(  # pyright: ignore
                select(Subscription).where(  # pyright: ignore
                    or_(
                        Subscription.last_updated == None,  # pylint: disable=singleton-comparison  noqa: E712
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


#### ----
#### ----
#### ----

#  TODO: Need to refactor the sync method to handle vidoes by subscription
#  Then we can call it for our above subscription
# and verify the video has been filtered out by the duration filter


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


# TODO: Only use as a reference for how we might refactor
async def handle_subscription2(subscription_id: int, session: AsyncSession) -> None:
    await sync_subscription(subscription_id, session)
    videos_with_metadata = await get_videos_for_subscription(subscription_id, VideoStatus.PENDING, session)

    updated_videos = [
        update_video_status(video, metadata_result)
        for video, metadata_result in await get_metadata(videos_with_metadata)
    ]

    for video in updated_videos:
        session.add(video)
    await session.commit()


# TODO: We need to act on all vidoes that we've obtained metadata for.
# Other videos that have failed can likely be excluded without filters

# Update the Subscription
# Update the subscription's videos metadata
# Apply filtering to that collection of videos

#### ----
#### ----
#### ----
#### ----


async def sync_and_update_videos():
    async for session in get_session():
        try:
            subscriptions_to_update = await get_subscriptions_to_update(session)

            # region LOGGING
            if len(subscriptions_to_update) < 1:
                logger.info("No subscriptions to update")
            else:
                logger.info("Found %d subscriptions to update", len(subscriptions_to_update))
            # endregion

            updated_videos: list[Video] = []

            for subscription in subscriptions_to_update:
                await sync_subscription(subscription.id, session)
                videos_to_obtain_metadata = await get_videos_for_subscription(
                    subscription.id, VideoStatus.PENDING, session
                )
                # region LOGGING
                if not pending_videos:
                    logger.info("No pending videos")
                    return
                else:
                    logger.info("Found %s pending videos", len(pending_videos))
                #  endregion
                updated_videos = [
                    update_video_status(video, metadata_result)
                    for video, metadata_result in await get_metadata(videos_to_obtain_metadata)
                ]

            # updated_video_subscriptions = {video.subscription_id for video in pending_videos}
            # logger.warning("Acted on videos from subscription ids: %s", updated_video_subscriptions)
            await update_plex_library(session)

            await session.commit()

        except Exception as e:
            logger.error("Error in sync_and_update_videos: %s", str(e))
            await session.rollback()
            raise


async def update_plex_library(session: AsyncSession) -> None:
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
