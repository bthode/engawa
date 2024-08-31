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
    duration: Mapped[DurationCriteria] | None = Relationship(sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    string: Mapped[StringCriteria] | None = Relationship(sa_relationship_kwargs={"cascade": "all, delete-orphan"})
