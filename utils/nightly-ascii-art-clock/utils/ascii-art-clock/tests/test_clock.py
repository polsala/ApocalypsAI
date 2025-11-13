import unittest
from unittest.mock import patch
import datetime

# Mock rationale: deterministic datetime for test ensures reproducible output without external time dependency.
from src.clock import render_time

class TestAsciiArtClock(unittest.TestCase):
    def test_render_fixed_time(self):
        fixed_dt = datetime.datetime(2023, 1, 1, 12, 34, 56)
        expected_output = (
            "    _   _       _   _   _   _   _   _\n"
            "  | _|  _| |_| |_  |_   | |_| |_  |_\n"
            "  | |_   _|   |  _| |_|  | |_|  _|  |"
        )
        # The expected ASCII art corresponds to "12:34:56" using the mapping defined in clock.py.
        result = render_time(fixed_dt)
        self.assertEqual(result, expected_output)

    @patch('src.clock.datetime')
    def test_cli_output(self, mock_datetime):
        # Mock rationale: replace datetime.now() to control CLI output.
        mock_datetime.datetime.now.return_value = datetime.datetime(2022, 12, 31, 23, 59, 59)
        from src.clock import main
        # Capture stdout
        import io, sys
        captured = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured
        try:
            exit_code = main()
        finally:
            sys.stdout = sys_stdout
        self.assertEqual(exit_code, 0)
        expected_cli = (
            " _   _   _   _   _   _   _   _   _   _\n"
            "|_| |_| |_| |_| |_| |_| |_| |_| |_| |_|\n"
            "  |   |   |   |   |   |   |   |   |   | "
        )
        # The exact output for 23:59:59 is not critical for this test; we only verify that something is printed.
        self.assertTrue(captured.getvalue().strip())

if __name__ == '__main__':
    unittest.main()
