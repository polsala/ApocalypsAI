import unittest
import sys
from io import StringIO
from unittest.mock import patch
from datetime import datetime, time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# Mock rationale:
# - sys.stdout: To capture print statements from CLI functions for verification.
# - sys.argv: To simulate command-line arguments for testing the main function.
# - datetime.now: To ensure deterministic date for meeting suggestions, as `datetime.now()` is non-deterministic.

# Import functions from the utility
from src.chronosync import list_timezones, convert_time, suggest_meeting_times, main

class TestChronosync(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    def test_list_timezones(self):
        list_timezones()
        output = self.mock_stdout.getvalue()
        self.assertIn("Available Time Zones (selection):", output)
        self.assertIn("- UTC", output)
        self.assertIn("- America/New_York", output)
        self.assertIn("- Europe/London", output)

    def test_convert_time_success(self):
        dt_str = "2024-07-20 10:00"
        from_tz = "America/New_York"
        to_tz = "Europe/London"
        expected_result = "2024-07-20 15:00 BST+0100" # New York 10 AM is London 3 PM in July (DST)
        result = convert_time(dt_str, from_tz, to_tz)
        self.assertEqual(result, expected_result)

        dt_str_utc = "2024-07-20 10:00"
        from_tz_utc = "UTC"
        to_tz_tokyo = "Asia/Tokyo"
        expected_result_tokyo = "2024-07-20 19:00 JST+0900" # UTC 10 AM is Tokyo 7 PM
        result_tokyo = convert_time(dt_str_utc, from_tz_utc, to_tz_tokyo)
        self.assertEqual(result_tokyo, expected_result_tokyo)

    def test_convert_time_invalid_timezone(self):
        dt_str = "2024-07-20 10:00"
        from_tz = "Invalid/Zone"
        to_tz = "Europe/London"
        with self.assertRaisesRegex(ValueError, "Invalid time zone specified"):
            convert_time(dt_str, from_tz, to_tz)

    def test_convert_time_invalid_datetime_format(self):
        dt_str = "2024/07/20 10:00" # Incorrect format
        from_tz = "America/New_York"
        to_tz = "Europe/London"
        with self.assertRaisesRegex(ValueError, "Invalid datetime format or value"):
            convert_time(dt_str, from_tz, to_tz)

    @patch('src.chronosync.datetime')
    def test_suggest_meeting_times_success(self, mock_datetime):
        # Mock rationale: Fix datetime.now() to ensure deterministic date for meeting suggestions.
        # This prevents tests from failing if run on a different day, as `today_utc` would change.
        mock_datetime.now.return_value = datetime(2024, 7, 20, 12, 0, 0, tzinfo=ZoneInfo("UTC"))
        mock_datetime.combine.side_effect = datetime.combine # Allow actual combine
        mock_datetime.strptime.side_effect = datetime.strptime # Allow actual strptime
        mock_datetime.time.side_effect = time # Allow actual time

        timezones = ["America/New_York", "Europe/London", "Asia/Tokyo"]
        suggestions = suggest_meeting_times(timezones)

        self.assertIn("09:00 UTC", suggestions)
        self.assertIn("13:00 UTC", suggestions)
        self.assertIn("17:00 UTC", suggestions)

        # Check 09:00 UTC slot
        slot_9_utc = suggestions["09:00 UTC"]
        self.assertIn("America/New_York", slot_9_utc)
        self.assertIn("Europe/London", slot_9_utc)
        self.assertIn("Asia/Tokyo", slot_9_utc)

        # 09:00 UTC is 05:00 AM in New York (July DST) -> outside working hours
        self.assertEqual(slot_9_utc["America/New_York"]["local_time"], "05:00 EDT-0400")
        self.assertFalse(slot_9_utc["America/New_York"]["is_working_hours"])

        # 09:00 UTC is 10:00 AM in London (July DST) -> inside working hours
        self.assertEqual(slot_9_utc["Europe/London"]["local_time"], "10:00 BST+0100")
        self.assertTrue(slot_9_utc["Europe/London"]["is_working_hours"])

        # 09:00 UTC is 18:00 (6 PM) in Tokyo (July DST) -> inside working hours (just barely)
        self.assertEqual(slot_9_utc["Asia/Tokyo"]["local_time"], "18:00 JST+0900")
        self.assertTrue(slot_9_utc["Asia/Tokyo"]["is_working_hours"])

        # Check 17:00 UTC slot
        slot_17_utc = suggestions["17:00 UTC"]
        # 17:00 UTC is 13:00 (1 PM) in New York (July DST) -> inside working hours
        self.assertEqual(slot_17_utc["America/New_York"]["local_time"], "13:00 EDT-0400")
        self.assertTrue(slot_17_utc["America/New_York"]["is_working_hours"])

        # 17:00 UTC is 18:00 (6 PM) in London (July DST) -> inside working hours
        self.assertEqual(slot_17_utc["Europe/London"]["local_time"], "18:00 BST+0100")
        self.assertTrue(slot_17_utc["Europe/London"]["is_working_hours"])

        # 17:00 UTC is 02:00 AM next day in Tokyo (July DST) -> outside working hours
        self.assertEqual(slot_17_utc["Asia/Tokyo"]["local_time"], "02:00 JST+0900") # Next day
        self.assertFalse(slot_17_utc["Asia/Tokyo"]["is_working_hours"])

    def test_suggest_meeting_times_empty_timezones(self):
        with self.assertRaisesRegex(ValueError, "At least one timezone must be provided."):
            suggest_meeting_times([])

    def test_suggest_meeting_times_invalid_timezone(self):
        timezones = ["America/New_York", "Invalid/Zone"]
        suggestions = suggest_meeting_times(timezones)
        self.assertIn("Invalid timezone", suggestions["09:00 UTC"]["Invalid/Zone"]["error"])

    @patch('sys.argv', ['chronosync.py', 'list'])
    def test_main_list_command(self):
        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Available Time Zones (selection):", output)

    @patch('sys.argv', ['chronosync.py', 'convert', '2024-07-20 10:00', 'America/New_York', 'Europe/London'])
    def test_main_convert_command_success(self):
        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Original: 2024-07-20 10:00 America/New_York", output)
        self.assertIn("Converted: 2024-07-20 15:00 BST+0100", output)

    @patch('sys.argv', ['chronosync.py', 'convert', '2024-07-20 10:00', 'Invalid/Zone', 'Europe/London'])
    @patch('sys.stderr', new_callable=StringIO) # Mock rationale: argparse prints errors to stderr
    def test_main_convert_command_error(self, mock_stderr):
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        output = self.mock_stdout.getvalue()
        self.assertIn("Error: Invalid time zone specified", output)

    @patch('sys.argv', ['chronosync.py', 'suggest', 'America/New_York', 'Europe/London'])
    @patch('src.chronosync.datetime')
    def test_main_suggest_command_success(self, mock_datetime):
        # Mock rationale: Fix datetime.now() for deterministic meeting suggestions.
        mock_datetime.now.return_value = datetime(2024, 7, 20, 12, 0, 0, tzinfo=ZoneInfo("UTC"))
        mock_datetime.combine.side_effect = datetime.combine
        mock_datetime.strptime.side_effect = datetime.strptime
        mock_datetime.time.side_effect = time

        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Meeting Time Suggestions", output)
        self.assertIn("--- If meeting starts at 09:00 UTC ---", output)
        self.assertIn("America/New_York: 05:00 EDT-0400 (❌ Outside Working Hours)", output)
        self.assertIn("Europe/London: 10:00 BST+0100 (✅ Working Hours)", output)

    @patch('sys.argv', ['chronosync.py', 'suggest']) # Missing timezones
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_suggest_command_missing_args(self, mock_stderr):
        with self.assertRaises(SystemExit) as cm:
            main()
        # argparse exits with 2 for argument errors
        self.assertEqual(cm.exception.code, 2)
        self.assertIn("the following arguments are required: timezones", mock_stderr.getvalue())
