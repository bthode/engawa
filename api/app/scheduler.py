import logging
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import cast

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import desc, or_, select

from app.database.session import get_session
from app.filters import applicable_filters
from app.models.plex import Plex
from app.models.subscription import (
    Filter,
    PlexLibraryDestination,
    RetentionPolicyModel,
    RetentionType,
    Subscription,
    Video,
    VideoStatus,
)
from app.routers.subscription import sync_subscription
from app.yt_downloader import (
    MetadataError,
    MetadataErrorType,
    MetadataResult,
    MetadataSuccess,
    get_metadata,
    mock_download_content,
)

logger = logging.getLogger(__name__)
SUBSCRIPTION_UPDATE_INTERVAL = 15
TEST_FILE_NAME = "test_engawa.tmp"

scheduler = AsyncIOScheduler(timezone=utc)


def verify_write_access(dir_path: str) -> bool:
    test_file = Path(dir_path) / TEST_FILE_NAME

    try:
        if test_file.exists():
            test_file.unlink()

        with test_file.open("w") as f:
            f.write("test")

        test_file.unlink()
        return True

    except Exception as e:  # pylint: disable=broad-except
        logger.error("Filesystem write access verification failed: %s", e)
        return False


async def process_retention_policy(
    session: AsyncSession, subscription_id: int, retention_policy: RetentionPolicyModel
) -> None:
    match retention_policy.type:
        case RetentionType.COUNT:
            count = retention_policy.videoCount
            statement = (
                select(Video)
                .where(Video.subscription_id == subscription_id)
                .where(Video.status == VideoStatus.DOWNLOADED)
                .order_by(desc(Video.published))
                .offset(count)
            )

        case RetentionType.DELTA:
            lookback_date = datetime.now() - retention_policy.timeDeltaTypeValue
            if lookback_date is None or datetime.now() < lookback_date or lookback_date is not date:
                return
            statement = select(Video).where(
                (Video.subscription_id == subscription_id) & (Video.published < lookback_date)
            )
        case RetentionType.DATE_SINCE:
            cutoff_date = retention_policy.dateBefore
            if cutoff_date is None or datetime.now() < cutoff_date or cutoff_date is not date:
                return
            statement = (
                select(Video).where(Video.subscription_id == subscription_id).where(Video.published < cutoff_date)
            )

    # Execute query with proper async context
    result = await session.execute(statement)
    videos_to_delete = result.scalars().all()

    # Batch update the videos
    for video in videos_to_delete:
        video.status = VideoStatus.DELETED

    # Commit the changes
    # await session.commit()


async def apply_retention_policy(
    subscription_id: int, retention_policy: RetentionPolicyModel, session: AsyncSession
) -> None:
    """Apply retention policy to videos for a given subscription.

    Args:
        subscription_id: ID of the subscription to apply policy to
        retention_policy: Retention policy to apply
        session: Database session
    """

    statement = None

    match retention_policy.type:
        case RetentionType.DATE_SINCE:
            cutoff_date = retention_policy.dateBefore
            if cutoff_date is None or datetime.now() < cutoff_date or cutoff_date is not date:
                return
            statement = (
                select(Video).where(Video.subscription_id == subscription_id).where(Video.published < cutoff_date)
            )

        case RetentionType.COUNT:
            # TODO: How should we handle the count updating if previously failed videos are now successful?
            count = retention_policy.videoCount
            statement = (
                select(Video)
                .where(Video.subscription_id == subscription_id)
                .where(Video.status == VideoStatus.DOWNLOADED)
                .order_by(desc(Video.published))
                .offset(count)
            )

        case RetentionType.DELTA:
            lookback_date = datetime.now() - retention_policy.timeDeltaTypeValue
            if lookback_date is None or datetime.now() < lookback_date or lookback_date is not date:
                return
            statement = (
                select(Video).where((Video.subscription_id == subscription_id) & (Video.published < lookback_date))
                # TODO: We have code to produce this delta elsewhere, should be refactored
            )

    # Mark videos for deletion
    result = await session.execute(statement)
    videos_to_delete = result.scalars().all()

    for video in videos_to_delete:
        video.status = VideoStatus.DELETED
        session.add(video)

    await session.commit()


