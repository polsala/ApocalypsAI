import datetime
import unittest
from unittest import mock

# Mock rationale: All tests are deterministic and offline; we mock datetime.date.today()
# to ensure consistent output regardless of when the test suite runs.

from src.emoji_mood_tracker import mood_for_date, mood_for_range

class TestEmojiMoodTracker(unittest.TestCase):
    def test_mood_for_known_date(self):
        # 2023-01-01 is a fixed reference date.
        date = datetime.date(2023, 1, 1)
        emoji = mood_for_date(date)
        # The expected emoji is derived from the algorithm; compute once.
        expected = "🤔"  # Determined by running the function once.
        self.assertEqual(emoji, expected)

    def test_mood_range_order(self):
        start = datetime.date(2023, 1, 1)
        end = datetime.date(2023, 1, 3)
        result = mood_for_range(start, end)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][0], start)
        self.assertEqual(result[-1][0], end)
        # Verify deterministic emojis for each day.
        expected_emojis = ["🤔", "🌈", "⚡"]
        self.assertEqual([e[1] for e in result], expected_emojis)

    @mock.patch("src.emoji_mood_tracker.datetime.date")
    def test_default_today_uses_mocked_date(self, mock_date):
        # Mock datetime.date.today() to return a known date.
        mock_date.today.return_value = datetime.date(2022, 12, 25)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        emoji = mood_for_date(datetime.date.today())
        expected = "🌟"  # Determined by the algorithm for 2022-12-25.
        self.assertEqual(emoji, expected)

    def test_invalid_range_raises(self):
        start = datetime.date(2023, 5, 10)
        end = datetime.date(2023, 5, 5)
        with self.assertRaises(ValueError):
            mood_for_range(start, end)

if __name__ == "__main__":
    unittest.main()
