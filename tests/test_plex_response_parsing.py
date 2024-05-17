import os
import xml.etree.ElementTree as ET
import unittest

from engawa.plex.parsing import Location, MediaContainer, parse_media_container


class TestMediaContainerParsing(unittest.TestCase):
    def test_parse_media_container(self) -> None:
        xml_file_path: str = os.path.join(os.path.dirname(__file__), "resources", "libraries.xml")
        with open(xml_file_path, "r", encoding="utf-8") as file:
            plex_library_data: ET.Element = ET.fromstring(file.read())

        mc: MediaContainer = parse_media_container(plex_library_data)

        self.assertEqual(mc.name, "Plex Library")
        self.assertEqual(mc.size, 11)
        self.assertEqual(mc.allow_sync, 0)

        self.assertEqual(len(mc.directories), 4)

        self.assertEqual(mc.directories[0].allow_sync, 1)
        self.assertEqual(mc.directories[0].art, "/:/resources/movie-fanart.jpg")
        self.assertEqual(mc.directories[0].composite, "/library/sections/12/composite/1678276690")
        self.assertEqual(mc.directories[0].filters, 1)
        self.assertEqual(mc.directories[0].refreshing, 0)
        self.assertEqual(mc.directories[0].thumb, "/:/resources/movie.png")
        self.assertEqual(mc.directories[0].key, 12)
        self.assertEqual(mc.directories[0].type_, "movie")
        self.assertEqual(mc.directories[0].title, "Movies")
        self.assertEqual(mc.directories[0].agent, "tv.plex.agents.movie")
        self.assertEqual(mc.directories[0].scanner, "Plex Movie")
        self.assertEqual(mc.directories[0].language, "en-US")
        self.assertEqual(mc.directories[0].uuid, "5401a1c5-962d-4a4c-a496-0021139479ae")
        self.assertEqual(mc.directories[0].updated_at, "1678276676")
        self.assertEqual(mc.directories[0].created_at, "1678276676")
        self.assertEqual(mc.directories[0].scanned_at, "1678276690")
        self.assertEqual(mc.directories[0].content, 1)
        self.assertEqual(mc.directories[0].directory, 1)
        self.assertEqual(mc.directories[0].content_changed_at, "743145")
        self.assertEqual(mc.directories[0].hidden, 0)
        self.assertEqual(len(mc.directories[0].location), 1)


if __name__ == "__main__":
    unittest.main()
