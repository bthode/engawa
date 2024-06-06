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


class Subscription(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(default=None)
    url: str = Field(default=None, unique=True)
    description: str = Field(default=None)
    rss_feed_url: str = Field(default=None)
    image: str | None = None

    # last_queried: datetime = Field(default=None)
    # videos: list["Video"] = Relationship(back_populates="subscription")
    # policy: "Policy" = Relationship(back_populates="subscription")


# class Policy(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     subscription_id: int = Field(default=None, foreign_key="subscription.id")
#     type: Retention = Field(default=Retention.DATE_BASED)
#     days_to_retain: int = Field(default=7)
#     subscription: "Subscription" = Relationship(back_populates="policy")


# class Video(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     subscription_id: int = Field(default=None, foreign_key="subscription.id")
#     url: str = Field(default=None, unique=True)
#     title: str = Field(default=None)
#     status: VideoStatus = Field(default=None)
#     subscription: "Subscription" = Relationship(back_populates="videos")
#     created_at: datetime = Field(default=None)
#     download_attempts: int = Field(default=None)
#     saved_path: str = Field(default=None)
