from datetime import datetime
from enum import StrEnum

from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel  # type: ignore  # type: ignore


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
    error_state: SubscriptionDirectoryError | None = None
    id: int = Field(default=None, primary_key=True)
    image: str | None = None
    last_updated: datetime | None = None
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
    COPYWRITE_STRIKE = "Copywrite Strike"
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
    link: str
    published: str
    retry_count: int = Field(default=0)
    status: VideoStatus = Field(sa_column_kwargs={"default": VideoStatus.PENDING})
    subscription_id: int = Field(default=None, foreign_key="subscription.id")
    subscription: Mapped[Subscription] = Relationship(back_populates="videos")
    thumbnail_url: str
    title: str
    video_id: str = Field(unique=True)


class ChannelInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    rss_link: str
    image_link: str
    description: str
