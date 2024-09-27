from collections.abc import Callable

from app.models.subscription import (
    Filter,
    Video,
    VideoStatus,
)


def apply_filters(videos: list[Video], filters: list[Filter]) -> list[Video]:
    filter_callables: list[Callable[[Video], bool]] = [f.to_callable() for f in filters]

    for video in videos:
        if video.status == VideoStatus.OBTAINED_METADATA:
            if all(f(video) for f in filter_callables):
                video.status = VideoStatus.PENDING_DOWNLOAD
            else:
                video.status = VideoStatus.FILTERED

    return videos
