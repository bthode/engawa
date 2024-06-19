from enum import StrEnum

from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel  # type: ignore


class FilterOperation(StrEnum):
    GREATER_THAN = "greaterThan"
    LESS_THAN = "lessThan"
    CONTAINS = "contains"
    DOES_NOT_CONTAIN = "doesNotContain"


class DurationCriteria(SQLModel):
    value: float = Field()
    unit: FilterOperation | None = Field(default=None)


class StringCriteria(SQLModel):
    text: str = Field()


class FilterCriteria(SQLModel):
    __visit_name__ = "filter_criteria"
    duration: Mapped[DurationCriteria] | None = Relationship(
        one_side=True, sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    string: Mapped[StringCriteria] | None = Relationship(
        one_side=True, sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


# class Filter(PlexBase, SQLModel):
#     name: str = Field(index=True)
#     operation: FilterOperation
#     criteria: FilterCriteria


# class DurationFilter(Filter):
#     __visit_name__ = 'duration_filter'
#     criteria: Mapped[DurationCriteria] = Relationship(back_populates="filter")


# class TitleFilter(Filter):
#     __visit_name__ = 'title_filter'
#     criteria: Mapped[StringCriteria] = Relationship(back_populates="filter")


# class AnyFilter(SQLModel):
#     __visit_name__ = 'any_filter'
#     duration: Mapped[DurationFilter] | None = Relationship(one_side=True, sa_relationship_kwargs={"cascade": "all, delete-orphan"})
#     title: Mapped[TitleFilter] | None = Relationship(one_side=True, sa_relationship_kwargs={"cascade": "all, delete-orphan"})


# class PlexServerCreate(PlexBase):
#     endpoint: str
#     port: str
#     token: str


# class PlexServerPublic(PlexBase):
#     id: int
