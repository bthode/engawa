import logging
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from enum import StrEnum
from typing import Annotated

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from engawa.plex.parsing import parse_plex_data  # type: ignore (Field)
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# from sqlalchemy.future import select
from sqlalchemy.orm import Mapped, selectinload
from sqlmodel import Field, Relationship, SQLModel, select  # type: ignore

# YOUTUBE PARSING START

# import logging
# from collections.abc import Callable
# from dataclasses import dataclass

# import requests
# from bs4 import BeautifulSoup
# from bs4.element import Tag

logger = logging.getLogger(__name__)


TIMEOUT_IN_SECONDS = 5


@dataclass
class Thumbnail:
    url: str
    width: str
    height: str


@dataclass
class Video:
    title: str
    published: str
    video_id: str
    link: str
    author: str
    thumbnail: Thumbnail


class Youtube_RSS_Parser:

    @staticmethod
    def make_request(url: str, timeout: int) -> str:
        response = requests.get(url, timeout=timeout)
        return response.content.decode("utf-8")

    @staticmethod
    def fetch_rss_feed(channel_url: str, request_maker: Callable[[str, int], str] = make_request) -> dict[str, str]:
        response_content = request_maker(channel_url, TIMEOUT_IN_SECONDS)
        soup = BeautifulSoup(response_content, "html.parser")

        # Fetch HTML title
        title = soup.title.string if soup.title else None
        if title is None:
            raise ValueError("Title not found")

        description = soup.find("meta", attrs={"name": "description"})
        if description is None:
            raise ValueError("Description not found")
        assert isinstance(description, Tag), "Description is not a Tag object"
        if not description.get("content"):
            raise ValueError("Description content not found")
        description_content = str(description["content"])

        # Fetch RSS link
        rss_link = soup.select_one('link[type="application/rss+xml"][title="RSS"]')
        if rss_link is None or not rss_link.get("href"):
            raise ValueError("RSS link not found")
        rss_href = rss_link["href"]
        rss_href = rss_href[0] if isinstance(rss_href, list) else rss_href

        # Fetch image link
        image_link = soup.select_one('link[rel="image_src"]')
        if image_link is None or not image_link.get("href"):
            raise ValueError("Image link not found")
        image_href = image_link["href"]
        image_href = image_href[0] if isinstance(image_href, list) else image_href

        return {"title": title, "rss_link": rss_href, "image_link": image_href, "description": description_content}

    @staticmethod
    def fetch_videos_from_rss_feed(
        rss_url: str, request_maker: Callable[[str, int], str] = make_request
    ) -> list[Video]:
        response_content = request_maker(rss_url, TIMEOUT_IN_SECONDS)
        soup = BeautifulSoup(response_content, "xml")

        entries = soup.find_all("entry")
        videos: list[Video] = []
        for entry in entries:
            title = entry.find("title")
            published = entry.find("published")
            video_id = entry.find("yt:videoId")
            author = entry.find("author").find("name")
            link = entry.find("link").get("href")
            thumbnail_link: str = entry.find("media:thumbnail").get("url")
            thumbnail_width: str = entry.find("media:thumbnail").get("width")
            thumbnail_height: str = entry.find("media:thumbnail").get("height")

            if title and published and video_id and author:
                videos.append(
                    Video(
                        title=title.text,
                        published=published.text,
                        video_id=video_id.text,
                        link=link,
                        author=author.text,
                        thumbnail=Thumbnail(url=thumbnail_link, width=thumbnail_width, height=thumbnail_height),
                    )
                )

        return videos


# YOUTUBE PARSING END


# TODO: Ideally fix up the relationship so we stop getting this greelet error on lazy loading something
# https://stackoverflow.com/questions/74252768/missinggreenlet-greenlet-spawn-has-not-been-called
# https://github.com/tiangolo/sqlmodel/issues/250


# TODO:
# COmmented out sa_relationship_kwargs settings make delete work, but break getting back the directories in the post command


class ErrorState(StrEnum):
    UNAUTHORIZED = "unauthorized"
    TIMEOUT = "timeout"
    REFUSED = "refused"


class PlexBase(SQLModel):
    name: str = Field(index=True)


class Plex(PlexBase, table=True):
    id: int = Field(default=None, primary_key=True)
    directories: Mapped[list["Directory"]] = Relationship(
        back_populates="plex"
        # , sa_relationship_kwargs={"cascade": "delete"}
    )
    endpoint: str
    port: str
    token: str
    error_state: ErrorState | None = Field(default=None)


class PlexServerCreate(PlexBase):
    endpoint: str
    port: str
    token: str


class PlexServerPublic(PlexBase):
    id: int


