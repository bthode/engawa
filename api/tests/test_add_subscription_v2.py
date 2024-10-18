import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlmodel import SQLModel, select

from app.database.session import engine
from app.main import app
from app.models.plex import Directory, Location, Plex
from app.models.subscription import (
    PlexLibraryDestination,
    RetentionPolicyModel,
    RetentionType,
    SubscriptionCreateV2,
)


@pytest.fixture(scope="function")
def test_db():
    SQLModel.metadata.create_all(engine)  # type: ignore
    yield
    SQLModel.metadata.drop_all(engine)  # type: ignore


@pytest.fixture
def test_plex_server(test_db):
    with Session(engine) as session:
        # Create a test Plex server
        plex_server = Plex(name="Test Plex Server", endpoint="http://localhost", port="32400", token="test_token")
        session.add(plex_server)
        session.commit()

        # Create test directories
        session.add(Directory(title="Movies", uuid="a", key=1, plex_id=plex_server.id))
        session.add(Directory(title="TV Shows", uuid="b", key=2, plex_id=plex_server.id))
        session.commit()

        directory1 = session.execute(select(Directory).where(Directory.uuid == "a")).scalar_one()
        directory2 = session.execute(select(Directory).where(Directory.uuid == "b")).scalar_one()

        # Create test locations
        assert directory1.id and directory2.id is not None, "directory1.id should not be None"
        location1 = Location(path="/media/movies", directory_id=directory1.id)
        location2 = Location(path="/media/tv_shows", directory_id=directory2.id)
        session.add(location1)
        session.add(location2)
        session.commit()

        yield plex_server


@pytest.fixture
def test_plex_data(test_plex_server):
    with Session(engine) as session:
        plex_server = session.get(Plex, test_plex_server.id)
        directories = plex_server.directories
        locations = [location for directory in directories for location in directory.locations]
        return {"plex_server": plex_server, "directories": directories, "locations": locations}


client = TestClient(app)


def test_create_subscription_v2():
    subscription_data = {
        "url": "https://www.youtube.com/channel/UCsXVk37bltHxD1rDPwtNM8Q",
        "filters": [{"filterType": "duration", "comparisonOperator": "gt", "thresholdSeconds": 600}],
        "retentionPolicy": {
            "type": RetentionType.COUNT,
            "videoCount": 10,
            "dateBefore": "2024-10-18",
            "timeDeltaTypeValue": "0 days",
        },
        "plexLibraryDestination": {"locationId": 1, "directoryId": 1},
    }

    response = client.post("/api/subscription/v2", json=subscription_data)
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["message"] == "Subscription logged successfully"

    # Optionally, you can add more assertions to check the response content
    created_subscription = response.json()
    assert created_subscription["id"] == 12345  # Adjust this based on your expected behavior
