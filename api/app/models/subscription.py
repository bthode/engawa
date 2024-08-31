from enum import StrEnum

from sqlmodel import Field, SQLModel  # type: ignore


class VideoStatus(StrEnum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    FAILED = "Failed"
    DELETED = "Deleted"
    COMPLETE = "Complete"
    EXCLUDED = "Excluded"


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
    id: int = Field(default=None, primary_key=True)
    title: str = Field(default=None)
    url: str = Field(default=None, unique=True)
    description: str = Field(default=None)
    rss_feed_url: str = Field(default=None)
    image: str | None = None
    type: SubscriptionType = Field(default=SubscriptionType.CHANNEL)
    error_state: SubscriptionDirectoryError | None = None