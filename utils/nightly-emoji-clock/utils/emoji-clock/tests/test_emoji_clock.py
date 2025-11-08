import unittest
from unittest.mock import patch
import datetime

# Import the function under test
from src.emoji_clock import get_emoji_time

class TestEmojiClock(unittest.TestCase):
    def test_midnight(self):
        # Mock rationale: ensure deterministic output without external time.
        fixed_dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
        with patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = fixed_dt
            mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
            self.assertEqual(get_emoji_time(), "🕛")

    def test_noon(self):
        fixed_dt = datetime.datetime(2023, 1, 1, 12, 30, 0)
        with patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = fixed_dt
            mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
            self.assertEqual(get_emoji_time(), "🕛")

    def test_afternoon(self):
        fixed_dt = datetime.datetime(2023, 1, 1, 15, 45, 0)
        with patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = fixed_dt
            mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
            self.assertEqual(get_emoji_time(), "🕒")

    def test_custom_datetime(self):
        # Directly pass a datetime without mocking.
        custom_dt = datetime.datetime(2023, 1, 1, 9, 0, 0)
        self.assertEqual(get_emoji_time(custom_dt), "🕘")

if __name__ == "__main__":
    unittest.main()
