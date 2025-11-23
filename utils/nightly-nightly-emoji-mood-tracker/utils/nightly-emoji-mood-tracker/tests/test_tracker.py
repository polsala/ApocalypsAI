import unittest
from pathlib import Path
from unittest import mock

# Import the module under test
from ..src.tracker import mood_to_emoji, parse_moods_from_args

class TestMoodToEmoji(unittest.TestCase):
    def test_known_moods(self):
        self.assertEqual(mood_to_emoji("I am feeling great today"), "😄")
        self.assertEqual(mood_to_emoji("Such a sad story"), "😢")
        self.assertEqual(mood_to_emoji("He is angry about the bug"), "😠")
        self.assertEqual(mood_to_emoji("Love is in the air"), "❤️")
        self.assertEqual(mood_to_emoji("I'm confused"), "🤔")

    def test_unknown_mood_returns_default(self):
        self.assertEqual(mood_to_emoji("just another day"), "❓")

    def test_multiple_keywords_first_match(self):
        # "happy" appears before "sad" in the mapping order, so it should win.
        self.assertEqual(mood_to_emoji("I am happy but also sad"), "😄")

class TestParseMoodsFromArgs(unittest.TestCase):
    def test_parses_positional_moods(self):
        args = mock.Mock()
        args.file = None
        args.moods = ["happy", "sad"]
        self.assertEqual(parse_moods_from_args(args), ["happy", "sad"])

    def test_parses_file_moods(self):
        # Mock rationale: we avoid real file I/O by mocking Path.read_text.
        mock_path = mock.Mock()
        mock_path.is_file.return_value = True
        mock_path.read_text.return_value = "happy\nangry\n"
        with mock.patch('pathlib.Path', return_value=mock_path):
            args = mock.Mock()
            args.file = "dummy.txt"
            args.moods = []
            self.assertEqual(parse_moods_from_args(args), ["happy", "angry"])

    def test_combines_file_and_positional(self):
        mock_path = mock.Mock()
        mock_path.is_file.return_value = True
        mock_path.read_text.return_value = "sad\n"
        with mock.patch('pathlib.Path', return_value=mock_path):
            args = mock.Mock()
            args.file = "dummy.txt"
            args.moods = ["love"]
            self.assertEqual(parse_moods_from_args(args), ["sad", "love"])

if __name__ == "__main__":
    unittest.main()
