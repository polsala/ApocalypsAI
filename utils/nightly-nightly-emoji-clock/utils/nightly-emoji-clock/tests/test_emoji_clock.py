import datetime
import unittest
from unittest.mock import patch

# Mock rationale: ensure deterministic `datetime.datetime.now()` without network.
from utils.nightly-emoji-clock.src.emoji_clock import get_emoji_time


class TestEmojiClock(unittest.TestCase):
    def test_midnight(self):
        fake_now = datetime.datetime(2023, 1, 1, 0, 0, 0)
        with patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = fake_now
            # Preserve the constructor for datetime objects used inside the module
            mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
            self.assertEqual(get_emoji_time(), "🕛")

    def test_afternoon(self):
        fake_now = datetime.datetime(2023, 1, 1, 15, 30, 0)  # 3 PM
        with patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = fake_now
            mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
            self.assertEqual(get_emoji_time(), "🕒")

    def test_explicit_dt(self):
        dt = datetime.datetime(2023, 1, 1, 22, 0, 0)  # 10 PM
        self.assertEqual(get_emoji_time(dt), "🕙")


if __name__ == "__main__":
    unittest.main()
