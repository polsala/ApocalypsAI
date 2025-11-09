import unittest
from unittest.mock import patch
import datetime

# Mock rationale: We replace ``datetime.datetime.now`` with a fixed timestamp so the test is deterministic and does not depend on the actual system clock.

from src.clock import get_ascii_time, _render_time_str

class TestAsciiClock(unittest.TestCase):
    def test_render_simple_time(self):
        # Verify that the internal renderer produces the expected line count and characters.
        rendered = _render_time_str("12:34")
        lines = rendered.split("\n")
        self.assertEqual(len(lines), 5)  # 5 lines per digit art
        # Spot‑check a few characters to ensure mapping works.
        self.assertIn("█", lines[0])
        self.assertIn(":", rendered)  # colon should be present

    @patch('src.clock.datetime')
    def test_get_ascii_time_with_mocked_now(self, mock_datetime):
        # Mock datetime.datetime.now() to return a known time.
        fixed_dt = datetime.datetime(2023, 1, 1, 9, 5)  # 09:05
        mock_datetime.datetime.now.return_value = fixed_dt
        mock_datetime.datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        # The function under test uses ``datetime.datetime.now()`` internally.
        ascii_art = get_ascii_time(fixed_dt)
        # Expected representation for "09:05"
        expected = (
            " ███   ███   ░   ███   ███ \n"
            "█   █     █  ░  █    █   █\n"
            "█   █   ███  ░   ███  ███ \n"
            "█   █  █    ░  ░     █    █\n"
            " ███   ███   ░   ███   ███ "
        )
        # Normalise whitespace for comparison.
        self.assertEqual(ascii_art.replace(" ", ""), expected.replace(" ", ""))

if __name__ == "__main__":
    unittest.main()
