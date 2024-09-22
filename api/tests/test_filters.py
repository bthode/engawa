from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any

import pytest

from app.filters import (
    apply_filters,
    description_contains_filter,
    duration_filter,
    published_after_filter,
    title_contains_filter,
)
from app.models.subscription import Video, VideoStatus


@pytest.fixture
def sample_videos() -> list[Video]:
    return [
        Video(
            id=1,
            subscription_id=1,
            status=VideoStatus.PENDING,
            link="http://example.com/video1",
            author="Author 1",
            description="This is a test video about Python",
            published=datetime(2023, 1, 1),
            thumbnail_url="http://example.com/thumbnail1.jpg",
            title="Learn Python Programming",
            video_id="video1",
            duration=3600,  # 1 hour
        ),
        Video(
            id=2,
            subscription_id=1,
            status=VideoStatus.COMPLETE,
            link="http://example.com/video2",
            author="Author 2",
            description="A short video about TypeScript",
            published=datetime(2023, 2, 15),
            thumbnail_url="http://example.com/thumbnail2.jpg",
            title="TypeScript in 10 minutes",
            video_id="video2",
            duration=600,  # 10 minutes
        ),
        Video(
            id=3,
            subscription_id=2,
            status=VideoStatus.PENDING,
            link="http://example.com/video3",
            author="Author 3",
            description="An introduction to machine learning",
            published=datetime(2023, 3, 30),
            thumbnail_url="http://example.com/thumbnail3.jpg",
            title="Machine Learning Basics",
            video_id="video3",
            duration=1800,  # 30 minutes
        ),
    ]


@pytest.mark.parametrize(
    "duration,comparison,threshold,expected",
    [
        ("01:00:00", "lt", timedelta(hours=2), True),
        ("01:00:00", "le", timedelta(hours=1), True),
        ("01:00:00", "eq", timedelta(hours=1), True),
        ("01:00:00", "ne", timedelta(hours=2), True),
        ("01:00:00", "ge", timedelta(minutes=30), True),
        ("01:00:00", "gt", timedelta(minutes=30), True),
        ("01:00:00", "lt", timedelta(minutes=30), False),
        ("01:00:00", "invalid", timedelta(hours=1), pytest.raises(ValueError)),
    ],
)
def test_duration_filter(
    duration: str, comparison: str, threshold: timedelta, expected: bool | pytest.ExceptionInfo[BaseException]
) -> None:
    if isinstance(expected, bool):
        assert duration_filter(duration, comparison, threshold) == expected
    else:
        with expected:  # type:ignore
            duration_filter(duration, comparison, threshold)


@pytest.mark.parametrize(
    "keyword,expected_count",
    [
        ("Python", 1),
        ("TypeScript", 1),
        ("Machine Learning", 1),
        ("Java", 0),
        ("Py%th@n", 0),
    ],
)
def test_title_contains_filter(sample_videos: list[Video], keyword: str, expected_count: int) -> None:
    filtered: list[Video] = list(filter(title_contains_filter(keyword), sample_videos))
    assert len(filtered) == expected_count


@pytest.mark.parametrize(
    "keyword,expected_count",
    [
        ("test video", 1),
        ("TypeScript", 1),
        ("machine learning", 1),
        ("Java", 0),
    ],
)
def test_description_contains_filter(sample_videos: list[Video], keyword: str, expected_count: int) -> None:
    filtered: list[Video] = list(filter(description_contains_filter(keyword), sample_videos))
    assert len(filtered) == expected_count


@pytest.mark.parametrize(
    "date,expected_count",
    [
        (datetime(2023, 1, 1), 2),
        (datetime(2023, 2, 15), 1),
        (datetime(2023, 3, 30), 0),
        (datetime(2022, 12, 31), 3),
        (datetime(2023, 12, 31), 0),
    ],
)
def test_published_after_filter(sample_videos: list[Video], date: datetime, expected_count: int) -> None:
    filtered: list[Video] = list(filter(published_after_filter(date), sample_videos))
    assert len(filtered) == expected_count


def test_apply_filters(sample_videos: list[Video]) -> None:
    filters: list[Callable[[Video], bool]] = [
        title_contains_filter("Python"),
        description_contains_filter("test"),
        published_after_filter(datetime(2022, 12, 31)),
        lambda v: duration_filter(
            f"{v.duration // 3600:02d}:{(v.duration % 3600) // 60:02d}:{v.duration % 60:02d}",
            "gt",
            timedelta(minutes=30),
        ),
    ]
    filtered_videos: list[Video] = list(apply_filters(sample_videos, filters))
    assert len(filtered_videos) == 1
    assert filtered_videos[0].title == "Learn Python Programming"


def test_apply_filters_no_match(sample_videos: list[Video]) -> None:
    filters: list[Callable[[Video], bool]] = [
        title_contains_filter("Java"),
        description_contains_filter("nonexistent"),
    ]
    filtered_videos: list[Video] = list(apply_filters(sample_videos, filters))
    assert len(filtered_videos) == 0


def test_apply_filters_all_match(sample_videos: list[Video]) -> None:
    filters: list[Callable[[Video], bool]] = [
        lambda v: True,
    ]
    filtered_videos: list[Video] = list(apply_filters(sample_videos, filters))
    assert len(filtered_videos) == len(sample_videos)


def test_apply_filters_with_invalid_filter(sample_videos: list[Video]) -> None:
    filters: list[Any] = [
        title_contains_filter("Python"),
        "not_a_callable_filter",
    ]

    with pytest.raises(TypeError) as excinfo:
        list(apply_filters(sample_videos, filters))  # Convert generator to list to trigger evaluation

    assert "All filters must be callable" in str(excinfo.value)
