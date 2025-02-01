import unittest

from story_writer.constants import StoryStructureEnum


class TestStoryStructureEnum(unittest.TestCase):

    def test_config_input_success(self):
        # Value from config (set by user)
        test_values = [
            "classic story structure",
            "three act structure",
            "fiveact structure",
            "seven point story structure",
            "freytag's pyramid",
            "thehero'sjourney",
            "danharmonsstorycircle",
            "story spine",
            "fichteancurve",
            "in medias res",
            "save the cat",
        ]
        for value in test_values:
            with self.subTest(msg=f"Testing string '{value}'"):
                result = StoryStructureEnum(value)

                self.assertIsInstance(result, StoryStructureEnum)

    def test_config_input_failure(self):
        # Value from config (set by user)
        value = "Don't Save the cat"
        with self.assertRaises(ValueError):
            StoryStructureEnum(value)
