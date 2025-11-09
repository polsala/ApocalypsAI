import unittest
from unittest import mock
from datetime import datetime, time

# Mock rationale: we replace datetime.datetime.now() to return a deterministic time
# so the test does not depend on the actual system clock or any external service.

from utils.nightly_ascii_clock.src.clock import _render_time

class TestAsciiClock(unittest.TestCase):
    def test_render_specific_time(self):
        # Fixed time: 12:34
        fixed_time = time(12, 34)
        expected_output = (
            "  ┐   ┌─┐   •   ┌─┐ \n"
            "  │   │ │   •   │ │ \n"
            " ─┘   └─┘       └─┘ "
        )
        # The _render_time function works with datetime.time objects directly.
        result = _render_time(fixed_time)
        self.assertEqual(result, expected_output)

    @mock.patch('utils.nightly_ascii_clock.src.clock.datetime')
    def test_main_prints_correct_output(self, mock_datetime):
        # Mock datetime.datetime.now() to return 09:07
        mock_now = datetime(2025, 1, 1, 9, 7, 0)
        mock_datetime.datetime.now.return_value = mock_now
        mock_datetime.datetime.now.return_value.time.return_value = mock_now.time()
        # Capture stdout
        from io import StringIO
        import sys
        captured = StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = captured
        try:
            from utils.nightly_ascii_clock.src.clock import main
            main()
        finally:
            sys.stdout = sys_stdout_original
        output = captured.getvalue().strip().split('\n')
        # First line should be the numeric time
        self.assertEqual(output[0], "09:07")
        # Remaining lines should match the ASCII rendering for 09:07
        ascii_part = "\n".join(output[1:])
        expected_ascii = (
            " ──┐   ┌─┐   •   ──┐ \n"
            "   │   │ │   •     │ \n"
            "   │   └─┘       │ "
        )
        self.assertEqual(ascii_part, expected_ascii)

if __name__ == '__main__':
    unittest.main()
