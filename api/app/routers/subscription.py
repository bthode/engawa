import base64
import logging
from datetime import datetime
from typing import Annotated

import requests
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends
from pytz import utc
from result import Err, Ok
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession

# from aiocache import cached
# from aiocache.serializers import PickleSerializer
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.database.session import get_session
from app.models.plex import Directory, Location, Plex
from app.models.subscription import (
    ComparisonOperator,
    Filter,
    FilterType,
    PlexLibraryDestination,
    RetentionType,
    Subscription,
    SubscriptionCreate,
    SubscriptionCreateV2,
    TimeDeltaTypeValue,
    Video,
    VideoStatus,
)
from app.routers import youtube
from app.yt_downloader import obtain_channel_data

router = APIRouter()


logger = logging.getLogger(__name__)


def produce_delta(delta: TimeDeltaTypeValue):
    time_delta = relativedelta(days=delta.days, weeks=delta.weeks, months=delta.months, years=delta.years)
    now = datetime.now(utc)
    return now - time_delta


@router.get("/subscription", response_model=list[Subscription])
async def get_all_subscription(session: Annotated[AsyncSession, Depends(get_session)]):
    statement = select(Subscription)
    results = await session.execute(statement)
    return results.scalars().all()


@router.post("/subscription")
async def create_subscription(create: SubscriptionCreate, session: Annotated[AsyncSession, Depends(get_session)]):
    existing_subscription = await session.execute(select(Subscription).where(Subscription.url == create.url))
    if existing_subscription.scalars().first():
        return {"message": "subscription already exists"}

    channel_info = youtube.fetch_rss_feed(create.url)
    image_link = channel_info.image_link

    image_data = None
    if image_link:
        response = requests.get(image_link, timeout=5)
        if response.status_code == 200:
            #  TODO: We should either store all images encoded or not encoded, not a mix
            image_data = base64.b64encode(response.content).decode("utf-8")

    subscription = Subscription(
        title=channel_info.title,
        url=create.url,
        rss_feed_url=channel_info.rss_link,
        description=channel_info.description,
        image=image_data if image_data is not None else None,
    )

    session.add(subscription)
    await session.commit()

    subscription_id = subscription.id

    new_filter = Filter(
        subscription_id=subscription_id,
        filter_type=FilterType.DURATION,
        comparison_operator=ComparisonOperator.GT,
        threshold_seconds=1800,
    )
    session.add(new_filter)
    await session.commit()
    return {"message": "subscription created"}


@router.delete("/subscription")
async def delete_all_subscriptions():
    return {"message": "subscriptions deleted"}


@router.get("/youtube_channel_info")
async def get_youtube_channel_info(channel_url: str):
    data = obtain_channel_data(channel_url)
    return data


