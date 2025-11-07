import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we replace datetime.datetime.now() with a deterministic value
# so the test runs offline and is fully deterministic.

from utils.nightly-emoji-clock.src.emoji_clock import get_emoji_time

class TestEmojiClock(unittest.TestCase):
    def test_exact_hour(self):
        fixed_dt = datetime.datetime(2023, 1, 1, 9, 0)  # 09:00
        self.assertEqual(get_emoji_time(fixed_dt), "🕘")

    def test_half_hour(self):
        fixed_dt = datetime.datetime(2023, 1, 1, 14, 30)  # 14:30
        self.assertEqual(get_emoji_time(fixed_dt), "🕑⏺")

    def test_round_down(self):
        # 10:10 should round to 10:00 → 🕙
        fixed_dt = datetime.datetime(2023, 1, 1, 10, 10)
        self.assertEqual(get_emoji_time(fixed_dt), "🕙")

    def test_round_up_to_next_hour(self):
        # 22:50 rounds up to 23:00 → 🕙 (23 maps to 🕙)
        fixed_dt = datetime.datetime(2023, 1, 1, 22, 50)
        self.assertEqual(get_emoji_time(fixed_dt), "🕙")

    def test_midnight_transition(self):
        # 23:50 rounds up to 00:00 → 🕛
        fixed_dt = datetime.datetime(2023, 1, 1, 23, 50)
        self.assertEqual(get_emoji_time(fixed_dt), "🕛")

    @patch('utils.nightly-emoji-clock.src.emoji_clock.datetime.datetime')
    def test_cli_output(self, mock_datetime):
        # Mock datetime.now() for CLI test
        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 5, 30)
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        # Import the module inside the patched context
        from utils.nightly-emoji-clock.src import emoji_clock as ec
        # Capture stdout
        import io, sys
        captured = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured
        try:
            ec._cli()
        finally:
            sys.stdout = sys_stdout
        self.assertEqual(captured.getvalue().strip(), "🕔⏺")

if __name__ == "__main__":
    unittest.main()
