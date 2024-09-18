import logging
from datetime import datetime, timedelta
from typing import cast

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from sqlalchemy.orm import selectinload
from sqlmodel import or_, select

from app.database.session import get_session
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


def update_video_status(video: Video, video_results: MetadataResult) -> None:
    match video_results:
        case MetadataSuccess():
            video.thumbnail_url = video_results.metadata.thumbnail_url
            video.duration = video_results.metadata.duration_in_seconds
            video.status = VideoStatus.OBTAINED_METADATA
        case MetadataError(error_type=MetadataErrorType.LIVE_EVENT_NOT_STARTED | MetadataErrorType.VIDEO_UNAVAILABLE):
            video.status = VideoStatus.EXCLUDED
        case MetadataError(error_type=MetadataErrorType.COPYRIGHT_STRIKE):
            video.status = VideoStatus.COPYRIGHT_STRIKE
        case MetadataError(error_type=MetadataErrorType.UNKNOWN_ERROR):
            video.status = VideoStatus.FAILED
            video.retry_count += 1
            logger.error("Error processing video %s: %s", video.id, video_results.message)
        case _:
            video.status = VideoStatus.FAILED
            video.retry_count += 1
            logger.error("Unexpected result type: %s", type(video_results))


async def sync_and_update_videos():
    async for session in get_session():
        try:
            fifteen_minutes_ago: datetime = datetime.now(utc) - timedelta(minutes=15)

            subscriptions_to_update = cast(
                list[Subscription],
                (
                    await session.execute(  # pyright: ignore
                        select(Subscription).where(  # pyright: ignore
                            or_(
                                Subscription.last_updated.is_(None),  # pyright: ignore
                                Subscription.last_updated < fifteen_minutes_ago,  # pyright: ignore
                            )
                        )
                    )
                )
                .scalars()
                .all(),
            )
            assert isinstance(subscriptions_to_update, list), "Should have received a list of subscriptions"

            if not subscriptions_to_update:
                logger.info("No subscriptions to update")
            else:
                logger.info("Found %d subscriptions to update", len(subscriptions_to_update))
            for subscription in subscriptions_to_update:
                await sync_subscription(subscription.id, session)

            pending_videos: list[Video] = (
                (
                    await session.execute(  # pyright: ignore
                        select(Video)
                        .where(Video.status == VideoStatus.PENDING)
                        .options(selectinload(Video.subscription))
                        # .limit(5)
                    )
                )
                .scalars()
                .all()
            )  # pyright: ignore

            if not pending_videos:
                logger.info("No pending videos")
                return
            else:
                logger.info("Found %s pending videos", len(pending_videos))

            video_urls = [video.link for video in pending_videos]
            metadata_results: list[MetadataResult] = await get_metadata(video_urls)

            video_dict: dict[str, Video] = {video.link: video for video in pending_videos}

            for video_results in metadata_results:
                video = video_dict[video_results.url]
                update_video_status(video, video_results)

            await session.commit()

            # TODO: Need to update the plex library here once we have the library mapped.
            # Or at least once the videos have been finished downloading.
            # http://$PLEX_SERVER:32400/library/sections/$library_key/refresh?X-Plex-Token=$PLEX_TOKEN
        except Exception as e:
            logger.error("Error in sync_and_update_videos: %s", str(e))
            await session.rollback()
            raise


scheduler = AsyncIOScheduler(timezone=utc)

scheduler.add_job(  # type: ignore
    sync_and_update_videos,
    "interval",
    seconds=10,
)
