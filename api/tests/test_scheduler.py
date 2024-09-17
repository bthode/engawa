from collections.abc import AsyncGenerator
from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel, select

from app.models.subscription import Subscription, Video, VideoStatus
from app.scheduler import sync_and_update_videos
from app.yt_downloader import (
    MetadataError,
    MetadataErrorType,
    MetadataResult,
    MetadataSuccess,
    VideoMetadata,
)


async def mock_get_metadata(urls: list[str]):
    return [
        MetadataSuccess(
            url=urls[0],
            metadata=VideoMetadata(
                id="test_video_id",
                title="Test Video Title",
                uploader="Test Uploader",
                upload_date=datetime(2023, 1, 1),
                duration_in_seconds=300,
                description="This is a test video description",
                thumbnail_url="http://example.com/test_thumbnail.jpg",
            ),
        )
    ]


@pytest.fixture(scope="function")
async def async_session_factory() -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    yield async_session_maker

    await engine.dispose()


async def mock_get_session(session):  # type:ignore
    yield session


@pytest.mark.asyncio
async def test_obtained_metadata(
    async_session_factory: AsyncGenerator[async_sessionmaker[AsyncSession], None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session() as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_get_metadata)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type:ignore

        subscription = Subscription(
            id=1,
            title="Test Subscription",
            url="http://example.com",
            rss_feed_url="http://example.com/rss",
            description="Test Description",
            image="http://example.com/image.jpg",
        )
        video = Video(
            id=1,
            subscription_id=1,
            status=VideoStatus.PENDING,
            link="http://example.com/video",
            author="Test Author",
            published="2023-01-01",
            thumbnail_url="http://example.com/thumbnail.jpg",
            title="Test Video",
            video_id="test_video_id",
        )
        session.add(subscription)
        session.add(video)
        await session.commit()

        await sync_and_update_videos()

        result = await session.execute(select(Video).where(Video.id == 1))
        updated_video = result.scalars().first()

        assert updated_video is not None
        assert updated_video.status == VideoStatus.OBTAINED_METADATA
        assert updated_video.duration == 300
        assert updated_video.thumbnail_url == "http://example.com/test_thumbnail.jpg"


async def mock_get_metadata_live_event(urls: list[str]):
    return [
        MetadataError(
            url=urls[0],
            error_type=MetadataErrorType.LIVE_EVENT_NOT_STARTED,
            message="This live event will begin in a few moments",
        )
    ]


async def mock_get_metadata_unavailable(urls: list[str]) -> list[MetadataResult]:
    return [
        MetadataError(url=urls[0], error_type=MetadataErrorType.VIDEO_UNAVAILABLE, message="This video is unavailable")
    ]


@pytest.mark.asyncio
async def test_live_event_not_started(
    async_session_factory: AsyncGenerator[async_sessionmaker[AsyncSession], None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session() as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_get_metadata_live_event)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type:ignore

        subscription = Subscription(
            id=1,
            title="Test Subscription",
            url="http://example.com",
            rss_feed_url="http://example.com/rss",
            description="Test Description",
            image="http://example.com/image.jpg",
        )
        video = Video(
            id=1,
            subscription_id=1,
            status=VideoStatus.PENDING,
            link="http://example.com/live",
            author="Test Author",
            published="2023-01-01",
            thumbnail_url="http://example.com/thumbnail.jpg",
            title="Test Video",
            video_id="test_video_id",
        )
        session.add(subscription)
        session.add(video)
        await session.commit()

        await sync_and_update_videos()

        result = await session.execute(select(Video).where(Video.id == 1))
        updated_video = result.scalars().first()

        assert updated_video is not None
        assert updated_video.status == VideoStatus.EXCLUDED
        assert updated_video.retry_count == 0


@pytest.mark.asyncio
async def test_video_unavailable(
    async_session_factory: AsyncGenerator[async_sessionmaker[AsyncSession], None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session() as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_get_metadata_unavailable)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))

        subscription = Subscription(
            id=1,
            title="Test Subscription",
            url="http://example.com",
            rss_feed_url="http://example.com/rss",
            description="Test Description",
            image="http://example.com/image.jpg",
        )
        video = Video(
            id=1,
            subscription_id=1,
            status=VideoStatus.PENDING,
            link="http://example.com/unavailable",
            author="Test Author",
            published="2023-01-01",
            thumbnail_url="http://example.com/thumbnail.jpg",
            title="Test Video",
            video_id="test_video_id",
        )
        session.add(subscription)
        session.add(video)
        await session.commit()

        await sync_and_update_videos()

        result = await session.execute(select(Video).where(Video.id == 1))
        updated_video = result.scalars().first()

        assert updated_video is not None
        assert updated_video.status == VideoStatus.EXCLUDED
