from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel  # type: ignore


class Thumbnail(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    width: str
    height: str
    video_id: int = Field(default=None, foreign_key="video.id")


class Video(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    published: str
    video_id: str = Field(unique=True)
    link: str
    author: str
    thumbnail: Mapped[Thumbnail] = Relationship(sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    subscription_id: int = Field(default=None, foreign_key="subscription.id")


class ChannelInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    rss_link: str
    image_link: str
    description: str
