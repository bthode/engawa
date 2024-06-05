from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database.session import get_session
from app.models.subscription import Subscription

router = APIRouter()


@router.get("/subscription", response_model=list[Subscription])
async def get_all_subscription(session: Annotated[AsyncSession, Depends(get_session)]):
    return await session.execute(select(Subscription))


@router.post("/subscription")
async def create_subscription():
    return {"message": "subscription created"}


@router.delete("/subscription")
async def delete_all_subscriptions():
    return {"message": "subscriptions deleted"}


@router.get("/subscription/{subscription_id}")
async def get_subscription(subscription_id: int):
    return {"message": f" get {subscription_id} subscription"}


@router.patch("/subscription/{subscription_id}")
async def update_subscription(subscription_id: int):
    return {"message": f"subscription {subscription_id} updated"}


@router.delete("/subscription/{subscription_id}")
async def delete_subscription(subscription_id: int):
    return {"message": f"subscription {subscription_id} deleted"}
