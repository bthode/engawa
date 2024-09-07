from enum import StrEnum

from sqlmodel import Field, Relationship, SQLModel  # type: ignore

from app.models.youtube import Video


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
    videos: list[Video] = Relationship(back_populates="subscription",
                                       sa_relationship_kwargs={"cascade": "all, delete-orphan"})
