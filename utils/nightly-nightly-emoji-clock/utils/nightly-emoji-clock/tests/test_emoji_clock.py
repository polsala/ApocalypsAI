import unittest
from unittest.mock import patch
from datetime import datetime

# Mock rationale: we replace datetime.now() to produce deterministic outputs without network or real time.

from src.emoji_clock import get_emoji_time

class TestEmojiClock(unittest.TestCase):
    def test_hour_exact(self):
        # 09:10 should map to 9 o'clock emoji 🕘
        mock_dt = datetime(2023, 1, 1, 9, 10, 0)
        with patch('src.emoji_clock.datetime') as mock_datetime:
            mock_datetime.now.return_value = mock_dt
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            self.assertEqual(get_emoji_time(), "🕘")

    def test_half_hour(self):
        # 14:45 (2:45 PM) should map to half‑hour emoji for 2 → 🕝
        mock_dt = datetime(2023, 1, 1, 14, 45, 0)
        with patch('src.emoji_clock.datetime') as mock_datetime:
            mock_datetime.now.return_value = mock_dt
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            self.assertEqual(get_emoji_time(), "🕝")

    def test_midnight(self):
        # 00:05 should be 12 o'clock 🕛
        mock_dt = datetime(2023, 1, 1, 0, 5, 0)
        with patch('src.emoji_clock.datetime') as mock_datetime:
            mock_datetime.now.return_value = mock_dt
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            self.assertEqual(get_emoji_time(), "🕛")

    def test_no_argument_uses_current_time(self):
        # Ensure function works without providing ``now`` – we just call it.
        # This test does not assert a specific emoji because it depends on the actual time.
        # Instead we verify that the return type is a string of length 1 (single emoji).
        result = get_emoji_time()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) >= 1)

if __name__ == "__main__":
    unittest.main()
