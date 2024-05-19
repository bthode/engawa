import os
import xml.etree.ElementTree as ET
import unittest

from engawa.plex.parsing import MediaContainer, parse_media_container


class TestMediaContainerParsing(unittest.TestCase):
    def test_parse_media_container(self) -> None:
        xml_file_path: str = os.path.join(os.path.dirname(__file__), "resources", "libraries.xml")
        with open(xml_file_path, "r", encoding="utf-8") as file:
            plex_library_data: ET.Element = ET.fromstring(file.read())

        mc: MediaContainer = parse_media_container(plex_library_data)

        # Assert the parsed MediaContainer object matches the expected values
        self.assertEqual(mc.name, "Plex Library")
        self.assertEqual(mc.size, 2)
        self.assertEqual(mc.allow_sync, 0)

        # Assert the parsed directories
        self.assertEqual(len(mc.directories), 2)

        # Assertions for the first directory ("Movies")
        movies_dir = mc.directories[0]
        self.assertEqual(movies_dir.allow_sync, 1)
        self.assertEqual(movies_dir.art, "/:/resources/movie-fanart.jpg")
        self.assertEqual(movies_dir.composite, "/library/sections/3/composite/1686100533")
        self.assertEqual(movies_dir.filters, 1)
        self.assertEqual(movies_dir.refreshing, 0)
        self.assertEqual(movies_dir.thumb, "/:/resources/movie.png")
        self.assertEqual(movies_dir.key, 3)
        self.assertEqual(movies_dir.type_, "movie")
        self.assertEqual(movies_dir.title, "Movies")
        self.assertEqual(movies_dir.agent, "tv.plex.agents.movie")
        self.assertEqual(movies_dir.scanner, "Plex Movie")
        self.assertEqual(movies_dir.language, "en-US")
        self.assertEqual(movies_dir.uuid, "364f2ba8-254e-492d-a8d5-8658cfc90161")
        self.assertEqual(movies_dir.updated_at, "1662601802")
        self.assertEqual(movies_dir.created_at, "1662601802")
        self.assertEqual(movies_dir.scanned_at, "1686100533")
        self.assertEqual(movies_dir.content, 1)
        self.assertEqual(movies_dir.directory, 1)
        self.assertEqual(movies_dir.content_changed_at, "688787")
        self.assertEqual(movies_dir.hidden, 0)
        self.assertEqual(len(movies_dir.location), 1)
        self.assertEqual(movies_dir.location[0].id_, 3)
        self.assertEqual(movies_dir.location[0].path, "/media/Media/Video/Movies")

        youtube_dir = mc.directories[1]
        self.assertEqual(youtube_dir.allow_sync, 1)
        self.assertEqual(youtube_dir.art, "/:/resources/movie-fanart.jpg")
        self.assertEqual(youtube_dir.composite, "/library/sections/7/composite/1699802001")
        self.assertEqual(youtube_dir.filters, 1)
        self.assertEqual(youtube_dir.refreshing, 0)
        self.assertEqual(youtube_dir.thumb, "/:/resources/movie.png")
        self.assertEqual(youtube_dir.key, 7)
        self.assertEqual(youtube_dir.type_, "movie")
        self.assertEqual(youtube_dir.title, "YouTube")
        self.assertEqual(youtube_dir.agent, "com.plexapp.agents.sicktube")
        self.assertEqual(youtube_dir.scanner, "Plex Movie Scanner")
        self.assertEqual(youtube_dir.language, "en")
        self.assertEqual(youtube_dir.uuid, "0c717b05-2deb-419c-a2d0-e68cceddea14")
        self.assertEqual(youtube_dir.updated_at, "1686965178")
        self.assertEqual(youtube_dir.created_at, "1674232261")
        self.assertEqual(youtube_dir.scanned_at, "1699802001")
        self.assertEqual(youtube_dir.content, 1)
        self.assertEqual(youtube_dir.directory, 1)
        self.assertEqual(youtube_dir.content_changed_at, "1231054")
        self.assertEqual(youtube_dir.hidden, 0)
        self.assertEqual(len(youtube_dir.location), 2)
        self.assertEqual(youtube_dir.location[0].id_, 17)
        self.assertEqual(youtube_dir.location[0].path, "/index/YouTube")
        self.assertEqual(youtube_dir.location[1].id_, 7)
        self.assertEqual(youtube_dir.location[1].path, "/nas/media")


if __name__ == "__main__":
    unittest.main()
