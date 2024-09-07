from enum import StrEnum

from sqlmodel import Field, Relationship, SQLModel

from app.models.subscription import Subscription



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
    subscription_id: int = Field(default=None, foreign_key="subscription.id")
    status: VideoStatus = Field(sa_column_kwargs={"default": VideoStatus.PENDING})
    subscription: Subscription = Relationship(
        back_populates="videos",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"}
    )


class ChannelInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    rss_link: str
    image_link: str
    description: str