def update_video_status(video: Video, video_results: MetadataResult) -> Video:
    updates = {}
    match video_results:
        case MetadataSuccess():
            updates = {
                "thumbnail_url": video_results.metadata.thumbnail_url,
                "duration": video_results.metadata.duration_in_seconds,
                "status": VideoStatus.OBTAINED_METADATA,
            }
            # TODO: Looks like we have some overlap in VideoStatus and MetadataErrorType
        case MetadataError(error_type=MetadataErrorType.LIVE_EVENT_NOT_STARTED | MetadataErrorType.VIDEO_UNAVAILABLE):
            updates = {"status": VideoStatus.EXCLUDED}
        case MetadataError(error_type=MetadataErrorType.COPYRIGHT_STRIKE):
            updates = {"status": VideoStatus.EXCLUDED, "metadata_error": MetadataErrorType.COPYRIGHT_STRIKE}
        case MetadataError(error_type=MetadataErrorType.AGE_RESTRICTED):
            updates = {"status": VideoStatus.EXCLUDED, "metadata_error": MetadataErrorType.AGE_RESTRICTED}
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
                .options(selectinload(Subscription.filters))  # type:ignore
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


async def rewrite_sync_and_update_videos():
    # update_subscriptions()
    # update_videos()
    # update_plex_library()
    pass


async def test_invoke():
    logger.info("Test invoke")


# Rough [Corrected] outline
# 1. Get subscriptions to update
# 2. For each subscription, sync the subscription
# 3. Get videos for the subscription that are pending metadata
# 4. Get metadata for the videos
# 5. Update the video status based on the metadata
# 6. Apply filters to the videos
# 7. Apply retention policy to the videos
# 7.a: Give special treatment to the count retention policy
# FIXIT: Can we do any early exclusions based on the filters or retention policy?
# 8. Commit the session
# 9. Download the videos that are pending download
# 10. Update Plex library
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

                # TODO: Need to retry failed videos
                # TODO: We shouldn't download videos if the retention policy is set to delete them

                video_urls = [video.link for video in videos_to_obtain_metadata]
                metadata_results = await get_metadata(video_urls)

                updated_videos: list[Video] = []
                for video, metadata_result in zip(videos_to_obtain_metadata, metadata_results):
                    # TODO: Update the video failure status here with MetadataErrorType

                    updated_video = update_video_status(video, metadata_result)
                    updated_videos.append(updated_video)

                asdf: dict[Video, list[Filter]] = applicable_filters(updated_videos, subscription.filters)
                logger.info("Applicable filters: %s", asdf)
                for video in updated_videos:
                    session.add(video)

                # TODO: This call is what is breaking greenlet await code
                # await process_retention_policy(session, subscription.id, subscription.retention_policy)
                # await apply_retention_policy(
                #     subscription_id=subscription.id, retention_policy=subscription.retention_policy, session=session
                # )

                to_download: list[Video] = await get_pending_videos(session)

                plex_results = await session.execute(select(Plex).options(selectinload(Plex.directories)))
                plex_server = plex_results.scalars().first()

                if plex_server is None:
                    logging.error("No Plex server found")

                download_path = (
                    await compute_library_path(plex_server, subscription.plex_library_path)
                    if isinstance(subscription.plex_library_path, PlexLibraryDestination)
                    else subscription.plex_library_path
                )

                if not verify_write_access(download_path):
                    logger.error("Write access verification failed for %s", download_path)
                    continue

                for video in to_download:
                    await mock_download_content(video.link, download_path)

                subscription.last_updated = datetime.now(utc)
                session.add(subscription)
                session.add(updated_videos)

            logger.info("Finished sync and update job")
            await session.commit()
            scheduler.add_job(test_invoke)  # type: ignore

        except Exception as e:
            logger.error("Error in sync_and_update_videos: %s", str(e))
            await session.rollback()
            raise


async def compute_library_path(plex_server: Plex | None, plex_library_path: PlexLibraryDestination) -> str:
    # TODO: Before we download any videos, ensure we can write to the download directory
    # In the error case, put the subscription in an error state and log the error
    directories = plex_server.directories
    directory = next((dir for dir in directories if dir.id == plex_library_path.directoryId), None)
    if directory is None:
        raise ValueError(f"Directory with id {plex_library_path.directoryId} not found")
    return directory.locations[0].path


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


scheduler.add_job(  # type: ignore
    sync_and_update_videos,
    "interval",
    seconds=10,
)
