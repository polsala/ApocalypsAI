import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we replace datetime.datetime.now() with a deterministic value
# so the test does not depend on the actual system clock.

from src.clock import get_ascii_time

class TestAsciiClock(unittest.TestCase):
    def test_ascii_render_midnight(self):
        dt = datetime.datetime(2023, 1, 1, 0, 0)
        expected = (
            " _   _   _ \n"
            "| | | | | |\n"
            "|_| |_| |_|"
        )
        self.assertEqual(get_ascii_time(dt), expected)

    def test_ascii_render_random_time(self):
        dt = datetime.datetime(2023, 1, 1, 14, 35)
        expected = (
            " _   _       _   _ \n"
            "| | | |  _  | | | |\n"
            "|_| |_| |_| |_| |_|"
        )
        self.assertEqual(get_ascii_time(dt), expected)

    @patch('src.clock.datetime')
    def test_cli_uses_mocked_now(self, mock_datetime):
        # Mock rationale: ensure the CLI prints a known value without real time.
        mock_now = datetime.datetime(2022, 12, 31, 23, 59)
        mock_datetime.datetime.now.return_value = mock_now
        mock_datetime.datetime.strptime = datetime.datetime.strptime
        mock_datetime.datetime.strftime = datetime.datetime.strftime
        # Import the CLI entry point lazily to pick up the patched datetime.
        from src import clock as cli_module
        # Capture stdout
        from io import StringIO
        import sys
        captured = StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = captured
        try:
            cli_module.main([])
        finally:
            sys.stdout = sys_stdout_original
        output = captured.getvalue().strip()
        expected = (
            " _   _   _   _   _   _   _   _   _   _ \n"
            "|_| |_| |_| |_| |_| |_| |_| |_| |_| |_|\n"
            " _   _   _   _   _   _   _   _   _   _"
        )
        # The expected string corresponds to "23:59" rendered in ASCII.
        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
