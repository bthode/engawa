import base64
from typing import Annotated

import requests
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database.session import get_session
from app.models.subscription import Subscription, SubscriptionCreate
from app.models.youtube import Youtube

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

    channel_info = Youtube.fetch_rss_feed(create.url)
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
async def delete_subscription(subscription_id: int):
    return {"message": f"subscription {subscription_id} deleted"}
