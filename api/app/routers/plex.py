from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException

# from plex_api_client import PlexAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.database.session import get_session
from app.models.plex import (
    Directory,
    Location,
    Plex,
    PlexPublicWithDirectories,
    PlexServerCreate,
)
from app.plex_parsing import parse_plex_data

router = APIRouter()

# TODO: Use key for both directory and location id values to avoid conflict with python's built-in id function


@staticmethod
def build_path(host: str, port: str, token: str) -> str:
    token_prefix = "?X-Plex-Token="
    return f"http://{host}:{port}/library/sections{token_prefix}{token}"


@router.get("/plex_server", response_model=list[PlexPublicWithDirectories])
async def plex_server(session: Annotated[AsyncSession, Depends(get_session)]):
    items: list[Plex] = []
    result = await session.execute(select(Plex).options(selectinload(Plex.directories)))
    server = result.scalars().first()
    if server is not None:
        items.append(server)
    return items


@router.post("/plex_server", response_model=list[PlexPublicWithDirectories])
async def create_plex_server(plex: PlexServerCreate, session: Annotated[AsyncSession, Depends(get_session)]):
    existing_plex_server = await session.execute(select(Plex).select())
    if existing_plex_server.scalars().first():
        raise HTTPException(status_code=400, detail="Plex server already exists")

    endpoint = build_path(plex.endpoint, plex.port, plex.token)
    plex_response = httpx.get(endpoint, timeout=15)
    plex_data = parse_plex_data(plex_response.text)

    plex_server = Plex(
        name=plex.name,
        endpoint=plex.endpoint,
        port=plex.port,
        token=plex.token,
        directories=[
            Directory(
                title=directory.title,
                uuid=directory.uuid,
                key=directory.key,
                locations=[
                    (await session.execute(select(Location).where(Location.path == location.path))).scalars().first()
                    or Location(path=location.path, id_=location.id_)
                    for location in directory.location
                ],
            )
            for directory in plex_data.directories
        ],
    )

    session.add(plex_server)
    await session.commit()
    await session.refresh(plex_server)

    result = await session.execute(
        select(Plex).options(selectinload(Plex.directories)).where(Plex.id == plex_server.id)
    )
    return [result.scalars().one()]


@router.delete("/plex_server/{plex_id}")
async def delete_plex_server(plex_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    result = await session.execute(select(Plex).where(Plex.id == plex_id))
    plex = result.scalars().first()
    if not plex:
        raise HTTPException(status_code=404, detail="Plex Server Not Found")
    await session.delete(plex)
    await session.commit()
    return plex
