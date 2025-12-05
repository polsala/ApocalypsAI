import unittest
from unittest.mock import patch
import datetime
import io
import sys

# Import the function to be tested
from src.reminder import check_for_snack_time, get_snack_message, SNACK_TIMES

class TestSnackReminder(unittest.TestCase):

    @patch('datetime.datetime')
    def test_snack_time_triggers_reminder(self, mock_datetime):
        # Mock rationale: We need to control the current time to deterministically
        # test if the reminder triggers at a specific snack time.
        # We patch datetime.datetime to return a fixed time.

        # Set the mock current time to one of the defined SNACK_TIMES
        test_hour, test_minute = SNACK_TIMES[0] # Use the first snack time for testing
        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, test_hour, test_minute, 0)

        # Capture stdout to check the printed message
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Run the function
        result = check_for_snack_time()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Assertions
        self.assertTrue(result, "Should return True when a snack time is hit.")
        self.assertIn(get_snack_message(), captured_output.getvalue(), "Should print the snack reminder message.")

    @patch('datetime.datetime')
    def test_non_snack_time_does_not_trigger_reminder(self, mock_datetime):
        # Mock rationale: Similar to the above, we need to ensure the reminder
        # does NOT trigger when the time is outside the defined snack windows.
        # We patch datetime.datetime to return a fixed time that is not a snack time.

        # Set the mock current time to a time that is NOT a snack time
        # Ensure it's not close to any snack time to avoid edge case issues
        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 9, 0, 0) # 9:00 AM, not a snack time

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Run the function
        result = check_for_snack_time()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Assertions
        self.assertFalse(result, "Should return False when not a snack time.")
        self.assertEqual(captured_output.getvalue(), "", "Should print nothing when not a snack time.")

    @patch('datetime.datetime')
    def test_time_just_before_snack_time_does_not_trigger(self, mock_datetime):
        # Mock rationale: Test edge cases to ensure precision.
        # Verify that a time just before a snack time does not trigger.
        test_hour, test_minute = SNACK_TIMES[0]
        # Set time to one minute before the snack time
        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, test_hour, test_minute - 1, 0)

        captured_output = io.StringIO()
        sys.stdout = captured_output

        result = check_for_snack_time()

        sys.stdout = sys.__stdout__

        self.assertFalse(result, "Should not trigger just before snack time.")
        self.assertEqual(captured_output.getvalue(), "", "Should print nothing just before snack time.")

    @patch('datetime.datetime')
    def test_time_just_after_snack_time_does_not_trigger(self, mock_datetime):
        # Mock rationale: Test edge cases to ensure precision.
        # Verify that a time just after a snack time does not trigger.
        test_hour, test_minute = SNACK_TIMES[0]
        # Set time to one minute after the snack time
        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, test_hour, test_minute + 1, 0)

        captured_output = io.StringIO()
        sys.stdout = captured_output

        result = check_for_snack_time()

        sys.stdout = sys.__stdout__

        self.assertFalse(result, "Should not trigger just after snack time.")
        self.assertEqual(captured_output.getvalue(), "", "Should print nothing just after snack time.")

    def test_get_snack_message_determinism(self):
        # Mock rationale: Ensure get_snack_message is deterministic as per current implementation.
        # No mock needed, directly test the function.
        message = get_snack_message()
        self.assertIsInstance(message, str)
        self.assertIn("APOCALYPSE ALERT", message)
        self.assertEqual(message, "🚨 APOCALYPSE ALERT! 🚨 Your internal energy reserves are critically low! Time for a tactical snack deployment! Go forth and refuel!")
