import unittest
from src.logger import get_mood_emoji

class TestMoodEmoji(unittest.TestCase):
    def test_happy_keywords(self):
        text = "I am feeling great and awesome today!"
        self.assertEqual(get_mood_emoji(text), "😄")

    def test_sad_keywords(self):
        text = "It was a terrible, sad day."
        self.assertEqual(get_mood_emoji(text), "😢")

    def test_angry_keywords(self):
        text = "I'm mad and irritated by the bug."
        self.assertEqual(get_mood_emoji(text), "😠")

    def test_surprised_keywords(self):
        text = "Wow! That was astonishing."
        self.assertEqual(get_mood_emoji(text), "😲")

    def test_neutral_when_no_match(self):
        text = "Just a regular update with no emotion."
        self.assertEqual(get_mood_emoji(text), "😐")

    def test_tie_breaker_respects_order(self):
        # Both happy and sad keywords appear once; happy is earlier in _MOOD_MAP.
        text = "I am glad but also sad."
        self.assertEqual(get_mood_emoji(text), "😄")

    # Mock rationale example (no external calls, but placeholder for future extension)
    def test_mock_external_sentiment(self):
        # Mock rationale: if we later replace the simple keyword engine with an
        # external sentiment API, we would mock its response here.
        # For now, the function is deterministic and offline.
        self.assertTrue(True)  # placeholder assertion

if __name__ == "__main__":
    unittest.main()
