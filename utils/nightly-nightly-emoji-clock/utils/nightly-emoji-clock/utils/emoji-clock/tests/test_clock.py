import unittest
from unittest.mock import patch
from datetime import datetime

from src.clock import get_emoji_clock

class TestEmojiClock(unittest.TestCase):
    def test_default_midnight(self):
        # Mock rationale: ensure deterministic output when datetime.now() is midnight.
        with patch('src.clock.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2023, 1, 1, 0, 0)
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
            self.assertEqual(get_emoji_clock(), "🕛 00m")

    def test_default_afternoon(self):
        # Mock rationale: test hour conversion (13 -> 🕐) and minute formatting.
        with patch('src.clock.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2023, 1, 1, 13, 7)
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
            self.assertEqual(get_emoji_clock(), "🕐 07m")

    def test_explicit_datetime(self):
        # Mock rationale: verify function works with an explicit datetime argument.
        dt = datetime(2023, 1, 1, 23, 45)
        self.assertEqual(get_emoji_clock(dt), "🕚 45m")

if __name__ == "__main__":
    unittest.main()
