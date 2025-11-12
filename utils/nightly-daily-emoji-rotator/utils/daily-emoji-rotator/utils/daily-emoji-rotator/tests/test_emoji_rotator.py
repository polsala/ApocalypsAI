import datetime
import unittest
from unittest.mock import patch

# Mock rationale: We patch ``datetime.date.today`` to control the current date without
# touching the system clock, ensuring deterministic offline tests.

from daily_emoji_rotator import get_today_emoji, get_emoji_for_date

class TestEmojiRotator(unittest.TestCase):
    def test_known_date(self):
        # 2025-01-01 is a known reference date.
        test_date = datetime.date(2025, 1, 1)
        emoji = get_emoji_for_date(test_date)
        # Compute expected emoji using the same algorithm (hard‑coded for stability).
        # The expected value was generated once and is now fixed.
        expected = "🚀"  # This value corresponds to the hash of 2025-01-01.
        self.assertEqual(emoji, expected)

    def test_today_emoji_mocked(self):
        mock_date = datetime.date(2023, 12, 25)
        with patch.object(datetime.date, "today", return_value=mock_date):
            emoji = get_today_emoji()
            expected = get_emoji_for_date(mock_date)
            self.assertEqual(emoji, expected)

if __name__ == "__main__":
    unittest.main()
