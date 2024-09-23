from collections.abc import AsyncGenerator
from datetime import datetime, timedelta

import pytest
from pytz import utc
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel, select

from app.models.subscription import (
    ComparisonOperator,
    Filter,
    FilterType,
    Subscription,
    Video,
    VideoStatus,
)
from app.scheduler import (
    SUBSCRIPTION_UPDATE_INTERVAL,
    get_pending_videos,
    get_subscriptions_to_update,
    sync_and_update_videos,
)
from app.yt_downloader import (
    MetadataError,
    MetadataErrorType,
    MetadataResult,
    MetadataSuccess,
    VideoMetadata,
)


async def mock_success_video_data(
    uploaded: datetime = datetime.now(),  # Default to current datetime
    duration: int = 3600,  # Default to 1 hour
    title: str = "Default Title",  # Default title
    description: str = "Default Description",  # Default description
) -> list[MetadataSuccess]:
    return [
        MetadataSuccess(
            url="http//example.com/video",
            metadata=VideoMetadata(
                id="test_video_id",
                title=title,
                uploader="Test Uploader",
                upload_date=uploaded,
                duration_in_seconds=duration,
                description=description,
                thumbnail_url="http://example.com/test_thumbnail.jpg",
            ),
        )
    ]


async def mock_success_metadata(urls: list[str]):
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


async def mock_live_event_metadata(urls: list[str]):
    return [
        MetadataError(
            url=urls[0],
            error_type=MetadataErrorType.LIVE_EVENT_NOT_STARTED,
            message="This live event will begin in a few moments",
        )
    ]


