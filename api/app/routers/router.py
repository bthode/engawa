from fastapi import APIRouter

from . import plex, youtube

base_router = APIRouter()

base_router.include_router(plex.router, tags=["plex"])
base_router.include_router(youtube.router, tags=["youtube"])
