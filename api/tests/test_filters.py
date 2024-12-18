from datetime import datetime

import pytest

from app.filters import (
    apply_filters,
)
from app.models.subscription import (
    ComparisonOperator,
    Filter,
    FilterType,
    Video,
    VideoStatus,
)


def create_duration_filter(operator: str, threshold: int) -> Filter:
    return Filter(
        filter_type=FilterType.DURATION,
        comparison_operator=ComparisonOperator(operator),
        threshold_seconds=threshold,
    )


def create_title_contains_filter(keyword: str) -> Filter:
    return Filter(filter_type=FilterType.TITLE_CONTAINS, keyword=keyword)


def create_description_contains_filter(keyword: str) -> Filter:
    return Filter(filter_type=FilterType.DESCRIPTION_CONTAINS, keyword=keyword)


def create_published_after_filter(operator: str, date: datetime) -> Filter:
    return Filter(
        filter_type=FilterType.PUBLISHED_AFTER,
        comparison_operator=ComparisonOperator(operator),
        threshold_date=date,
    )


@pytest.fixture
def sample_videos() -> list[Video]:
    return [
        Video(
            id=1,
            subscription_id=1,
            status=VideoStatus.OBTAINED_METADATA,
            link="http://example.com/video1",
            author="Author 1",
            title="Learn Python Programming",
            description="This is a test video about Python",
            published=datetime(2023, 1, 1),
            thumbnail_url="http://example.com/thumbnail1.jpg",
            video_id="video1",
            duration=3600,  # 1 hour
        ),
        Video(
            id=2,
            subscription_id=1,
            status=VideoStatus.OBTAINED_METADATA,
            link="http://example.com/video2",
            author="Author 2",
            title="TypeScript in 10 minutes",
            description="A short video about TypeScript",
            published=datetime(2023, 2, 15),
            thumbnail_url="http://example.com/thumbnail2.jpg",
            video_id="video2",
            duration=600,  # 10 minutes
        ),
        Video(
            id=3,
            subscription_id=2,
            status=VideoStatus.OBTAINED_METADATA,
            link="http://example.com/video3",
            author="Author 3",
            title="Machine Learning Basics",
            description="An introduction to machine learning",
            published=datetime(2023, 3, 30),
            thumbnail_url="http://example.com/thumbnail3.jpg",
            video_id="video3",
            duration=1800,  # 30 minutes
        ),
    ]


def test_duration_filter(sample_videos: list[Video]) -> None:
    duration_filter = create_duration_filter(ComparisonOperator.LT, 1801)
    filtered = apply_filters(sample_videos, [duration_filter])
    assert len([v for v in filtered if v.status == VideoStatus.PENDING_DOWNLOAD]) == 1
    assert [v for v in filtered if v.status == VideoStatus.PENDING_DOWNLOAD][0].title == "Learn Python Programming"
    assert len([v for v in filtered if v.status == VideoStatus.FILTERED]) == 2


def test_title_contains_filter(sample_videos: list[Video]) -> None:
    title_filter = create_title_contains_filter("Python")
    filtered = apply_filters(sample_videos, [title_filter])
    assert len([v for v in filtered if v.status == VideoStatus.PENDING_DOWNLOAD]) == 1
    assert [v for v in filtered if v.status == VideoStatus.PENDING_DOWNLOAD][0].title == "Learn Python Programming"
    assert len([v for v in filtered if v.status == VideoStatus.FILTERED]) == 2


def test_description_contains_filter(sample_videos: list[Video]) -> None:
    desc_filter = create_description_contains_filter("machine learning")
    filtered = apply_filters(sample_videos, [desc_filter])
    assert len([v for v in filtered if v.status == VideoStatus.PENDING_DOWNLOAD]) == 1
    assert [v for v in filtered if v.status == VideoStatus.PENDING_DOWNLOAD][0].title == "Machine Learning Basics"
    assert len([v for v in filtered if v.status == VideoStatus.FILTERED]) == 2


def test_published_after_filter(sample_videos: list[Video]) -> None:
    date_filter = create_published_after_filter(ComparisonOperator.GT, datetime(2023, 2, 1))
    filtered = apply_filters(sample_videos, [date_filter])
    assert len([v for v in filtered if v.status == VideoStatus.PENDING_DOWNLOAD]) == 2
    assert [v.title for v in filtered if v.status == VideoStatus.PENDING_DOWNLOAD] == [
        "TypeScript in 10 minutes",
        "Machine Learning Basics",
    ]
    assert len([v for v in filtered if v.status == VideoStatus.FILTERED]) == 1


def test_multiple_filters(sample_videos: list[Video]) -> None:
    duration_filter = create_duration_filter(ComparisonOperator.GT, 1800)
    title_filter = create_title_contains_filter("TypeScript")
    filtered = apply_filters(sample_videos, [duration_filter, title_filter])
    assert len([v for v in filtered if v.status == VideoStatus.PENDING_DOWNLOAD]) == 1
    assert [v for v in filtered if v.status == VideoStatus.PENDING_DOWNLOAD][0].title == "TypeScript in 10 minutes"
    assert len([v for v in filtered if v.status == VideoStatus.FILTERED]) == 2


def test_no_matching_filters(sample_videos: list[Video]) -> None:
    non_existent_filter = create_title_contains_filter("Rust")
    filtered = apply_filters(sample_videos, [non_existent_filter])
    assert len([v for v in filtered if v.status == VideoStatus.PENDING_DOWNLOAD]) == 0
    assert len([v for v in filtered if v.status == VideoStatus.FILTERED]) == 3


def test_all_matching_filters(sample_videos: list[Video]) -> None:
    all_match_filter = create_duration_filter(ComparisonOperator.LT, 0)
    filtered = apply_filters(sample_videos, [all_match_filter])
    assert len([v for v in filtered if v.status == VideoStatus.PENDING_DOWNLOAD]) == len(sample_videos)
    assert len([v for v in filtered if v.status == VideoStatus.FILTERED]) == 0
