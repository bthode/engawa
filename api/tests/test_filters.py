from datetime import datetime, timedelta

import pytest

from app.filters import (
    apply_filters,
    create_description_contains_filter,
    create_duration_filter,
    create_published_after_filter,
    create_title_contains_filter,
)
from app.models.subscription import Filter, Video, VideoStatus


@pytest.fixture
def sample_videos() -> list[Video]:
    return [
        Video(
            id=1,
            subscription_id=1,
            status=VideoStatus.PENDING,
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
            status=VideoStatus.COMPLETE,
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
            status=VideoStatus.PENDING,
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
    duration_filter = create_duration_filter("Long videos", "gt", 1800)
    filtered = apply_filters(sample_videos, [duration_filter])
    assert len(filtered) == 1
    assert filtered[0].title == "Learn Python Programming"


def test_title_contains_filter(sample_videos: list[Video]) -> None:
    title_filter = create_title_contains_filter("Python videos", "Python")
    filtered = apply_filters(sample_videos, [title_filter])
    assert len(filtered) == 1
    assert filtered[0].title == "Learn Python Programming"


def test_description_contains_filter(sample_videos: list[Video]) -> None:
    desc_filter = create_description_contains_filter("ML videos", "machine learning")
    filtered = apply_filters(sample_videos, [desc_filter])
    assert len(filtered) == 1
    assert filtered[0].title == "Machine Learning Basics"


def test_published_after_filter(sample_videos: list[Video]) -> None:
    date_filter = create_published_after_filter("Recent videos", "gt", datetime(2023, 2, 1))
    filtered = apply_filters(sample_videos, [date_filter])
    assert len(filtered) == 2
    assert [v.title for v in filtered] == ["TypeScript in 10 minutes", "Machine Learning Basics"]


def test_multiple_filters(sample_videos: list[Video]) -> None:
    duration_filter = create_duration_filter("Short videos", "lt", 1800)
    title_filter = create_title_contains_filter("TypeScript videos", "TypeScript")
    filtered = apply_filters(sample_videos, [duration_filter, title_filter])
    assert len(filtered) == 1
    assert filtered[0].title == "TypeScript in 10 minutes"


def test_no_matching_filters(sample_videos: list[Video]) -> None:
    non_existent_filter = create_title_contains_filter("Non-existent", "Rust")
    filtered = apply_filters(sample_videos, [non_existent_filter])
    assert len(filtered) == 0


def test_all_matching_filters(sample_videos: list[Video]) -> None:
    all_match_filter = create_duration_filter("All videos", "gt", 0)
    filtered = apply_filters(sample_videos, [all_match_filter])
    assert len(filtered) == len(sample_videos)
