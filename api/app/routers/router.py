from fastapi import APIRouter

from . import plex, settings, subscription, youtube

base_router = APIRouter()

base_router.include_router(plex.router, tags=["plex"])
base_router.include_router(youtube.router, tags=["youtube"])
base_router.include_router(subscription.router, tags=["subscription"])
base_router.include_router(settings.router, tags=["settings"])
