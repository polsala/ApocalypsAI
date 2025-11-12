import unittest
from utils.emoji_mood_analyzer.src.analyzer import get_mood_emoji

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_happy_keywords(self):
        self.assertEqual(get_mood_emoji("I love this new feature!"), "😄")
        self.assertEqual(get_mood_emoji("What a fantastic day"), "😄")

    def test_sad_keywords(self):
        self.assertEqual(get_mood_emoji("I am feeling sad today"), "😢")
        self.assertEqual(get_mood_emoji("This is terrible"), "😢")

    def test_angry_keywords(self):
        self.assertEqual(get_mood_emoji("I am so angry about the bug"), "😠")
        self.assertEqual(get_mood_emoji("This makes me mad"), "😠")

    def test_surprised_keywords(self):
        self.assertEqual(get_mood_emoji("Wow, that was unexpected!"), "😲")
        self.assertEqual(get_mood_emoji("I am shocked by the result"), "😲")

    def test_neutral_when_no_match(self):
        self.assertEqual(get_mood_emoji("Just a regular update"), "😐")
        self.assertEqual(get_mood_emoji(""), "😐")

    def test_case_insensitivity(self):
        self.assertEqual(get_mood_emoji("I LOVE this"), "😄")
        self.assertEqual(get_mood_emoji("i am SAD"), "😢")

# Mock rationale: No external services are called; tests are fully deterministic.

if __name__ == "__main__":
    unittest.main()
