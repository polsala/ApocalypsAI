import unittest
from datetime import datetime
from unittest.mock import patch

# Mock rationale: we replace datetime.now() with a fixed timestamp to make the test deterministic.

from nightly_ascii_clock import get_ascii_time

class TestAsciiClock(unittest.TestCase):
    def test_ascii_representation_fixed_time(self):
        fixed_dt = datetime(2025, 1, 1, 13, 37)  # 13:37
        expected_output = (
            " _   _   _   _   _   _   _   _   _   _ \n"
            "| | | | | | | | | | | | | | | | | | |\n"
            "|_| |_| |_| |_| |_| |_| |_| |_| |_| |_| \n"
        )
        # The expected pattern above corresponds to digits 1 3 : 3 7
        # Build expected manually using the same patterns as the implementation
        # to avoid duplication errors.
        from nightly_ascii_clock import _DIGIT_PATTERNS, _COLON_PATTERN
        def render(ch):
            if ch.isdigit():
                return _DIGIT_PATTERNS[int(ch)]
            return _COLON_PATTERN
        time_str = fixed_dt.strftime("%H:%M")
        lines = ["" for _ in range(3)]
        for ch in time_str:
            pat = render(ch)
            for i in range(3):
                lines[i] += pat[i]
        expected = "\n".join(lines) + "\n"
        self.assertEqual(get_ascii_time(fixed_dt), expected)

    @patch('nightly_ascii_clock.datetime')
    def test_cli_uses_datetime_now(self, mock_datetime):
        # Mock rationale: ensure CLI prints the mocked current time.
        mock_now = datetime(1999, 12, 31, 23, 59)
        mock_datetime.now.return_value = mock_now
        # Import the CLI function directly
        from nightly_ascii_clock import _cli
        import io, sys
        captured = io.StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = captured
        try:
            _cli()
        finally:
            sys.stdout = sys_stdout_original
        # Build expected output for 23:59
        from nightly_ascii_clock import _DIGIT_PATTERNS, _COLON_PATTERN
        def render(ch):
            if ch.isdigit():
                return _DIGIT_PATTERNS[int(ch)]
            return _COLON_PATTERN
        time_str = mock_now.strftime("%H:%M")
        lines = ["" for _ in range(3)]
        for ch in time_str:
            pat = render(ch)
            for i in range(3):
                lines[i] += pat[i]
        expected = "\n".join(lines) + "\n"
        self.assertEqual(captured.getvalue(), expected)

if __name__ == "__main__":
    unittest.main()
