from collections.abc import Callable
from datetime import datetime, timedelta

from app.models.subscription import ComparisonOperator, Filter, FilterType, Video


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


# def create_time_window_filter(operator: str, delta: timedelta) -> Filter:
#     return Filter(
#         filter_type=FilterType.PUBLISHED_AFTER,
#         comparison_operator=ComparisonOperator(operator),
#         threshold_date=delta
#     )


def apply_filters(videos: list[Video], filters: list[Filter]) -> list[Video]:
    filter_callables: list[Callable[[Video], bool]] = [f.to_callable() for f in filters]
    return [video for video in videos if all(f(video) for f in filter_callables)]
