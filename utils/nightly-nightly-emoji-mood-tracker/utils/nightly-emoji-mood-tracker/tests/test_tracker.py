import unittest
from unittest.mock import patch
import datetime

# Import the module under test
from nightly_emoji_mood_tracker.src.tracker import generate_mood_calendar, _emoji_for_date, EMOJIS

class TestEmojiMoodTracker(unittest.TestCase):
    def test_generate_simple_range(self):
        # Simple 3‑day range – we only check length and ordering
        calendar = generate_mood_calendar("2023-01-01", "2023-01-03")
        self.assertEqual(len(calendar), 3)
        self.assertEqual([d for d, _ in calendar], ["2023-01-01", "2023-01-02", "2023-01-03"])
        # Ensure each emoji is from the predefined list
        for _, emoji in calendar:
            self.assertIn(emoji, EMOJIS)

    def test_start_after_end_raises(self):
        with self.assertRaises(ValueError):
            generate_mood_calendar("2023-01-10", "2023-01-01")

    def test_invalid_date_format_raises(self):
        with self.assertRaises(ValueError):
            generate_mood_calendar("2023/01/01", "2023-01-02")

    def test_emoji_determinism_with_mock(self):
        # Mock hashlib.sha256 to always return a digest of all zeros.
        # This forces the index to be 0, yielding the first emoji in EMOJIS.
        # Mock rationale: we want a fully deterministic, offline test without
        # relying on the actual hash implementation.
        class MockHash:
            def __init__(self, *args, **kwargs):
                pass
            def hexdigest(self):
                return "0" * 64  # 256‑bit zero digest

        with patch("nightly_emoji_mood_tracker.src.tracker.hashlib.sha256", MockHash):
            emoji = _emoji_for_date("2099-12-31")
            self.assertEqual(emoji, EMOJIS[0])
            calendar = generate_mood_calendar("2099-12-30", "2099-12-31")
            self.assertEqual(calendar, [("2099-12-30", EMOJIS[0]), ("2099-12-31", EMOJIS[0])])

if __name__ == "__main__":
    unittest.main()
