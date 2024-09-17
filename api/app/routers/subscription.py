import base64
from datetime import datetime
from typing import Annotated

import requests
from fastapi import APIRouter, Depends
from pytz import utc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database.session import get_session
from app.models.subscription import Subscription, SubscriptionCreate, Video, VideoStatus
from app.routers import youtube

router = APIRouter()


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
    return {"message": "subscription created"}


@router.delete("/subscription")
async def delete_all_subscriptions():
    return {"message": "subscriptions deleted"}


@router.get("/subscription/{subscription_id}", response_model=Subscription)
async def get_subscription(subscription_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    result = await session.execute(select(Subscription).where(Subscription.id == subscription_id))
    subscription = result.scalars().first()
    return subscription


@router.delete("/subscription/{subscription_id}")
async def delete_subscription(subscription_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    result = await session.execute(select(Subscription).where(Subscription.id == subscription_id))
    subscription = result.scalars().first()
    await session.delete(subscription)
    await session.commit()
    return {"message": "subscription deleted"}


@router.post("/subscription/{subscription_id}/sync", response_model=Subscription)
async def sync_subscription(subscription_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    subscription = await get_subscription(subscription_id, session)
    results: list[Video] = youtube.fetch_videos_from_rss_feed(subscription.rss_feed_url)
    for video in results:
        existing_video = await session.execute(select(Video).where(Video.video_id == video.video_id))
        #  TODO: Should we use a hash to check if the video data has changed?
        if not existing_video.scalars().first():
            new_video = Video(
                title=video.title,
                published=video.published,
                video_id=video.video_id,
                link=video.link,
                author=video.author,
                thumbnail_url=video.thumbnail_url,
                subscription_id=subscription.id,
                status=VideoStatus.PENDING,
            )
            session.add(new_video)

            session.add(subscription)
        subscription.last_updated = datetime.now(utc)

    await session.commit()
    return {"message": "subscription synced"}


@router.get("/subscription/{subscription_id}/videos", response_model=list[Video])
async def get_subscription_videos(subscription_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    result = await session.execute(select(Video).where(Video.subscription_id == subscription_id)
                                   .order_by(Video.published.desc()))
    return result.scalars().all()
