import unittest
import sys
import pathlib

# Add the src directory to sys.path so we can import the module.
src_path = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

from emoji_mood import get_emojis

class TestEmojiMood(unittest.TestCase):
    def test_known_mood(self):
        self.assertEqual(get_emojis("happy"), ["😄", "😊", "🥳"])

    def test_case_insensitivity(self):
        self.assertEqual(get_emojis("SaD"), ["😢", "😞", "☔"])

    def test_unknown_mood(self):
        self.assertEqual(get_emojis("ecstatic"), [])

    def test_whitespace(self):
        self.assertEqual(get_emojis("  love  "), ["❤️", "😍", "💖"])

if __name__ == "__main__":
    unittest.main()
