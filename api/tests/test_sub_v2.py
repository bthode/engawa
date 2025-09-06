from datetime import date, timedelta
from unittest.mock import Mock, patch

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

# from app.models.plex import Directory, Location, Plex
from app.models.plex import Plex
from app.models.subscription import (
    ComparisonOperator,
    Filter,
    FilterType,
    PlexLibraryDestination,
    RetentionPolicy,
    RetentionType,
    SubscriptionCreateV2,
    TimeDeltaTypeValue,
)
from app.routers.subscription import router


@pytest.mark.asyncio
async def test_create_subscription_v2_happy_path():
    # Mock data
    mock_channel_info = Mock(
        title="Test Channel",
        rss_link="https://example.com/rss",
        description="Test Description",
        image_link="https://example.com/image.jpg",
    )

    time_delta_value = TimeDeltaTypeValue(days=1, weeks=0, months=0, years=0)

    # Create test data
    test_filter = Filter(
        filter_type=FilterType.DURATION, comparison_operator=ComparisonOperator.GT, threshold_seconds=1800
    )

    retention_policy = RetentionPolicy(
        type=RetentionType.COUNT,
        videoCount=10,
        timeDeltaTypeValue=time_delta_value,
        dateBefore=(date.today() - timedelta(days=30)),
    )

    plex_destination = PlexLibraryDestination(locationId=1, directoryId=1)

    subscription_data = SubscriptionCreateV2(
        url="https://youtube.com/channel/test",
        filters=[test_filter],
        retentionPolicy=retention_policy,
        plexLibraryDestination=plex_destination,
    )

    # Mock the database session
    mock_session = Mock(spec=AsyncSession)
    mock_session.execute.return_value.scalars.return_value.first.return_value = None

    # Mock Plex server data
    # mock_location = Location(id_=1, path="/test/path")
    # mock_directory = Directory(key=1, locations=[mock_location], title="Test Directory", uuid="test_uuid")
    mock_plex = Plex(
        name="Test Plex",
        endpoint="http://test.com",
        port="32400",
        token="test_token",
    )

    # Setup mocks
    with (
        patch("app.routers.youtube.fetch_rss_feed", return_value=mock_channel_info),
        patch("requests.get") as mock_requests,
    ):

        # Mock the image request
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake_image_data"
        mock_requests.return_value = mock_response

        # Mock the Plex query
        mock_session.execute.return_value.scalars.return_value.first.side_effect = [
            None,  # First call for existing subscription check
            mock_plex,  # Second call for Plex server check
        ]

        # Create FastAPI test client
        app = FastAPI()

        app.include_router(router)

        async with AsyncClient(app=app, base_url="http://localhost") as ac:
            response = await ac.post(
                "/subscription/v2",
                json=subscription_data.model_dump(),
            )

        # Assertions
        assert response.status_code == 200
        assert response.json()["message"] == "Subscription logged successfully"
        assert "id" in response.json()

        # Verify the session was used correctly
        mock_session.add.assert_called_once()
        mock_session.commit.assert_awaited_once()


# def test_create_subscription_v2_happy_path(client: TestClient):
#     # Prepare test data
#     subscription_data = {
#         "url": "https://www.youtube.com/channel/UC123456789",
#         "filters": [
#             {
#                 "filter_type": FilterType.DURATION,
#                 "comparison_operator": ComparisonOperator.GT,
#                 "threshold_seconds": 300,  # 5 minutes
#             },
#             {"filter_type": FilterType.TITLE_CONTAINS, "keyword": "Tutorial"},
#         ],
#         "retentionPolicy": {
#             "type": RetentionType.COUNT,
#             "videoCount": 50,
#             "dateBefore": date.today().isoformat(),
#             "timeDeltaTypeValue": str(timedelta(days=30)),
#         },
#         "plexLibraryDestination": {"locationId": 1, "directoryId": 2},
#     }

#     # Make the request
#     response = client.post("/api/v2/subscriptions", json=subscription_data)

#     # Assertions
#     assert response.status_code == 201

#     created_subscription = response.json()
#     assert created_subscription["url"] == subscription_data["url"]
#     assert len(created_subscription["filters"]) == 2
#     assert created_subscription["type"] == SubscriptionType.CHANNEL

#     # Verify filters were created correctly
#     duration_filter = next(f for f in created_subscription["filters"] if f["filter_type"] == FilterType.DURATION)
#     assert duration_filter["comparison_operator"] == ComparisonOperator.GT
#     assert duration_filter["threshold_seconds"] == 300

#     title_filter = next(f for f in created_subscription["filters"] if f["filter_type"] == FilterType.TITLE_CONTAINS)
#     assert title_filter["keyword"] == "Tutorial"

#     # Verify retention policy
#     retention = created_subscription["retention"]
#     assert retention["type"] == RetentionType.COUNT
#     assert retention["videoCount"] == 50

#     # Verify plex library destination
#     plex_dest = created_subscription["plex_library_path"]
#     assert plex_dest["locationId"] == 1
#     assert plex_dest["directoryId"] == 2
