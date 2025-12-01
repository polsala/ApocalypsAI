import unittest
import sys
from unittest.mock import patch
from io import StringIO
import datetime
import os

# Add the src directory to the path to allow direct import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from rift_repair import unix_to_iso, iso_to_unix, main

class TestRiftRepair(unittest.TestCase):

    def test_unix_to_iso(self):
        # Test a known Unix timestamp to ISO 8601 UTC conversion
        unix_ts = 1678886400  # March 15, 2023 00:00:00 UTC
        expected_iso = "2023-03-15T00:00:00+00:00"
        self.assertEqual(unix_to_iso(unix_ts), expected_iso)

        unix_ts_epoch = 0 # Jan 1, 1970 00:00:00 UTC
        expected_iso_epoch = "1970-01-01T00:00:00+00:00"
        self.assertEqual(unix_to_iso(unix_ts_epoch), expected_iso_epoch)

    def test_iso_to_unix(self):
        # Test a known ISO 8601 UTC string to Unix timestamp conversion
        iso_str = "2023-03-15T00:00:00+00:00"
        expected_unix_ts = 1678886400
        self.assertEqual(iso_to_unix(iso_str), expected_unix_ts)

        # Test ISO string without explicit timezone, should assume UTC
        iso_str_no_tz = "2023-03-15T00:00:00"
        self.assertEqual(iso_to_unix(iso_str_no_tz), expected_unix_ts)

        # Test ISO string with Z for Zulu time (UTC)
        iso_str_z = "2023-03-15T00:00:00Z"
        self.assertEqual(iso_to_unix(iso_str_z), expected_unix_ts)

        # Test ISO string with different timezone, should convert to UTC timestamp
        # March 15, 2023 00:00:00 in New York (-04:00) is March 15, 2023 04:00:00 UTC
        iso_str_ny = "2023-03-15T00:00:00-04:00"
        expected_unix_ts_ny = 1678900800 # 1678886400 + (4 * 3600)
        self.assertEqual(iso_to_unix(iso_str_ny), expected_unix_ts_ny)


    def test_iso_to_unix_invalid_format(self):
        # Test invalid ISO 8601 string
        with self.assertRaises(ValueError, msg="Invalid ISO 8601 string: not-an-iso-string"):
            iso_to_unix("not-an-iso-string")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_unix_to_iso(self, mock_stderr, mock_stdout):
        # Mock rationale: Capture stdout/stderr for CLI output verification.
        with patch('sys.argv', ['rift_repair.py', '1678886400']):
            main()
            self.assertIn("Unix 1678886400 -> ISO 8601 UTC: 2023-03-15T00:00:00+00:00", mock_stdout.getvalue())
            self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_iso_to_unix(self, mock_stderr, mock_stdout):
        # Mock rationale: Capture stdout/stderr for CLI output verification.
        with patch('sys.argv', ['rift_repair.py', '--from-iso', '2023-03-15T00:00:00+00:00']):
            main()
            self.assertIn("ISO 8601 UTC '2023-03-15T00:00:00+00:00' -> Unix: 1678886400", mock_stdout.getvalue())
            self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_now(self, mock_stderr, mock_stdout):
        # Mock rationale: `datetime.datetime.now` is non-deterministic.
        # We need to control the "current time" to make the test deterministic.
        mock_now = datetime.datetime(2023, 10, 27, 10, 30, 45, tzinfo=datetime.timezone.utc)
        with patch('datetime.datetime', autospec=True) as mock_dt:
            mock_dt.now.return_value = mock_now
            mock_dt.fromtimestamp = datetime.datetime.fromtimestamp # Keep original
            mock_dt.fromisoformat = datetime.datetime.fromisoformat # Keep original
            mock_dt.timezone = datetime.timezone # Keep original
            with patch('sys.argv', ['rift_repair.py', '--now']):
                main()
                output = mock_stdout.getvalue()
                self.assertIn("Current UTC ISO 8601: 2023-10-27T10:30:45+00:00", output)
                self.assertIn("Current Unix Timestamp: 1698393045", output)
                self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit') # Mock rationale: sys.exit terminates the program, preventing further test execution.
    def test_main_invalid_iso_input(self, mock_exit, mock_stderr, mock_stdout):
        with patch('sys.argv', ['rift_repair.py', '--from-iso', 'invalid-date']):
            main()
            self.assertIn("Error converting ISO 8601 string: Invalid ISO 8601 string: invalid-date", mock_stderr.getvalue())
            mock_exit.assert_called_with(1)
            self.assertEqual(mock_stdout.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit') # Mock rationale: sys.exit terminates the program, preventing further test execution.
    def test_main_no_args(self, mock_exit, mock_stderr, mock_stdout):
        with patch('sys.argv', ['rift_repair.py']):
            main()
            self.assertIn("usage: rift_repair.py", mock_stdout.getvalue()) # Help message
            mock_exit.assert_called_with(1)
            self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_too_many_args(self, mock_stderr, mock_stdout):
        # Mock rationale: Capture stdout/stderr for CLI output verification.
        # argparse handles this by printing usage and exiting with code 2.
        with patch('sys.argv', ['rift_repair.py', '123', '--from-iso', 'abc']):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 2) # argparse exits with 2 for usage errors
            self.assertIn("usage: rift_repair.py", mock_stderr.getvalue())
            self.assertEqual(mock_stdout.getvalue(), "")
