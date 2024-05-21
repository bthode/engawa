import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class VideoStatus(enum.Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    FAILED = "Failed"
    DELETED = "Deleted"
    COMPLETE = "Complete"
    EXCLUDED = "Excluded"


class Retention(enum.Enum):
    DATE_BASED = "Date Based"
    COUNT_BASED = "Count Based"


class Policy(Base):
    __tablename__ = "policy"
    id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    type = Column(Enum(Retention), default=Retention.DATE_BASED)
    days_to_retain = Column(Integer, default=7)
    subscription = relationship("Subscription", back_populates="policy")


class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    url = Column(String, unique=True)
    title = Column(String)
    status = Column(Enum(VideoStatus))
    subscription = relationship("Subscription", back_populates="videos")
    created_at = Column(DateTime, nullable=False)
    download_attempts = Column(Integer)
    saved_path = Column(String)

    def __str__(self):
        return (
            f"Video(url={self.url}, status={self.status}, "
            f"download_attempts={self.download_attempts}, subscription={self.subscription},"
            f"title={self.title}, created_at={self.created_at})"
        )


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String, unique=True)
    rss_feed_url = Column(String)
    last_queried = Column(DateTime)
    videos = relationship("Video", back_populates="subscription")
    policy = relationship("Policy", back_populates="subscription", uselist=False)


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    key = Column(String(50), unique=True, nullable=False)
    value = Column(String, nullable=False)
    value_type = Column(String(20), nullable=False)

    def __repr__(self):
        return f"<Setting(key='{self.key}', value='{self.value}', value_type='{self.value_type}')>"
