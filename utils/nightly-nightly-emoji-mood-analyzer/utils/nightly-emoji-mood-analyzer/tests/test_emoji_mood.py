import unittest
import importlib.util
import pathlib


def load_emoji_mood_module():
    """Load the emoji_mood module from the sibling src directory.
    # Mock rationale: deterministic import without relying on package names containing hyphens.
    """
    src_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "emoji_mood.py"
    spec = importlib.util.spec_from_file_location("emoji_mood", src_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

emoji_mood = load_emoji_mood_module()


class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_happy_mood(self):
        text = "What a day! 😄😀😁"
        self.assertEqual(emoji_mood.analyze_text(text), "happy")

    def test_sad_mood(self):
        text = "Feeling down... 😢😭"
        self.assertEqual(emoji_mood.analyze_text(text), "sad")

    def test_love_mood(self):
        text = "I love this! ❤️💖"
        self.assertEqual(emoji_mood.analyze_text(text), "love")

    def test_mixed_tie_breaker(self):
        # Two happy, two love -> tie, alphabetical order => "happy"
        text = "Great! 😄❤️😀💖"
        self.assertEqual(emoji_mood.analyze_text(text), "happy")

    def test_neutral_when_no_known_emoji(self):
        text = "Just plain text, no emojis."
        self.assertEqual(emoji_mood.analyze_text(text), "neutral")

    def test_unknown_emoji_ignored(self):
        # 🐍 is not in the map, should be ignored -> neutral
        text = "Python time 🐍"
        self.assertEqual(emoji_mood.analyze_text(text), "neutral")


if __name__ == "__main__":
    unittest.main()
