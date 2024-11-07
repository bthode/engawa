# TODO: Need to present a distinct list of paths to the user, which ideally is distinct in the database as well.
# TODO: Allow the user to map from 1 to all paths to what we can see on the file system, directories only.

from sqlmodel import Field, Relationship, SQLModel  # type: ignore

from app.models.plex import Location
from app.models.subscription import Subscription


# TODO: This belongs in models
class SubscriptionLocationMapping(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    subscription_id: int = Field(foreign_key="subscription.id")
    subscription: Subscription = Relationship()
    location_id: int = Field(foreign_key="location.id")
    location: Location = Relationship()
