import unittest
from unittest.mock import patch, MagicMock
import datetime
import sys
from io import StringIO

# Mock rationale: We need to control the 'current' time to ensure deterministic test results.
# datetime.datetime.now() is mocked to return a fixed UTC time.
# sys.stdout is mocked to capture printed output for verification.
# sys.stderr is mocked to capture warnings/errors for verification.

class TestChronosChime(unittest.TestCase):

    # Fixed UTC time for all tests
    MOCKED_UTC_NOW = datetime.datetime(2023, 10, 27, 10, 30, 0, tzinfo=datetime.timezone.utc)

    @patch('datetime.datetime')
    def test_get_current_times_in_timezones_basic(self, mock_datetime):
        # Mock rationale: Fixes the 'current' time for deterministic testing.
        mock_datetime.now.return_value = self.MOCKED_UTC_NOW
        mock_datetime.timezone = datetime.timezone # Ensure timezone attribute is available
        mock_datetime.datetime = datetime.datetime # Ensure datetime class is available for isinstance checks

        # Dynamically import the module to ensure patches apply correctly
        # This assumes the test runner sets up sys.path or the module is discoverable.
        # For self-contained utility, we assume `src/chronos_chime.py` is accessible.
        # A more robust way for tests in `tests/` to import from `src/` would be to modify `sys.path`.
        # For this context, we'll use a direct import assuming the test environment handles it.
        import chronos_chime

        timezones = ["America/New_York", "Europe/London"]
        times = chronos_chime.get_current_times_in_timezones(timezones)

        self.assertIn("UTC", times)
        self.assertIn("America/New_York", times)
        self.assertIn("Europe/London", times)

        self.assertEqual(times["UTC"], self.MOCKED_UTC_NOW)

        # Expected times based on MOCKED_UTC_NOW
        # America/New_York is UTC-4 during DST (Oct 27, 2023)
        expected_ny = datetime.datetime(2023, 10, 27, 6, 30, 0)
        self.assertEqual(times["America/New_York"].replace(tzinfo=None), expected_ny)
        self.assertEqual(times["America/New_York"].tzinfo.utcoffset(times["America/New_York"]), datetime.timedelta(hours=-4))

        # Europe/London is UTC+1 during BST (Oct 27, 2023)
        expected_london = datetime.datetime(2023, 10, 27, 11, 30, 0)
        self.assertEqual(times["Europe/London"].replace(tzinfo=None), expected_london)
        self.assertEqual(times["Europe/London"].tzinfo.utcoffset(times["Europe/London"]), datetime.timedelta(hours=1))

    @patch('datetime.datetime')
    @patch('sys.stderr', new_callable=StringIO)
    def test_get_current_times_in_timezones_invalid(self, mock_stderr, mock_datetime):
        # Mock rationale: Fixes the 'current' time and captures stderr output.
        mock_datetime.now.return_value = self.MOCKED_UTC_NOW
        mock_datetime.timezone = datetime.timezone
        mock_datetime.datetime = datetime.datetime

        import chronos_chime

        timezones = ["Invalid/Timezone", "Europe/London"]
        times = chronos_chime.get_current_times_in_timezones(timezones)

        self.assertIn("UTC", times)
        self.assertNotIn("Invalid/Timezone", times)
        self.assertIn("Europe/London", times)
        self.assertIn("Warning: Timezone 'Invalid/Timezone' not found. Skipping.", mock_stderr.getvalue())

    @patch('datetime.datetime')
    def test_format_time_output(self, mock_datetime):
        # Mock rationale: Fixes the 'current' time for deterministic formatting.
        mock_datetime.now.return_value = self.MOCKED_UTC_NOW
        mock_datetime.timezone = datetime.timezone
        mock_datetime.datetime = datetime.datetime

        import chronos_chime
        from zoneinfo import ZoneInfo

        # Manually create datetime objects with ZoneInfo for consistent testing
        # Note: ZoneInfo objects are loaded from system data, so we rely on their correctness
        # for the actual offset values, but the *logic* of formatting is tested.
        ny_tz = ZoneInfo("America/New_York")
        london_tz = ZoneInfo("Europe/London")
        tokyo_tz = ZoneInfo("Asia/Tokyo")
        sydney_tz = ZoneInfo("Australia/Sydney")

        mock_times = {
            "UTC": self.MOCKED_UTC_NOW,
            "America/New_York": self.MOCKED_UTC_NOW.astimezone(ny_tz),
            "Europe/London": self.MOCKED_UTC_NOW.astimezone(london_tz),
            "Asia/Tokyo": self.MOCKED_UTC_NOW.astimezone(tokyo_tz),
            "Australia/Sydney": self.MOCKED_UTC_NOW.astimezone(sydney_tz)
        }

        output = chronos_chime.format_time_output(mock_times)

        expected_output_lines = [
            "--- Chronos-Chime Temporal Scan ---",
            "UTC: 2023-10-27T10:30+00:00",
            "",
            "America/New_York: 2023-10-27T06:30-04:00 (Offset: -04:00)",
            "Asia/Tokyo:       2023-10-27T19:30+09:00 (Offset: +09:00)",
            "Australia/Sydney: 2023-10-27T21:30+11:00 (Offset: +11:00)",
            "Europe/London:    2023-10-27T11:30+01:00 (Offset: +01:00)"
        ]
        # The format_time_output sorts by timezone name, so the expected order should be consistent.
        self.assertEqual(output.strip(), "\n".join(expected_output_lines).strip())

    @patch('sys.argv', ['chronos_chime.py', 'America/New_York', 'Europe/London'])
    @patch('datetime.datetime')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_args(self, mock_stdout, mock_datetime):
        # Mock rationale: Mocks command-line arguments, fixes current time, and captures stdout.
        mock_datetime.now.return_value = self.MOCKED_UTC_NOW
        mock_datetime.timezone = datetime.timezone
        mock_datetime.datetime = datetime.datetime

        # Import and run main function
        import chronos_chime
        chronos_chime.main()

        output = mock_stdout.getvalue()
        self.assertIn("America/New_York", output)
        self.assertIn("Europe/London", output)
        self.assertNotIn("Asia/Tokyo", output) # Should not contain default if args are provided

    @patch('sys.argv', ['chronos_chime.py'])
    @patch('datetime.datetime')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_without_args(self, mock_stdout, mock_datetime):
        # Mock rationale: Mocks command-line arguments (empty), fixes current time, and captures stdout.
        mock_datetime.now.return_value = self.MOCKED_UTC_NOW
        mock_datetime.timezone = datetime.timezone
        mock_datetime.datetime = datetime.datetime

        # Import and run main function
        import chronos_chime
        chronos_chime.main()

        output = mock_stdout.getvalue()
        self.assertIn("America/New_York", output)
        self.assertIn("Europe/London", output)
        self.assertIn("Asia/Tokyo", output) # Should contain default timezones
        self.assertIn("Australia/Sydney", output)

if __name__ == '__main__':
    unittest.main()
