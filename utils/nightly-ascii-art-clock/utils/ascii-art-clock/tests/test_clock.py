import unittest
from unittest.mock import patch
from datetime import datetime

# Mock rationale: we replace datetime.now() with a fixed value so the test is deterministic and offline.

from utils.ascii-art-clock.src.clock import render_time


class TestAsciiArtClock(unittest.TestCase):
    def test_render_specific_time(self):
        fixed_dt = datetime(2023, 1, 1, 14, 5)  # 14:05
        expected_output = (
            " ███   ███   ███   ███   ███   ███\n"
            "█   █  █   █  █   █  █   █  █   █  █   █\n"
            "█   █      █  ███   ███   ███   ███   ███\n"
            "█   █  █   █  █       █      █  █   █  █   █\n"
            " ███   ███   ███   ███   ███   ███   ███"
        )
        # The expected string is built manually based on the digit art mapping.
        result = render_time(fixed_dt)
        self.assertEqual(result, expected_output)

    @patch('utils.ascii-art-clock.src.clock.datetime')
    def test_cli_uses_current_time(self, mock_datetime):
        # Mock datetime.now() to return a known value.
        mock_datetime.now.return_value = datetime(2022, 12, 31, 23, 59)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        # Import the CLI function directly.
        from utils.ascii-art-clock.src.clock import _cli
        # Capture stdout.
        from io import StringIO
        import sys
        captured = StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured
        try:
            _cli()
        finally:
            sys.stdout = sys_stdout
        output = captured.getvalue().strip()
        # Verify that the output matches the rendered 23:59.
        expected = render_time(datetime(2022, 12, 31, 23, 59))
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
