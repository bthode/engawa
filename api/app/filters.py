import operator
from collections.abc import Callable, Generator
from datetime import datetime, timedelta

from app.models.subscription import Video


@staticmethod
def duration_filter(duration: str, comparison: str, threshold: timedelta) -> bool:
    duration_td = datetime.strptime(duration, "%H:%M:%S") - datetime(1900, 1, 1)
    comparison_ops = {
        "lt": operator.lt,
        "le": operator.le,
        "eq": operator.eq,
        "ne": operator.ne,
        "ge": operator.ge,
        "gt": operator.gt,
    }
    if comparison not in comparison_ops:
        raise ValueError(f"Invalid comparison operator: {comparison}")
    return comparison_ops[comparison](duration_td, threshold)


@staticmethod
def title_contains_filter(keyword: str) -> Callable[[Video], bool]:
    return lambda video: keyword.lower() in video.title.lower()


@staticmethod
def description_contains_filter(keyword: str) -> Callable[[Video], bool]:
    return lambda video: keyword.lower() in video.description.lower()


@staticmethod
def published_after_filter(date: datetime) -> Callable[[Video], bool]:
    return lambda video: isinstance(video.published, datetime) and video.published > date


@staticmethod
def apply_filters(videos: list[Video], filters: list[Callable[[Video], bool]]) -> Generator[Video, None, None]:
    valid_filters = [f for f in filters if callable(f)]
    if len(valid_filters) != len(filters):
        raise TypeError("All filters must be callable")
    return (video for video in videos if all(f(video) for f in valid_filters))
