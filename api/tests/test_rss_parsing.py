import pytest
from engawa.api.plex_service import PlexService
from requests import Timeout


def test_fetch_rss_feed():
    def mock_make_request(url: str, timeout: int) -> str:  # pylint: disable=W0613
        return """
        <html>
            <head>
                <title>Test Title</title>
                <meta name="description" content="Test Description">
                <link type="application/rss+xml" title="RSS" href="http://test.com/rss">
                <link rel="image_src" href="http://test.com/image.jpg">
            </head>
            <body></body>
        </html>
        """

    result = PlexService.fetch_rss_feed("http://test.com", mock_make_request)

    assert result == {
        "title": "Test Title",
        "description": "Test Description",
        "rss_link": "http://test.com/rss",
        "image_link": "http://test.com/image.jpg",
    }


def test_fetch_rss_feed_timeout():
    def mock_make_request(url: str, timeout: int) -> str:
        raise Timeout("Request timed out")

    with pytest.raises(Timeout):
        PlexService.fetch_rss_feed("http://example.com", request_maker=mock_make_request)


def test_fetch_rss_feed_connection_error():
    def mock_make_request(url: str, timeout: int) -> str:
        raise ConnectionError("Connection refused")

    with pytest.raises(ConnectionError):
        PlexService.fetch_rss_feed("http://example.com", request_maker=mock_make_request)


def test_fetch_rss_feed_auth_required():
    def mock_make_request(url: str, timeout: int) -> str:  # pylint: disable=W0613
        return "<html><body><h1>401 Unauthorized</h1></body></html>"

    with pytest.raises(ValueError):
        PlexService.fetch_rss_feed("http://example.com", request_maker=mock_make_request)


def test_fetch_rss_feed_non_html_response():
    def mock_make_request(url: str, timeout: int) -> str:  # pylint: disable=W0613
        return "This is not an HTML response"

    with pytest.raises(ValueError):
        PlexService.fetch_rss_feed("http://example.com", request_maker=mock_make_request)


def test_fetch_rss_feed_no_rss_link():
    def mock_make_request(url: str, timeout: int) -> str:  # pylint: disable=W0613
        return "<html><head></head></html>"

    with pytest.raises(ValueError):
        PlexService.fetch_rss_feed("http://example.com", request_maker=mock_make_request)