# @cached(
#     ttl=300,
#     key_builder=lambda *args, **kwargs: f"subscription:{kwargs['subscription_id']}",  # type:ignore
#     serializer=PickleSerializer(),
# )
@router.get("/subscription/{subscription_id}", response_model=Subscription)
async def get_subscription(
    subscription_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> Subscription:
    result = await session.execute(select(Subscription).where(Subscription.id == subscription_id))
    subscription = result.scalars().first()
    assert subscription is not None and isinstance(subscription, Subscription)
    return subscription


@router.delete("/subscription/{subscription_id}")
async def delete_subscription(subscription_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    result = await session.execute(select(Subscription).where(Subscription.id == subscription_id))
    subscription = result.scalars().first()
    await session.delete(subscription)
    await session.commit()
    return {"message": "subscription deleted"}


# TODO: Refactor this method to it's own method. We need to know if there was an error in the calling
# sync_and_update_videos # Ideally we don't invoke any fastapi methods via sync_and_update_videos. Shouldn't really
# be a fastapi method at all.
# We might need to be able to invoke this logic when we do the multipart subscription add flow,
# but it should invoke another separate method.
@router.post("/subscription/{subscription_id}/sync", response_model=Subscription)
async def sync_subscription(subscription_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    subscription: Subscription = await get_subscription(subscription_id, session)  # type:ignore
    assert subscription is not None and isinstance(subscription, Subscription)
    result: youtube.RssFeedResult = youtube.fetch_videos_from_rss_feed(subscription.rss_feed_url)
    match result:
        case Ok(videos):
            for video in videos:
                existing_video = await session.execute(select(Video).where(Video.video_id == video.video_id))
                if not existing_video.scalars().first():
                    new_video = Video(
                        title=video.title,
                        published=video.published,
                        video_id=video.video_id,
                        link=video.link,
                        author=video.author,
                        thumbnail_url=video.thumbnail_url,
                        description=video.description,
                        subscription_id=subscription.id,
                        status=VideoStatus.PENDING,
                    )
                    session.add(new_video)

            subscription.last_updated = datetime.now(utc)
            session.add(subscription)

            await session.commit()
            return {"message": "subscription synced"}
        case Err(error):
            logger.error("Error syncing subscription %d: %s - %s", subscription_id, error.error_type, error.message)
            return {"message": f"Error syncing subscription: {error.error_type}"}


@router.get("/subscription/{subscription_id}/videos", response_model=list[Video])
async def get_subscription_videos(subscription_id: int, session: AsyncSession = Depends(get_session)) -> list[Video]:
    result = await session.execute(  # type:ignore
        select(Video).where(Video.subscription_id == subscription_id).order_by(desc(Video.published))  # type:ignore
    )
    return result.scalars().all()  # type:ignore


# async def get_subscription_data(channel_url: str) -> Subscription:
#     channel_info = youtube.fetch_rss_feed(channel_url)
#     image_link = channel_info.image_link

#     image_data = None
#     if image_link:
#         response = requests.get(image_link, timeout=5)
#         if response.status_code == 200:
#             image_data = base64.b64encode(response.content).decode("utf-8")

#     return Subscription[
#         title=channel_info.title,
#         url=channel_url,
#         rss_feed_url=channel_info.rss_link,
#         description=channel_info.description,
#         image=image_data if image_data is not None else None,
#         ]


@router.post("/subscription/v2")
async def create_subscription_v2(new_subscription: SubscriptionCreateV2, session: AsyncSession = Depends(get_session)):
    logger.info("Received subscription creation request")
    logger.info("URL: %s", new_subscription.url)

    logger.info("Filters:")
    for idx, filter_model in enumerate(new_subscription.filters, 1):
        logger.info("  Filter %d:", idx)
        logger.info("    Criteria: %s", filter_model.comparison_operator)
        logger.info("    Operand: %s", filter_model.filter_type)

    logger.info("Retention Policy:")
    logger.info("  Type: %s", new_subscription.retentionPolicy.type)

    match new_subscription.retentionPolicy.type:
        case RetentionType.DATE_SINCE:
            logger.info("  Duration: %s", new_subscription.retentionPolicy.dateBefore)
        case RetentionType.COUNT:
            logger.info("  Count: %s", new_subscription.retentionPolicy.videoCount)
        case RetentionType.DELTA:
            logger.info("  No retention policy")

    plex_desc: PlexLibraryDestination = PlexLibraryDestination(
        locationId=new_subscription.plexLibraryDestination.locationId,
        directoryId=new_subscription.plexLibraryDestination.directoryId,
    )
    logger.info(plex_desc)

    result = await session.execute(select(Plex).options(selectinload(Plex.directories)))
    plex_server = result.scalars().first()

    directories: list[Directory] = plex_server.directories

    directory_id = new_subscription.plexLibraryDestination.directoryId
    location_id = new_subscription.plexLibraryDestination.locationId

    directory: list[Directory] = [item for item in directories if item.key == directory_id]
    if len(directory) == 0:
        return {"message": "Invalid directory"}
    else:
        location: list[Location] = [v for v in directory[0].locations if v.id_ == location_id] or []
        if len(location) == 0:
            return {"message": "Invalid location"}

    logger.info("  Directory ID: %s", new_subscription.plexLibraryDestination.directoryId)
    logger.info("  Location ID: %s", new_subscription.plexLibraryDestination.locationId)

    # Simulate successful creation
    return {"message": "Subscription logged successfully", "id": 12345}
