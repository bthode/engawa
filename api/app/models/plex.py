from enum import StrEnum

from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel  # type: ignore

# TODO: Just because we get back Directory/Location in a confusing manner from Plex doesn't mean
# we should make the naming confusing in our model/db.


class ErrorState(StrEnum):
    UNAUTHORIZED = "unauthorized"
    TIMEOUT = "timeout"
    REFUSED = "refused"


class PlexBase(SQLModel):
    name: str = Field(index=True)


class Plex(PlexBase, table=True):
    id: int = Field(default=None, primary_key=True)
    directories: Mapped[list["Directory"]] = Relationship(
        back_populates="plex", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    endpoint: str
    port: str
    token: str
    error_state: ErrorState | None = Field(default=None)


class PlexServerCreate(PlexBase):
    endpoint: str
    port: str
    token: str


class PlexServerUpdate(PlexBase):
    id: int
    name: str
    endpoint: str
    port: str
    token: str


class PlexServerPublic(PlexBase):
    id: int


class DirectoryBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    uuid: str
    key: int


class Directory(DirectoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    plex: Mapped[Plex] = Relationship(back_populates="directories")
    plex_id: int = Field(default=None, foreign_key="plex.id", index=True)
    locations: Mapped[list["Location"]] = Relationship(
        back_populates="directory",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )


class LocationBase(SQLModel):
    path: str = Field()
    # TODO: Would be ideal to be able to return the id_ as id, not sure if SQLModel supports this
    id_: int | None = Field(default=None, primary_key=True)


class LocationPublic(LocationBase):
    pass


class DirectoryPublic(DirectoryBase):
    locations: list[LocationPublic] = []


class DirectoryCreate(DirectoryBase):
    pass


class DirectoryPublicWithPlexServer(DirectoryPublic):
    plex: PlexServerPublic | None = None


class PlexPublicWithDirectories(PlexServerPublic):
    directories: list[DirectoryPublic] = []
    endpoint: str
    port: str
    error_state: ErrorState | None = None


class Location(LocationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    directory_id: int = Field(default=None, foreign_key="directory.id")
    directory: Mapped[Directory] = Relationship(back_populates="locations")
