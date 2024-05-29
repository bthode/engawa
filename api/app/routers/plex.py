from typing import Annotated

import requests
from engawa.plex.parsing import parse_plex_data
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select  # type: ignore

from database.session import get_session
from models.plex import (
    Directory,
    Location,
    Plex,
    PlexPublicWithDirectories,
    PlexServerCreate,
)
from utils import build_path

router = APIRouter()


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
    plex_response: requests.models.Response = requests.get(endpoint, timeout=15)
    plex_data = parse_plex_data(plex_response.text)

    create = Plex(
        name=plex.name,
        endpoint=plex.endpoint,
        port=plex.port,
        token=plex.token,
        directories=[
            Directory(
                title=directory.title,
                uuid=directory.uuid,
                locations=[Location(path=location.path) for location in directory.location],
            )
            for directory in plex_data.directories
        ],
    )

    session.add(create)
    await session.commit()
    await session.refresh(create)

    # Eagerly load directories
    result = await session.execute(select(Plex).options(selectinload(Plex.directories)).where(Plex.id == create.id))
    return [result.scalars().one()]


# BUG: sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: directory.plex_id
@router.delete("/plex_server/{plex_id}")
async def delete_plex_server(plex_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    result = await session.execute(select(Plex).where(Plex.id == plex_id))
    plex = result.scalars().first()
    if not plex:
        raise HTTPException(status_code=404, detail="Plex not found")
    await session.delete(plex)
    await session.commit()
    return plex
