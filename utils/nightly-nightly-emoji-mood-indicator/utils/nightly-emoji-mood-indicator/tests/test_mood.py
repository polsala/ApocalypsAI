import unittest
from src.mood import get_mood_emoji

class TestMoodEmoji(unittest.TestCase):
    def test_valid_scores(self):
        expected = {
            1: "😞",
            2: "☹️",
            3: "😐",
            4: "🙂",
            5: "😁",
        }
        for score, emoji in expected.items():
            with self.subTest(score=score):
                self.assertEqual(get_mood_emoji(score), emoji)

    def test_invalid_score(self):
        # Mock rationale: ensure function raises for out‑of‑range values without external calls.
        with self.assertRaises(ValueError):
            get_mood_emoji(0)
        with self.assertRaises(ValueError):
            get_mood_emoji(6)

if __name__ == "__main__":
    unittest.main()
