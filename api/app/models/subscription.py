from collections.abc import Callable
from datetime import date, datetime, timedelta
from enum import StrEnum
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import JSON, Column
from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel  # type: ignore

T = TypeVar("T", bound=timedelta | datetime)
type ComparisonFunc[T: timedelta | datetime] = Callable[[T, T], bool]


class RetentionType(StrEnum):
    DATE_SINCE = "DateSince"
    COUNT = "Count"
    DELTA = "Delta"


class TimeDeltaTypeValue(BaseModel):
    days: int
    weeks: int
    months: int
    years: int


class SubscriptionCreate(SQLModel):
    url: str


class SubscriptionType(StrEnum):
    CHANNEL = "Channel"
    PLAYLIST = "Playlist"
    VIDEO = "Video"


class SubscriptionError(StrEnum):
    CHANNEL_NOT_FOUND = "Channel Not Found"  # No user action possible
    PLAYLIST_NOT_FOUND = "Playlist Not Found"  # No user action possible
    UNAUTHORIZED = "Unauthorized"  # User action required??
    TIMEOUT = "Timeout"  # No user action possible, but we can retry
    REFUSED = "Refused"  # No user action possible, but we can retry
    NONEXISTENT = "Nonexistent"  # No user action possible


class SubscriptionErrorType:
    error_type: SubscriptionError
    message: str


class PlexLibraryDestination(SQLModel):
    locationId: int
    directoryId: int


class RetentionPolicy(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    subscription_id: int | None = Field(default=None, foreign_key="subscription.id")
    subscription: "Subscription" = Relationship(back_populates="retention")  # TODO: Why the name discrepancy works?
    type: RetentionType
    videoCount: int
    dateBefore: date
    timeDeltaTypeValue: timedelta


class Subscription(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str = Field(default=None)
    filters: list["Filter"] = Relationship(back_populates="subscription")
    image: str | None = None
    last_updated: datetime | None = Field(default=None, index=True)
    # TODO: Rename this to be more generic as a destination (Not just plex related)
    plex_library_path: PlexLibraryDestination | str = Field(sa_column=Column(JSON))
    retention: RetentionPolicy = Relationship(back_populates="subscription")
    rss_feed_url: str = Field(default=None)
    # SubscriptionError: SubscriptionErrorType | None = Field(default=None)
    title: str = Field(default=None)
    type: SubscriptionType = Field(default=SubscriptionType.CHANNEL)
    url: str = Field(default=None, unique=True)
    videos: Mapped[list["Video"]] = Relationship(
        back_populates="subscription",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )


#  TODO: We should split out the reasons for filtering or excluding a video.
class VideoStatus(StrEnum):
    PENDING = "Pending"
    OBTAINING_METADATA = "Obtaining Metadata"
    OBTAINED_METADATA = "Obtained Metadata"
    DOWNLOADING = "Downloading"
    PENDING_DOWNLOAD = "Pending Download"
    FAILED = "Failed"
    DELETED = "Deleted"
    DOWNLOADED = "Downloaded"
    EXCLUDED = "Excluded"
    FILTERED = "Filtered"
    RETENTION_SKIPPED = "Retention Skipped"
    # COPYRIGHT_STRIKE = "Copyright Strike"
    # DMCA = "DMCA"


class MetadataErrorType(StrEnum):
    # TODO: "Live stream offline"
    # "Live stream currently offline"
    LIVE_EVENT_NOT_STARTED = "Live event not started"
    VIDEO_UNAVAILABLE = "Video unavailable"
    COPYRIGHT_STRIKE = "Copyright strike"
    UNKNOWN_ERROR = "Unknown error"
    AGE_RESTRICTED = "Age restricted"


class Thumbnail(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    width: str
    height: str


class FilterType(StrEnum):
    DURATION = "duration"
    TITLE_CONTAINS = "title_contains"
    DESCRIPTION_CONTAINS = "description_contains"
    PUBLISHED_AFTER = "published_after"


class ComparisonOperator(StrEnum):
    LT = "<"
    LE = "<="
    EQ = "=="
    NE = "!="
    GE = ">="
    GT = ">"


ops: dict[ComparisonOperator, ComparisonFunc[datetime]] = {
    ComparisonOperator.LT: lambda x, y: x < y,
    ComparisonOperator.LE: lambda x, y: x <= y,
    ComparisonOperator.EQ: lambda x, y: x == y,
    ComparisonOperator.NE: lambda x, y: x != y,
    ComparisonOperator.GE: lambda x, y: x >= y,
    ComparisonOperator.GT: lambda x, y: x > y,
}


class Video(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    author: str
    duration: int | None = Field(default=None, alias="duration")
    description: str | None
    # filtered_reason: list[FilterType] | None = None
    link: str
    published: datetime | None = Field(default=None, index=True)
    metadata_error: MetadataErrorType | None = Field(default=None)
    retry_count: int = Field(default=0)
    status: VideoStatus = Field(sa_column_kwargs={"default": VideoStatus.PENDING}, index=True)
    subscription_id: int = Field(default=None, foreign_key="subscription.id", index=True)
    subscription: Mapped[Subscription] = Relationship(back_populates="videos")
    thumbnail_url: str | None = None
    title: str
    video_id: str = Field(unique=True)


class ChannelInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    rss_link: str
    image_link: str
    description: str


class Filter(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filter_type: FilterType

    keyword: str | None = Field(default=None)
    comparison_operator: ComparisonOperator | None = Field(default=None)
    threshold_seconds: int | None = Field(default=None)
    threshold_date: datetime | None = Field(default=None)

    subscription_id: int | None = Field(default=None, foreign_key="subscription.id")
    subscription: Subscription = Relationship(back_populates="filters")

    def to_callable(self) -> Callable[[Video], bool]:
        if self.filter_type == FilterType.DURATION:
            return lambda v: self._compare_duration(v.duration)
        elif self.filter_type == FilterType.TITLE_CONTAINS:
            return lambda v: (
                self.keyword.lower() in v.title.lower() if self.keyword else False  # pylint: disable=no-member
            )
        elif self.filter_type == FilterType.DESCRIPTION_CONTAINS:
            return lambda v: (
                self.keyword.lower() in v.description.lower()  # pylint: disable=no-member
                if self.keyword and v.description
                else False
            )
        elif self.filter_type == FilterType.PUBLISHED_AFTER:
            return lambda v: self._compare_datetime(v.published)
        else:
            raise ValueError(f"Unknown filter type: {self.filter_type}")

    def _compare_duration(self, duration: int | None) -> bool:
        if duration is None or self.threshold_seconds is None or self.comparison_operator is None:
            return False
        return not self._compare(
            timedelta(seconds=duration), self.comparison_operator, timedelta(seconds=self.threshold_seconds)
        )

    def _compare_datetime(self, timestamp: datetime | None) -> bool:
        if self.threshold_date is None or self.comparison_operator is None or timestamp is None:
            return False
        return self._compare(timestamp, self.comparison_operator, self.threshold_date)

    def _compare(
        self, value: datetime | timedelta, operator: ComparisonOperator, threshold: datetime | timedelta
    ) -> bool:
        value_dt = datetime.now() + value if isinstance(value, timedelta) else value
        threshold_dt = datetime.now() + threshold if isinstance(threshold, timedelta) else threshold

        return ops[operator](value_dt, threshold_dt)


class SubscriptionCreateV2(BaseModel):
    url: str
    filters: list[Filter] = Field(default_factory=list)
    retentionPolicy: RetentionPolicy
    plexLibraryDestination: PlexLibraryDestination
