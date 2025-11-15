import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path to allow importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from timezone_converter import convert_timezone, main

class TestTimezoneConverter(unittest.TestCase):

    def test_convert_timezone_basic(self):
        # Test conversion from New York to London
        # 2024-10-27 10:00:00 EDT (UTC-4) -> 2024-10-27 15:00:00 BST (UTC+1)
        # Note: BST ends on Oct 27, 2024, at 02:00, so 10:00 EDT is 15:00 BST
        result = convert_timezone("2024-10-27 10:00:00", "America/New_York", "Europe/London")
        self.assertEqual(result, "2024-10-27 15:00:00 BST+0100")

    def test_convert_timezone_different_day(self):
        # Test conversion crossing midnight
        # 2024-10-27 23:00:00 PDT (UTC-7) -> 2024-10-28 15:00:00 JST (UTC+9)
        result = convert_timezone("2024-10-27 23:00:00", "America/Los_Angeles", "Asia/Tokyo")
        self.assertEqual(result, "2024-10-28 15:00:00 JST+0900")

    def test_convert_timezone_same_timezone(self):
        # Test conversion to the same timezone
        result = convert_timezone("2024-01-15 12:00:00", "Europe/Berlin", "Europe/Berlin")
        self.assertEqual(result, "2024-01-15 12:00:00 CET+0100")

    def test_invalid_datetime_format(self):
        # Test with an unparseable datetime string
        with self.assertRaisesRegex(ValueError, "Could not parse datetime string"):
            convert_timezone("invalid-date-time", "America/New_York", "Europe/London")

    def test_unknown_from_timezone(self):
        # Test with an unknown source timezone
        with self.assertRaisesRegex(ValueError, "Unknown timezone"):
            convert_timezone("2024-10-27 10:00:00", "Unknown/Timezone", "Europe/London")

    def test_unknown_to_timezone(self):
        # Test with an unknown target timezone
        with self.assertRaisesRegex(ValueError, "Unknown timezone"):
            convert_timezone("2024-10-27 10:00:00", "America/New_York", "Unknown/Timezone")

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_success(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: We mock argparse.ArgumentParser.parse_args to control CLI input without affecting actual sys.argv.
        # We mock sys.stdout and sys.stderr to capture printed output without affecting the console.
        # We mock sys.exit to prevent the test from terminating the runner prematurely.
        mock_parse_args.return_value = MagicMock(
            datetime="2024-03-10 01:00:00", # Before DST change in NY
            from_tz="America/New_York",
            to_tz="Europe/Berlin"
        )
        main()
        mock_stdout.assert_any_call("Input: 2024-03-10 01:00:00 America/New_York")
        mock_stdout.assert_any_call("Output: 2024-03-10 07:00:00 CET+0100")
        mock_exit.assert_not_called()

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_error_invalid_datetime(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Same as above, to control CLI input and capture output/exit calls.
        mock_parse_args.return_value = MagicMock(
            datetime="bad-date",
            from_tz="America/New_York",
            to_tz="Europe/Berlin"
        )
        main()
        mock_stderr.assert_called_once_with(unittest.mock.ANY) # Check if stderr was called
        self.assertIn("Error: Datetime conversion error: Could not parse datetime string", mock_stderr.call_args[0][0])
        mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_error_unknown_timezone(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Same as above, to control CLI input and capture output/exit calls.
        mock_parse_args.return_value = MagicMock(
            datetime="2024-10-27 10:00:00",
            from_tz="Invalid/Timezone",
            to_tz="Europe/Berlin"
        )
        main()
        mock_stderr.assert_called_once_with(unittest.mock.ANY)
        self.assertIn("Error: Unknown timezone: 'Invalid/Timezone'", mock_stderr.call_args[0][0])
        mock_exit.assert_called_once_with(1)

    @patch('sys.stderr', new_callable=MagicMock)
    @patch('sys.exit')
    def test_pytz_import_error(self, mock_exit, mock_stderr):
        # Mock rationale: Simulate a scenario where pytz is not installed.
        # We temporarily remove 'pytz' from sys.modules and then re-import the module
        # to trigger the ImportError handling logic.
        original_pytz = sys.modules.get('pytz')
        if 'pytz' in sys.modules:
            del sys.modules['pytz']

        # Clear the module cache for timezone_converter to force re-import
        if 'timezone_converter' in sys.modules:
            del sys.modules['timezone_converter']

        with patch.dict('sys.modules', {'pytz': None}): # This makes 'import pytz' fail
            # Re-import the module to trigger the error handling
            import importlib
            with self.assertRaises(SystemExit) as cm:
                importlib.import_module('timezone_converter')
            
            self.assertEqual(cm.exception.code, 1)
            mock_stderr.assert_called_once_with("Error: 'pytz' library not found. Please install it using 'pip install pytz'.", file=sys.stderr)
            mock_exit.assert_called_once_with(1)
        
        # Restore pytz if it was originally present
        if original_pytz:
            sys.modules['pytz'] = original_pytz
        if 'timezone_converter' in sys.modules:
            del sys.modules['timezone_converter'] # Clean up for other tests
        importlib.import_module('timezone_converter') # Re-import for subsequent tests
