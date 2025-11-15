import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we replace datetime.datetime.now() to return a fixed timestamp
# so the test is deterministic and does not require network or real time.

from utils.nightly-emoji-clock.src.emoji_clock import get_emoji_time

class TestEmojiClock(unittest.TestCase):
    def test_fixed_time_midnight(self):
        fixed_dt = datetime.datetime(2023, 1, 1, 0, 0)  # 00:00
        with patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = fixed_dt
            mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
            result = get_emoji_time()
        self.assertEqual(result, "🕛 00")

    def test_fixed_time_afternoon(self):
        fixed_dt = datetime.datetime(2023, 1, 1, 15, 7)  # 15:07
        with patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = fixed_dt
            mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
            result = get_emoji_time()
        # 15 -> 3 PM -> 🕒 (since list repeats every 12 hours)
        self.assertEqual(result, "🕒 07")

    def test_explicit_now_parameter(self):
        dt = datetime.datetime(2023, 1, 1, 23, 59)
        result = get_emoji_time(now=dt)
        self.assertEqual(result, "🕚 59")

if __name__ == "__main__":
    unittest.main()
