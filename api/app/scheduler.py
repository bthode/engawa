import asyncio
import logging
from datetime import datetime, timedelta

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
from pytz import utc
from sqlalchemy.future import select

# from app.database.session import engine
from app.database.session import get_session
from app.models.subscription import Subscription, Video, VideoStatus
from app.routers.subscription import sync_subscription
from app.yt_downloader import extract_metadata, obtain_metadata

logger = logging.getLogger(__name__)


async def async_sync_and_update_videos():
    async for session in get_session():
        try:
            # Step 1: Get subscriptions that need updating
            fifteen_minutes_ago = datetime.now(utc) - timedelta(minutes=15)
            result = await session.execute(
                select(Subscription).where(
                    (Subscription.last_updated == None) | (Subscription.last_updated < fifteen_minutes_ago)
                )
            )
            subscriptions_to_update: list[Subscription] = result.scalars().all()

            if len(subscriptions_to_update) == 0:
                logger.info("No subscriptions to update")
            else:
                logger.info(f"Found {len(subscriptions_to_update)} subscriptions to update")

            for subscription in subscriptions_to_update:
                await sync_subscription(subscription.id, session)

            # Step 3: Get pending videos
            result = await session.execute(
                select(Video).where(Video.status == VideoStatus.PENDING)
            )
            pending_videos: list[Video] = result.scalars().all()

            # Step 4: Update metadata for each pending video
            for video in pending_videos:
                try:
                    metadata_dict = obtain_metadata(video.link)
                    metadata = extract_metadata(metadata_dict)
                    
                    # Update video with new metadata
                    video.thumbnail_url = metadata.thumbnail_url
                    video.duration_in_seconds = metadata.duration_in_seconds
                    video.status = VideoStatus.OBTAINED_METADATA  # Or another appropriate status
                    
                    await session.commit()
                except Exception as e:
                    print(f"Error processing video {video.id}: {str(e)}")
                    video.status = VideoStatus.FAILED
                    video.retry_count += 1
                    await session.commit()

        except Exception as e:  # pylint: disable=broad-except
            print(f"An error occurred during job execution: {str(e)}")
            await session.rollback()
        finally:
            await session.close()

def sync_and_update_videos():
    """
    Synchronous wrapper for the asynchronous sync_and_update_videos function.
    This is the function that will be called by APScheduler.
    """
    asyncio.run(async_sync_and_update_videos())

def my_job():
    logging.info("🤣🤣🤣🤣🤣🤣🤣")


executors = {
    "default": ThreadPoolExecutor(1)
}

scheduler: BackgroundScheduler = BackgroundScheduler()  # type:ignore

scheduler.add_job(my_job, 'interval', seconds=10)  # type: ignore
scheduler.add_job(sync_and_update_videos, 'interval', seconds=10)  # type: ignore

scheduler.start()  # type: ignore
