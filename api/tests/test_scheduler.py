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
    PlexLibraryDestination,
    RetentionPolicy,
    RetentionType,
    Subscription,
    SubscriptionCreateV2,
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
    uploaded: datetime = datetime.now(),
    duration: int = 3600,  # 1 hour
    title: str = "Default Title",
    description: str = "Default Description",
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


def create_subscription(
    id: int = 1,
    title: str = "Test Subscription",
    url: str = "http://example.com",
    rss_feed_url: str = "http://example.com/rss",
    description: str = "Test Description",
    image: str = "http://example.com/image.jpg",
    plex_library_path: str = "/some/path",
) -> Subscription:
    return Subscription(
        id=id,
        title=title,
        url=url,
        rss_feed_url=rss_feed_url,
        description=description,
        image=image,
        plex_library_path=plex_library_path,
    )


@pytest.fixture(scope="function")
async def async_session_factory() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    yield async_session_maker()
    await engine.dispose()


async def mock_get_session(session):  # type:ignore
    yield session


@pytest.mark.asyncio
async def test_obtained_metadata(
    async_session_factory: AsyncGenerator[AsyncSession, None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_success_metadata)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type:ignore

        subscription = create_subscription()

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
        # TODO: This is being set to obtained metadata, but it should be pending download
        assert updated_video.status == VideoStatus.OBTAINED_METADATA
        assert updated_video.duration == 300
        assert updated_video.thumbnail_url == "http://example.com/test_thumbnail.jpg"


@pytest.mark.asyncio
async def test_live_event_not_started(
    async_session_factory: AsyncGenerator[AsyncSession, None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_live_event_metadata)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type:ignore

        subscription = create_subscription()
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
    async_session_factory: AsyncGenerator[AsyncSession, None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_unavailable_metadata)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type: ignore

        subscription = create_subscription()
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
    async_session_factory: AsyncGenerator[AsyncSession, None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_success_video_data)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type: ignore

        subscription = create_subscription()
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
    async_session_factory: AsyncGenerator[AsyncSession, None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_unavailable_metadata)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type: ignore

        past_date: datetime = datetime.now(utc) - timedelta(minutes=SUBSCRIPTION_UPDATE_INTERVAL + 1)

        subscription = create_subscription()
        subscription.last_updated = past_date

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
    async_session_factory: AsyncGenerator[AsyncSession, None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_unavailable_metadata)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type: ignore
        new_subscription = create_subscription(id=1, url="http://example.com/new", title="New Subscription")

        recent_subscription = create_subscription(id=2, url="http://example.com/recent", title="Recent Subscription")
        recent_subscription.last_updated = datetime.now(utc)

        stale_subscription = create_subscription(id=3, url="http://example.com/stale", title="Old Subscription")
        stale_subscription.last_updated = datetime.now(utc) - timedelta(minutes=SUBSCRIPTION_UPDATE_INTERVAL + 1)

        session.add(new_subscription)
        session.add(recent_subscription)
        session.add(stale_subscription)
        await session.commit()

        subscriptions_to_update = await get_subscriptions_to_update(session)

        assert len(subscriptions_to_update) == 2
        assert any(sub.title == "New Subscription" for sub in subscriptions_to_update)
        assert any(sub.title == "Old Subscription" for sub in subscriptions_to_update)
        assert all(sub.title != "Recent Subscription" for sub in subscriptions_to_update)


@pytest.mark.asyncio
async def test_get_pending_videos(
    async_session_factory: AsyncGenerator[AsyncSession, None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session as session:
        monkeypatch.setattr("app.scheduler.get_metadata", mock_success_video_data)
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type: ignore

        subscription = create_subscription()
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
    async_session_factory: AsyncGenerator[AsyncSession, None],
    monkeypatch: pytest.MonkeyPatch,
):
    async_session = await anext(async_session_factory)
    async with async_session as session:
        video_duration: int = 1800
        monkeypatch.setattr("app.scheduler.get_session", lambda: mock_get_session(session))  # type: ignore

        subscription = create_subscription()
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


@pytest.mark.asyncio
async def test_new_subscription_v2(
    async_session_factory: AsyncGenerator[AsyncSession, None],
):
    async_session = await anext(async_session_factory)
    async with async_session as session:
        retention_policy = RetentionPolicy(
            type=RetentionType.COUNT,
            videoCount=1,
            dateBefore=datetime.now(),
            timeDeltaTypeValue=timedelta(days=1),
        )

        filters: list[Filter] = [
            Filter(filter_type=FilterType.DURATION, comparison_operator=ComparisonOperator.GT, threshold_seconds=1800)
        ]

        subscription_data = SubscriptionCreateV2(
            url="http://example.com",
            filters=filters,
            retention_policy=retention_policy,
            plex_library=PlexLibraryDestination(locationId=1, directoryId=1),
        )

        # Create a proper Subscription instance
        subscription = Subscription(
            title="Test Subscription",
            url=subscription_data.url,
            rss_feed_url="http://example.com/rss",
            description="Test Description",
            image="http://example.com/image.jpg",
            plex_library_path="/some/path",
            filters=filters,
            retention=retention_policy,
        )

        # Add the retention policy
        retention_policy.subscription_id = subscription.id
        session.add(subscription)
        session.add(retention_policy)

        # Add the filters to the subscription
        for filter_data in subscription_data.filters:
            filter_instance = Filter(
                subscription_id=subscription.id,
                filter_type=filter_data.filter_type,
                comparison_operator=filter_data.comparison_operator,
                threshold_seconds=filter_data.threshold_seconds,
            )
            session.add(filter_instance)

        await session.commit()

        asdf: PlexLibraryDestination = PlexLibraryDestination(locationId=1, directoryId=1)
        v2 = SubscriptionCreateV2(url="url", filters=filters, retention_policy=retention_policy, plex_library=asdf)

        print(v2)

        subscriptions_to_be_updated: list[Subscription] = await get_subscriptions_to_update(session)
        assert len(subscriptions_to_be_updated) == 1
        assert subscriptions_to_be_updated[0].id == 1
        assert subscriptions_to_be_updated[0].title == "Test Subscription"
        assert subscriptions_to_be_updated[0].url == "http://example.com"
        assert subscriptions_to_be_updated[0].rss_feed_url == "http://example.com/rss"
        assert subscriptions_to_be_updated[0].description == "Test Description"
        assert subscriptions_to_be_updated[0].image == "http://example.com/image.jpg"
