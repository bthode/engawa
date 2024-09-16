import asyncio
import logging
from collections.abc import Sequence
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from sqlalchemy import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import or_, select

from app.database.session import get_session
from app.models.subscription import Subscription, Video, VideoStatus
from app.routers.subscription import sync_subscription
from app.yt_downloader import (
    VideoError,
    VideoMetadata,
    VideoMetadataError,
    get_metadata,
)

logger = logging.getLogger(__name__)

SUBSCRIPTION_UPDATE_INTERVAL = 15


async def sync_and_update_videos(session: AsyncSession):
    async for session in get_session():
        try:
            fifteen_minutes_ago: datetime = datetime.now(utc) - timedelta(minutes=15)

            # Fetch subscriptions to update
            result: ScalarResult[Subscription] | None = await session.execute(
                select(Subscription).where(
                    or_(
                        Subscription.last_updated.is_(None),
                        Subscription.last_updated < fifteen_minutes_ago,
                    )
                )
            )
            subscriptions_to_update: Sequence[Subscription] = result.scalars().all()

            if not subscriptions_to_update:
                logger.info("No subscriptions to update")
            else:
                logger.info("Found %d subscriptions to update", len(subscriptions_to_update))
                await asyncio.gather(*(sync_subscription(sub.id, session) for sub in subscriptions_to_update))

            # Fetch pending videos
            result = await session.execute(
                select(Video).where(Video.status == VideoStatus.PENDING).options(selectinload(Video.subscription))
            )
            pending_videos: Sequence[Video] = result.scalars().all()

            if not pending_videos:
                logger.info("No pending videos")
            else:
                logger.info("Found %s pending videos", len(pending_videos))

                # Create tasks for each video metadata fetch
                tasks = [process_video(video) for video in pending_videos]

                # Run tasks concurrently and wait for all to complete
                await asyncio.gather(*tasks)

            # Commit all changes
            await session.commit()

        except Exception as e:
            logger.error("Error in async_sync_and_update_videos: %s", str(e))
            await session.rollback()
            raise

        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error in async_sync_and_update_videos: %s", str(e))
            await session.rollback()
            raise


async def process_video(video: Video):
    try:
        metadata: VideoMetadata = await get_metadata(video.link)

        video.thumbnail_url = metadata.thumbnail_url
        video.duration = metadata.duration_in_seconds
        video.status = VideoStatus.OBTAINED_METADATA
    except VideoMetadataError as e:
        if e.error_type in (VideoError.LIVE_EVENT_NOT_STARTED, VideoError.VIDEO_UNAVAILABLE):
            video.status = VideoStatus.EXCLUDED
        else:
            video.status = VideoStatus.FAILED
    except Exception as e:
        logger.error("Error processing video %s: %s", video.id, str(e))
        video.status = VideoStatus.FAILED
        video.retry_count += 1


scheduler = AsyncIOScheduler(timezone=utc)

scheduler.add_job(  # type: ignore
    sync_and_update_videos,
    "interval",
    seconds=10,
    args=[get_session()],
)


async def start_scheduler():
    scheduler.start()
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
