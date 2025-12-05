import unittest
import sys
from unittest.mock import patch, MagicMock
import datetime
import pytz

# Import the main function from the utility
# Mock rationale: We need to import the module to test its functions.
# Since tamer.py calls sys.exit, we'll mock sys.exit in tests.
from src import tamer

class TestTemporalTangleTamer(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Capture stdout to check printed output.
        self.patcher_stdout = patch('sys.stdout', new_callable=MagicMock)
        self.mock_stdout = self.patcher_stdout.start()
        # Mock rationale: Capture stderr to check error messages.
        self.patcher_stderr = patch('sys.stderr', new_callable=MagicMock)
        self.mock_stderr = self.patcher_stderr.start()
        # Mock rationale: Prevent sys.exit from terminating the test runner.
        self.patcher_exit = patch('sys.exit')
        self.mock_exit = self.patcher_exit.start()

    def tearDown(self):
        self.patcher_stdout.stop()
        self.patcher_stderr.stop()
        self.patcher_exit.stop()

    def get_stdout_output(self):
        """Helper to get the printed output."""
        return self.mock_stdout.getvalue().strip()

    def get_stderr_output(self):
        """Helper to get the printed error output."""
        return self.mock_stderr.getvalue().strip()

    @patch('sys.argv', ['tamer.py', '--timestamp', '1678886400'])
    def test_epoch_to_default_iso_utc(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_not_called()
        self.assertEqual(self.get_stdout_output(), '2023-03-15T12:00:00+0000')

    @patch('sys.argv', ['tamer.py', '--timestamp', '2023-03-15T12:00:00Z', '--output-tz', 'America/Los_Angeles'])
    def test_iso_utc_to_la_time(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_not_called()
        self.assertEqual(self.get_stdout_output(), '2023-03-15T05:00:00-0700')

    @patch('sys.argv', [
        'tamer.py',
        '--timestamp', '2023-03-15 12:00:00',
        '--input-format', '%Y-%m-%d %H:%M:%S',
        '--input-tz', 'Europe/London',
        '--output-tz', 'Asia/Tokyo',
        '--output-format', '%Y/%m/%d %H:%M:%S %Z'
    ])
    def test_custom_string_london_to_tokyo_custom_format(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_not_called()
        self.assertEqual(self.get_stdout_output(), '2023/03/15 21:00:00 JST')

    @patch('sys.argv', [
        'tamer.py',
        '--timestamp', '2023-03-15T12:00:00+01:00', # ISO with offset
        '--output-tz', 'America/New_York'
    ])
    def test_iso_offset_to_new_york(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_not_called()
        self.assertEqual(self.get_stdout_output(), '2023-03-15T07:00:00-0400') # 12:00+01:00 is 11:00 UTC, NY is -0400, so 07:00

    @patch('sys.argv', [
        'tamer.py',
        '--timestamp', '2023-03-15 12:00:00',
        '--input-format', '%Y-%m-%d %H:%M:%S',
        '--input-tz', 'UTC',
        '--output-format', '%A, %B %d, %Y %H:%M:%S %Z'
    ])
    def test_custom_string_utc_to_custom_format(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_not_called()
        self.assertEqual(self.get_stdout_output(), 'Wednesday, March 15, 2023 12:00:00 UTC')

    @patch('sys.argv', ['tamer.py', '--timestamp', 'invalid-timestamp'])
    def test_invalid_timestamp_format(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Could not parse timestamp 'invalid-timestamp'", self.get_stderr_output())

    @patch('sys.argv', ['tamer.py', '--timestamp', '1678886400', '--output-tz', 'Invalid/TimeZone'])
    def test_invalid_output_timezone(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Unknown timezone specified: 'Invalid/TimeZone'", self.get_stderr_output())

    @patch('sys.argv', ['tamer.py', '--timestamp', '2023-03-15 12:00:00', '--input-format', '%Y-%m-%d %H:%M:%S', '--input-tz', 'Invalid/TimeZone'])
    def test_invalid_input_timezone(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Unknown timezone specified: 'Invalid/TimeZone'", self.get_stderr_output())

    @patch('sys.argv', ['tamer.py', '--timestamp', '2023-03-15 12:00:00', '--input-format', '%Y-%m-%d %H:%M:%S', '--output-format', '%Y-%m-%d %H:%M:%S %Z'])
    def test_default_input_tz_utc(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_not_called()
        self.assertEqual(self.get_stdout_output(), '2023-03-15 12:00:00 UTC')

    @patch('sys.argv', ['tamer.py', '--timestamp', '2023-03-15T12:00:00', '--input-tz', 'America/New_York', '--output-tz', 'Europe/Berlin'])
    def test_iso_no_tz_input_tz_specified(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_not_called()
        # 2023-03-15T12:00:00 in America/New_York is 2023-03-15T16:00:00 UTC
        # 2023-03-15T16:00:00 UTC in Europe/Berlin is 2023-03-15T17:00:00+0100 (CET)
        self.assertEqual(self.get_stdout_output(), '2023-03-15T17:00:00+0100')

    @patch('sys.argv', ['tamer.py', '--timestamp', '2023-03-15T12:00:00-05:00', '--output-tz', 'UTC'])
    def test_iso_with_offset_to_utc(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_not_called()
        self.assertEqual(self.get_stdout_output(), '2023-03-15T17:00:00+0000')

    @patch('sys.argv', ['tamer.py', '--timestamp', '1678886400', '--output-format', '%s'])
    def test_epoch_to_epoch_output(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_not_called()
        self.assertEqual(self.get_stdout_output(), '1678886400')

    @patch('sys.argv', ['tamer.py', '--timestamp', '2023-03-15T12:00:00Z', '--output-format', '%Y-%m-%d %H:%M:%S'])
    def test_iso_to_simple_format_no_tz_info(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_not_called()
        self.assertEqual(self.get_stdout_output(), '2023-03-15 12:00:00')

    @patch('sys.argv', ['tamer.py', '--timestamp', '2023-03-15T12:00:00', '--input-tz', 'UTC', '--output-tz', 'UTC'])
    def test_iso_no_tz_input_to_utc_output_utc(self):
        # Mock rationale: sys.argv is mocked to simulate command-line input.
        tamer.main()
        self.mock_exit.assert_not_called()
        self.assertEqual(self.get_stdout_output(), '2023-03-15T12:00:00+0000')


if __name__ == '__main__':
    unittest.main()
