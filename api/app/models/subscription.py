from collections.abc import Callable
from datetime import datetime, timedelta
from enum import StrEnum

from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel  # type:ignore


class Retention(StrEnum):
    DATE_BASED = "Date Based"
    COUNT_BASED = "Count Based"


class SubscriptionCreate(SQLModel):
    url: str


class SubscriptionType(StrEnum):
    CHANNEL = "Channel"
    PLAYLIST = "Playlist"
    VIDEO = "Video"


class SubscriptionDirectoryError(StrEnum):
    UNAUTHORIZED = "Unauthorized"
    TIMEOUT = "Timeout"
    REFUSED = "Refused"
    NONEXISTENT = "Nonexistent"


class Subscription(SQLModel, table=True):
    description: str = Field(default=None)
    filters: list["Filter"] = Relationship(back_populates="subscription")
    error_state: SubscriptionDirectoryError | None = None
    id: int = Field(default=None, primary_key=True)
    image: str | None = None
    last_updated: datetime | None = Field(default=None, index=True)
    rss_feed_url: str = Field(default=None)
    title: str = Field(default=None)
    type: SubscriptionType = Field(default=SubscriptionType.CHANNEL)
    url: str = Field(default=None, unique=True)
    videos: Mapped[list["Video"]] = Relationship(
        back_populates="subscription",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )


class VideoStatus(StrEnum):
    PENDING = "Pending"
    OBTAINING_METADATA = "Obtaining Metadata"
    OBTAINED_METADATA = "Obtained Metadata"
    DOWNLOADING = "Downloading"
    FAILED = "Failed"
    DELETED = "Deleted"
    COMPLETE = "Complete"
    EXCLUDED = "Excluded"
    COPYRIGHT_STRIKE = "Copyright Strike"
    DMCA = "DMCA"


class Thumbnail(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    width: str
    height: str


class Video(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    author: str
    duration: int | None = Field(default=None, alias="duration")
    description: str | None
    link: str
    published: datetime | None = Field(default=None, index=True)
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


class FilterType(StrEnum):
    DURATION = "duration"
    TITLE_CONTAINS = "title_contains"
    DESCRIPTION_CONTAINS = "description_contains"
    PUBLISHED_AFTER = "published_after"


class ComparisonOperator(StrEnum):
    LT = "lt"
    LE = "le"
    EQ = "eq"
    NE = "ne"
    GE = "ge"
    GT = "gt"


class Filter(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filter_type: FilterType

    keyword: str | None = Field(default=None)
    comparison_operator: ComparisonOperator | None = Field(default=None)
    threshold_seconds: int | None = Field(default=None)
    threshold_date: datetime | None = Field(default=None)

    subscription_id: int | None = Field(default=None, foreign_key="subscription.id")
    subscription: Subscription = Relationship(back_populates="filters")

    def to_callable(self) -> Callable[["Video"], bool]:
        if self.filter_type == FilterType.DURATION:
            return lambda v: self._compare_duration(v.duration)
        elif self.filter_type == FilterType.TITLE_CONTAINS:
            return lambda v: self.keyword.lower() in v.title.lower() if self.keyword else False
        elif self.filter_type == FilterType.DESCRIPTION_CONTAINS:
            return lambda v: self.keyword.lower() in v.description.lower() if self.keyword and v.description else False
        elif self.filter_type == FilterType.PUBLISHED_AFTER:
            return lambda v: self._compare_datetime(v.published)
        else:
            raise ValueError(f"Unknown filter type: {self.filter_type}")

    def _compare_duration(self, duration: int | None) -> bool:
        if duration is None or self.threshold_seconds is None or self.comparison_operator is None:
            return False
        return self._compare(
            timedelta(seconds=duration), self.comparison_operator, timedelta(seconds=self.threshold_seconds)
        )

    def _compare_datetime(self, date: datetime | None) -> bool:
        if self.threshold_date is None or self.comparison_operator is None or date is None:
            return False
        return self._compare(date, self.comparison_operator, self.threshold_date)

    def _compare(
        self, value: timedelta | datetime, operator: ComparisonOperator, threshold: timedelta | datetime
    ) -> bool:
        # if isinstance(value, (datetime, timedelta)) and isinstance(threshold, (datetime, timedelta)):
        #     if isinstance(value, datetime) and isinstance(threshold, timedelta):
        #         threshold = datetime.now() + threshold
        #     elif isinstance(value, timedelta) and isinstance(threshold, datetime):
        #         value = datetime.now() + value
        if operator == ComparisonOperator.LT:
            return value < threshold
        elif operator == ComparisonOperator.LE:
            return value <= threshold
        elif operator == ComparisonOperator.EQ:
            return value == threshold
        elif operator == ComparisonOperator.NE:
            return value != threshold
        elif operator == ComparisonOperator.GE:
            return value >= threshold
        elif operator == ComparisonOperator.GT:
            return value > threshold
