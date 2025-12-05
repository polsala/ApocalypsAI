import unittest
from datetime import datetime
from unittest.mock import patch

from src.emoji_clock import get_clock_emoji

class TestEmojiClock(unittest.TestCase):
    def test_mapping(self):
        cases = [
            (datetime(2023, 1, 1, 0, 0), "🕛"),   # midnight
            (datetime(2023, 1, 1, 1, 15), "🕐"),
            (datetime(2023, 1, 1, 12, 30), "🕛"), # noon
            (datetime(2023, 1, 1, 13, 45), "🕐"),
            (datetime(2023, 1, 1, 23, 59), "🕚"),
        ]
        for dt, expected in cases:
            with self.subTest(dt=dt):
                self.assertEqual(get_clock_emoji(dt), expected)

    @patch("src.emoji_clock.datetime")
    def test_cli_output(self, mock_datetime):
        # Mock datetime.now() to a fixed time (14:00 -> 2 o’clock)
        mock_datetime.now.return_value = datetime(2023, 1, 1, 14, 0)
        # Import the module after patching
        import src.emoji_clock as emoji_clock
        # Capture stdout
        import io, sys
        captured = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured
        try:
            emoji_clock._cli()
        finally:
            sys.stdout = sys_stdout
        self.assertEqual(captured.getvalue().strip(), "🕑")  # 14 % 12 = 2

if __name__ == "__main__":
    unittest.main()
