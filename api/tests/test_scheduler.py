from collections.abc import AsyncGenerator
from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel, select

from app.models.subscription import Subscription, Video, VideoStatus
from app.scheduler import async_sync_and_update_videos
from app.yt_downloader import (
    VideoMetadata,
)


async def mock_get_metadata() -> VideoMetadata:
    return VideoMetadata(
        id="test_video_id",
        title="Test Video Title",
        uploader="Test Uploader",
        upload_date=datetime.strptime("20230101", "%Y%m%d"),
        duration_in_seconds=300,
        description="This is a test video description",
        thumbnail_url="http://example.com/test_thumbnail.jpg",
    )


# def mock_obtain_metadata(url: str) -> dict[str, str | int]:
#     if "live" in url:
#         raise VideoMetadataError(VideoError.LIVE_EVENT_NOT_STARTED, "Live event not started")
#     elif "unavailable" in url:
#         raise VideoMetadataError(VideoError.VIDEO_UNAVAILABLE, "Video unavailable")
#     else:
#         return {
#             "id": "test_id",
#             "title": "Test Video",
#             "uploader": "Test Uploader",
#             "upload_date": "20230101",
#             "duration": 100,
#             "description": "Test description",
#             "thumbnail": "http://example.com/thumbnail.jpg",
#             "status": "available",
#         }


@pytest.fixture(scope="function")
async def async_session_factory() -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    yield async_session_maker

    await engine.dispose()


@pytest.mark.asyncio
async def test_obtained_metadata(
    async_session_factory: AsyncGenerator[async_sessionmaker[AsyncSession], None],
    monkeypatch: pytest.MonkeyPatch,
):
    session_maker = await anext(async_session_factory)
    async with session_maker() as session:
        monkeypatch.setattr("app.scheduler.obtain_metadata", mock_obtain_metadata)
        monkeypatch.setattr("app.scheduler.get_metadata", mock_get_metadata)
        monkeypatch.setattr("app.scheduler.get_session", lambda: session)

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

        await async_sync_and_update_videos(session)

        result = await session.execute(select(Video).where(Video.id == 1))
        updated_video = result.scalars().first()

        assert updated_video is not None
        assert updated_video.status == VideoStatus.OBTAINED_METADATA
        assert updated_video.duration == 100
        assert updated_video.thumbnail_url == "http://example.com/thumbnail.jpg"


@pytest.mark.asyncio
async def test_live_event_not_started(
    async_session_factory: AsyncGenerator[async_sessionmaker[AsyncSession], None], monkeypatch: pytest.MonkeyPatch
):
    session_maker = await anext(async_session_factory)
    async with session_maker() as session:
        # Setup
        monkeypatch.setattr("app.scheduler.obtain_metadata", mock_obtain_metadata)
        monkeypatch.setattr("app.scheduler.get_session", lambda: [session])

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

        await async_sync_and_update_videos(session)

        result = await session.execute(select(Video).where(Video.id == 1))
        updated_video = result.scalars().first()

        assert updated_video.status == VideoStatus.EXCLUDED


@pytest.mark.asyncio
async def test_video_unavailable(
    async_session_factory: AsyncGenerator[async_sessionmaker[AsyncSession], None], monkeypatch: pytest.MonkeyPatch
):
    session_maker = await anext(async_session_factory)
    async with session_maker() as session:
        # Setup
        monkeypatch.setattr("app.scheduler.obtain_metadata", mock_obtain_metadata)
        monkeypatch.setattr("app.scheduler.get_session", lambda: [session])

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

        # Run the function
        await async_sync_and_update_videos(session)

        result = await session.execute(select(Video).where(Video.id == 1))
        updated_video = result.scalars().first()

        assert updated_video is not None
        assert updated_video.status == VideoStatus.EXCLUDED