class PlexServerUpdate(SQLModel):
    id: int | None = None
    name: str


class DirectoryBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    uuid: str


class Directory(DirectoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    plex: Mapped[Plex] = Relationship(back_populates="directories")
    plex_id: int = Field(default=None, foreign_key="plex.id")
    locations: Mapped[list["Location"]] = Relationship(
        back_populates="directory",
        sa_relationship_kwargs={"lazy": "selectin"},
        # sa_relationship_kwargs={"lazy": "selectin", "cascade": "delete"}
    )


class LocationBase(SQLModel):
    path: str


class LocationPublic(LocationBase):
    pass


class DirectoryPublic(DirectoryBase):
    locations: list[LocationPublic] = []


class DirectoryCreate(DirectoryBase):
    pass


class DirectoryPublicWithPlexServer(DirectoryPublic):
    plex: PlexServerPublic | None = None


class PlexPublicWithDirectories(PlexServerPublic):
    directories: list[DirectoryPublic] = []
    endpoint: str
    port: str
    error_state: ErrorState | None = None


class Location(LocationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    directory_id: int = Field(default=None, foreign_key="directory.id")
    directory: Mapped[Directory] = Relationship(back_populates="locations")


def build_path(host: str, port: str, token: str) -> str:
    token_prefix = "?X-Plex-Token="
    return f"http://{host}:{port}/library/sections{token_prefix}{token}"


async def insert_initial_data(session: AsyncSession):
    plex_test_data = Plex(
        name="Plex",
        endpoint="10.1.1.10",
        port="32400",
        token="Token1",
        directories=[
            Directory(
                title="Movies",
                uuid="0c717b05-2deb-419c-a2d0-e68cceddea04",
                locations=[
                    Location(path="/media/Media/Video/Movies"),
                ],
            ),
            Directory(
                title="Plexor",
                uuid="0c717b05-2deb-419c-a2d0-e68cceddea05",
                locations=[
                    Location(path="/index/YouTube/plexor"),
                ],
            ),
            Directory(
                title="Youtube",
                uuid="0c717b05-2deb-419c-a2d0-e68cceddea06",
                locations=[
                    Location(path="/index/YouTube"),
                    Location(path="/index/media"),
                ],
            ),
        ],
    )

    print("Inserting initial data")
    session.add(plex_test_data)
    await session.commit()


# Database setup
sqlite_file_name = "test.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"
engine = create_async_engine(sqlite_url, echo=True)
# SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Setup dependency for getting a session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session_local = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
    async with session_local() as session:
        yield session


# FastAPI lifespan management
@asynccontextmanager
async def get_connection(app: FastAPI):  # pylint: disable=unused-argument
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
        # await insert_initial_data(SessionLocal())
    yield
    await engine.dispose()


router = APIRouter()


@router.get("/plex_server", response_model=list[PlexPublicWithDirectories])
async def plex_server(session: Annotated[AsyncSession, Depends(get_session)]):
    items: list[Plex] = []
    result = await session.execute(select(Plex).options(selectinload(Plex.directories)))
    server = result.scalars().first()
    if server is not None:
        items.append(server)
    return items
    # if server is not None:
    #     items.append(server)
    # return items


@router.post("/fetch_rss")
async def fetch_rss_route(channel_url: str) -> dict[str, str]:  # Make custom url class
    return Youtube_RSS_Parser.fetch_rss_feed(channel_url)


@router.get("/get_videos")
async def get_videos_route(rss_url: str) -> list[Video]:  # Make custom rss url class
    return Youtube_RSS_Parser.fetch_videos_from_rss_feed(rss_url)


@router.post("/plex_server", response_model=list[PlexPublicWithDirectories])
async def create_plex_server(plex: PlexServerCreate, session: Annotated[AsyncSession, Depends(get_session)]):
    existing_plex_server = await session.execute(select(Plex).select())
    if existing_plex_server.scalars().first():
        raise HTTPException(status_code=400, detail="Plex server already exists")

    endpoint = build_path(plex.endpoint, plex.port, plex.token)
    plex_response: requests.models.Response = requests.get(endpoint, timeout=15)
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
                locations=[Location(path=location.path) for location in directory.location],
            )
            for directory in plex_data.directories
        ],
    )

    session.add(plex_server)
    await session.commit()
    await session.refresh(plex_server)

    # Eagerly load directories
    result = await session.execute(
        select(Plex).options(selectinload(Plex.directories)).where(Plex.id == plex_server.id)
    )
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


# FastAPI app setup
fastAPI = FastAPI(lifespan=get_connection)
fastAPI.include_router(router, prefix="/api")

fastAPI.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(fastAPI, host="0.0.0.0", port=8000)