async def mock_unavailable_metadata(urls: list[str]) -> list[MetadataResult]:
    return [
        MetadataError(url=urls[0], error_type=MetadataErrorType.VIDEO_UNAVAILABLE, message="This video is unavailable")
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
        monkeypatch.setattr("app.scheduler.get_metadata", mock_success_metadata)
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
            subscription_id=subscription.id,
            status=VideoStatus.PENDING,
            link="http://example.com/video",
            author="Test Author",
            description="Sample description",
            published=datetime(2023, 1, 1),
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


@pytest.mark.asyncio
async def test_live_event_not_started(
    async_session_factory: AsyncGenerator[async_sessionmaker[AsyncSession], None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session() as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_live_event_metadata)
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
            subscription_id=subscription.id,
            status=VideoStatus.PENDING,
            link="http://example.com/live",
            author="Test Author",
            description="Test description",
            published=datetime(2023, 1, 1),
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
        monkeypatch.setattr("app.scheduler.get_metadata", mock_unavailable_metadata)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type: ignore

        subscription = Subscription(
            title="Test Subscription",
            url="http://example.com",
            rss_feed_url="http://example.com/rss",
            description="Test Description",
            image="http://example.com/image.jpg",
        )
        session.add(subscription)
        await session.commit()

        video = Video(
            subscription_id=subscription.id,
            status=VideoStatus.PENDING,
            link="http://example.com/unavailable",
            author="Test Author",
            description="Test description",
            published=datetime(2023, 1, 1),
            thumbnail_url="http://example.com/thumbnail.jpg",
            title="Test Video",
            video_id="test_video_id",
        )
        session.add(video)
        await session.commit()

        await sync_and_update_videos()

        result = await session.execute(select(Video).where(Video.id == 1))
        updated_video = result.scalars().first()

        assert updated_video is not None
        assert updated_video.status == VideoStatus.EXCLUDED


@pytest.mark.asyncio
async def test_new_subscription_is_picked_up(
    async_session_factory: AsyncGenerator[async_sessionmaker[AsyncSession], None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session() as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_success_video_data)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type: ignore

        subscription = Subscription(
            id=1,
            title="Test Subscription",
            url="http://example.com",
            rss_feed_url="http://example.com/rss",
            description="Test Description",
            image="http://example.com/image.jpg",
        )
        session.add(subscription)
        await session.commit()

        subscriptions_to_be_updated: list[Subscription] = await get_subscriptions_to_update(session)
        assert len(subscriptions_to_be_updated) == 1
        assert subscriptions_to_be_updated[0].id == 1
        assert subscriptions_to_be_updated[0].title == "Test Subscription"
        assert subscriptions_to_be_updated[0].url == "http://example.com"
        assert subscriptions_to_be_updated[0].rss_feed_url == "http://example.com/rss"
        assert subscriptions_to_be_updated[0].description == "Test Description"
        assert subscriptions_to_be_updated[0].image == "http://example.com/image.jpg"


@pytest.mark.asyncio
async def test_existing_subscription_is_picked_up(
    async_session_factory: AsyncGenerator[async_sessionmaker[AsyncSession], None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session() as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_unavailable_metadata)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type: ignore

        past_date: datetime = datetime.now(utc) - timedelta(minutes=SUBSCRIPTION_UPDATE_INTERVAL + 1)

        subscription = Subscription(
            id=1,
            title="Test Subscription",
            url="http://example.com",
            rss_feed_url="http://example.com/rss",
            description="Test Description",
            image="http://example.com/image.jpg",
            last_updated=past_date,
        )
        session.add(subscription)
        await session.commit()

        subscriptions_to_be_updated: list[Subscription] = await get_subscriptions_to_update(session)
        assert len(subscriptions_to_be_updated) == 1
        assert subscriptions_to_be_updated[0].id == 1
        assert subscriptions_to_be_updated[0].title == "Test Subscription"
        assert subscriptions_to_be_updated[0].url == "http://example.com"
        assert subscriptions_to_be_updated[0].rss_feed_url == "http://example.com/rss"
        assert subscriptions_to_be_updated[0].description == "Test Description"
        assert subscriptions_to_be_updated[0].image == "http://example.com/image.jpg"


@pytest.mark.asyncio
async def test_get_subscriptions_to_update(
    async_session_factory: AsyncGenerator[async_sessionmaker[AsyncSession], None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session() as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_unavailable_metadata)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type: ignore
        new_subscription = Subscription(
            title="New Subscription",
            url="http://example.com/new",
            rss_feed_url="http://example.com/new/rss",
            description="Test Description",
            image="http://example.com/image.jpg",
        )

        recent_subscription = Subscription(
            title="Recent Subscription",
            url="http://example.com/recent",
            rss_feed_url="http://example.com/recent/rss",
            description="Test Description",
            image="http://example.com/image.jpg",
            last_updated=datetime.now(utc),
        )

        old_subscription = Subscription(
            title="Old Subscription",
            url="http://example.com/old",
            rss_feed_url="http://example.com/old/rss",
            description="Test Description",
            image="http://example.com/image.jpg",
            last_updated=datetime.now(utc) - timedelta(minutes=SUBSCRIPTION_UPDATE_INTERVAL + 1),
        )

        session.add(new_subscription)
        session.add(recent_subscription)
        session.add(old_subscription)
        await session.commit()

        subscriptions_to_update = await get_subscriptions_to_update(session)

        assert len(subscriptions_to_update) == 2
        assert any(sub.title == "New Subscription" for sub in subscriptions_to_update)
        assert any(sub.title == "Old Subscription" for sub in subscriptions_to_update)
        assert all(sub.title != "Recent Subscription" for sub in subscriptions_to_update)


@pytest.mark.asyncio
async def test_get_pending_videos(
    async_session_factory: AsyncGenerator[async_sessionmaker[AsyncSession], None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session() as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_success_video_data)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type: ignore

        subscription = Subscription(
            title="New Subscription",
            url="http://example.com/new",
            rss_feed_url="http://example.com/new/rss",
            description="Test Description",
            image="http://example.com/image.jpg",
        )
        session.add(subscription)
        await session.commit()

        new_filter = Filter(
            subscription_id=subscription.id,
            filter_type=FilterType.DURATION,
            comparison_operator=ComparisonOperator.GT,
            threshold_seconds=1800,
        )
        session.add(new_filter)
        await session.commit()

        video = Video(
            subscription_id=subscription.id,
            status=VideoStatus.PENDING,
            link="http://example.com/unavailable",
            author="Test Author",
            description="Test description",
            published=datetime(2023, 1, 1),
            thumbnail_url="http://example.com/thumbnail.jpg",
            title="Test Video",
            video_id="test_video_id",
        )

        session.add(video)
        await session.commit()

        videos_to_update = await get_pending_videos(session)
        assert isinstance(videos_to_update, list)
        assert isinstance(videos_to_update[0], Video)
        assert (
            len(
                videos_to_update,
            )
            == 1
        )


@pytest.mark.asyncio
async def test_video_filters(
    async_session_factory: AsyncGenerator[async_sessionmaker[AsyncSession], None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session() as session:
        video_duration: int = 1800
        monkeypatch.setattr("app.scheduler.get_metadata", mock_success_video_data(duration=video_duration - 100))
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type: ignore

        subscription = Subscription(
            title="New Subscription",
            url="http://example.com/new",
            rss_feed_url="http://example.com/new/rss",
            description="Test Description",
            image="http://example.com/image.jpg",
        )
        session.add(subscription)
        await session.commit()

        new_filter = Filter(
            subscription_id=subscription.id,
            filter_type=FilterType.DURATION,
            comparison_operator=ComparisonOperator.GT,
            threshold_seconds=video_duration,
        )
        session.add(new_filter)
        await session.commit()

        video = Video(
            subscription_id=subscription.id,
            status=VideoStatus.PENDING,
            link="http://example.com/unavailable",
            author="Test Author",
            description="Test description",
            published=datetime(2023, 1, 1),
            thumbnail_url="http://example.com/thumbnail.jpg",
            title="Test Video",
            video_id="test_video_id",
            duration=video_duration,
        )

        session.add(video)
        await session.commit()

        videos_to_update = await get_pending_videos(session)
        assert isinstance(videos_to_update, list)
        assert isinstance(videos_to_update[0], Video)
        assert (
            len(
                videos_to_update,
            )
            == 1
        )
