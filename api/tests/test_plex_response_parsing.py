import os
import unittest

from src.engawa.plex.parsing import MediaContainer, parse_plex_data


class TestMediaContainerParsing(unittest.TestCase):
    def test_parse_media_container(self) -> None:
        xml_file_path: str = os.path.join(os.path.dirname(__file__), "resources", "libraries.xml")
        with open(xml_file_path, encoding="utf-8") as file:
            plex_library_data: str = file.read()

        mc: MediaContainer = parse_plex_data(plex_library_data)

        assert mc.name == "Plex Library"
        assert mc.size == 2
        assert mc.allow_sync == 0

        assert len(mc.directories) == 2

        movies_dir = mc.directories[0]
        assert movies_dir.allow_sync == 1
        assert movies_dir.art == "/:/resources/movie-fanart.jpg"
        assert movies_dir.composite == "/library/sections/3/composite/1686100533"
        assert movies_dir.filters == 1
        assert movies_dir.refreshing == 0
        assert movies_dir.thumb == "/:/resources/movie.png"
        assert movies_dir.key == 3
        assert movies_dir.type_ == "movie"
        assert movies_dir.title == "Movies"
        assert movies_dir.agent == "tv.plex.agents.movie"
        assert movies_dir.scanner == "Plex Movie"
        assert movies_dir.language == "en-US"
        assert movies_dir.uuid == "364f2ba8-254e-492d-a8d5-8658cfc90161"
        assert movies_dir.updated_at == "1662601802"
        assert movies_dir.created_at == "1662601802"
        assert movies_dir.scanned_at == "1686100533"
        assert movies_dir.content == 1
        assert movies_dir.directory == 1
        assert movies_dir.content_changed_at == "688787"
        assert movies_dir.hidden == 0
        assert len(movies_dir.location) == 1
        assert movies_dir.location[0].id_ == 3
        assert movies_dir.location[0].path == "/media/Media/Video/Movies"

        youtube_dir = mc.directories[1]
        assert youtube_dir.allow_sync == 1
        assert youtube_dir.art == "/:/resources/movie-fanart.jpg"
        assert youtube_dir.composite == "/library/sections/7/composite/1699802001"
        assert youtube_dir.filters == 1
        assert youtube_dir.refreshing == 0
        assert youtube_dir.thumb == "/:/resources/movie.png"
        assert youtube_dir.key == 7
        assert youtube_dir.type_ == "movie"
        assert youtube_dir.title == "YouTube"
        assert youtube_dir.agent == "com.plexapp.agents.sicktube"
        assert youtube_dir.scanner == "Plex Movie Scanner"
        assert youtube_dir.language == "en"
        assert youtube_dir.uuid == "0c717b05-2deb-419c-a2d0-e68cceddea14"
        assert youtube_dir.updated_at == "1686965178"
        assert youtube_dir.created_at == "1674232261"
        assert youtube_dir.scanned_at == "1699802001"
        assert youtube_dir.content == 1
        assert youtube_dir.directory == 1
        assert youtube_dir.content_changed_at == "1231054"
        assert youtube_dir.hidden == 0
        assert len(youtube_dir.location) == 2
        assert youtube_dir.location[0].id_ == 17
        assert youtube_dir.location[0].path == "/index/YouTube"
        assert youtube_dir.location[1].id_ == 7
        assert youtube_dir.location[1].path == "/nas/media"


if __name__ == "__main__":
    unittest.main()
