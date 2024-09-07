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
    id: int = Field(default=None, primary_key=True)
    title: str = Field(default=None)
    url: str = Field(default=None, unique=True)
    description: str = Field(default=None)
    rss_feed_url: str = Field(default=None)
    image: str | None = None
    type: SubscriptionType = Field(default=SubscriptionType.CHANNEL)
    error_state: SubscriptionDirectoryError | None = None
    videos: Mapped[list["Video"]] = Relationship(
        back_populates="subscription",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )


class VideoStatus(StrEnum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    FAILED = "Failed"
    DELETED = "Deleted"
    COMPLETE = "Complete"
    EXCLUDED = "Excluded"


class Thumbnail(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    width: str
    height: str


class Video(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    published: str
    video_id: str = Field(unique=True)
    link: str
    author: str
    thumbnail_url: str
    subscription: Mapped[Subscription] = Relationship(back_populates="videos")
    subscription_id: int = Field(default=None, foreign_key="subscription.id")
    status: VideoStatus = Field(sa_column_kwargs={"default": VideoStatus.PENDING})


class ChannelInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    rss_link: str
    image_link: str
    description: str
