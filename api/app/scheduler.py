import asyncio
import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from sqlmodel import or_, select

from app.database.session import get_session
from app.models.subscription import Subscription, Video, VideoStatus
from app.routers.subscription import sync_subscription
from app.yt_downloader import (
    VideoError,
    VideoMetadataError,
    extract_metadata,
    obtain_metadata,
)

logger = logging.getLogger(__name__)


async def async_sync_and_update_videos():
    async for session in get_session():
        try:
            fifteen_minutes_ago: datetime = datetime.now(utc) - timedelta(minutes=15)
            result = await session.execute(  # type: ignore
                select(Subscription).where(
                    or_(
                        Subscription.last_updated == None,  # noqa: E711 pylint: disable=singleton-comparison
                        Subscription.last_updated < fifteen_minutes_ago,
                    )  # type: ignore
                )
            )

            subscriptions_to_update: list[Subscription] = result.scalars().all()  # type: ignore
            assert subscriptions_to_update is not None, "Subscriptions list should not be None"
            assert isinstance(subscriptions_to_update, list), "Subscriptions should be a list"

            if len(subscriptions_to_update) == 0:
                logger.info("No subscriptions to update")
            else:
                logger.info("Found %d subscriptions to update", len(subscriptions_to_update))

            for subscription in subscriptions_to_update:
                await sync_subscription(subscription.id, session)

            # Step 3: Get pending videos
            result = await session.execute(select(Video).where(Video.status == VideoStatus.PENDING))  # type: ignore
            pending_videos: list[Video] = result.scalars().all()  # type: ignore

            assert pending_videos is not None, "Pending videos list should not be None"
            assert isinstance(pending_videos, list), "Pending videos should be a list"
            if len(pending_videos) == 0:
                logger.info("No pending videos")
            else:
                logger.info("Found %s pending videos", len(pending_videos))

            # Step 4: Update metadata for each pending video
            for video in pending_videos:
                try:
                    try:
                        metadata_dict = obtain_metadata(video.link)
                        metadata = extract_metadata(metadata_dict)

                        # Update video with new metadata
                        video.thumbnail_url = metadata.thumbnail_url
                        video.duration = metadata.duration_in_seconds
                        video.status = VideoStatus.OBTAINED_METADATA  # Or another appropriate status
                    except VideoMetadataError as e:
                        if e.error_type == VideoError.LIVE_EVENT_NOT_STARTED:
                            video.status = VideoStatus.EXCLUDED
                        elif e.error_type == VideoError.VIDEO_UNAVAILABLE:
                            video.status = VideoStatus.EXCLUDED
                        else:
                            video.status = VideoStatus.FAILED
                    await session.commit()
                except Exception as e:
                    print(f"Error processing video {video.id}: {str(e)}")
                    video.status = VideoStatus.FAILED
                    video.retry_count += 1  # type: ignore
                    await session.commit()
        except Exception as e:  # pylint: disable=broad-except
            print(f"An error occurred during job execution: {str(e)}")
            await session.rollback()
        finally:
            await session.close()


async def my_job():
    logging.info("🤣🤣🤣🤣🤣🤣🤣")


# Create the AsyncIOScheduler
scheduler = AsyncIOScheduler(timezone=utc)

# Add jobs to the scheduler
scheduler.add_job(async_sync_and_update_videos, "interval", seconds=10)  # type: ignore


# Function to start the scheduler
async def start_scheduler():
    scheduler.start()
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
