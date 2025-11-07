import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import sys
from io import StringIO

# Import the function to test
from src.countdown import calculate_countdown, main

class TestCountdown(unittest.TestCase):

    @patch('src.countdown.datetime') # Mock rationale: Patching datetime to control the 'now' value for deterministic tests.
    def test_future_countdown(self, mock_datetime):
        # Set a fixed 'now' for the test
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        # Ensure datetime.strptime still works
        mock_datetime.strptime = datetime.strptime

        target_dt_str = "2024-01-02 12:00:00"
        expected_output = "Time until apocalypse: 1 days, 0 hours, 0 minutes, 0 seconds."
        self.assertEqual(calculate_countdown(target_dt_str), expected_output)

        target_dt_str_complex = "2024-01-01 13:30:45"
        expected_output_complex = "Time until apocalypse: 0 days, 1 hours, 30 minutes, 45 seconds."
        self.assertEqual(calculate_countdown(target_dt_str_complex), expected_output_complex)

    @patch('src.countdown.datetime') # Mock rationale: Patching datetime to control the 'now' value for deterministic tests.
    def test_past_countdown(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.strptime = datetime.strptime

        target_dt_str = "2023-12-31 12:00:00"
        expected_output = "The apocalypse was 1 days, 0 hours, 0 minutes, and 0 seconds ago. You survived (or missed it)!"
        self.assertEqual(calculate_countdown(target_dt_str), expected_output)

        target_dt_str_complex = "2024-01-01 11:30:15"
        expected_output_complex = "The apocalypse was 0 days, 0 hours, 29 minutes, and 45 seconds ago. You survived (or missed it)!"
        self.assertEqual(calculate_countdown(target_dt_str_complex), expected_output_complex)

    @patch('src.countdown.datetime') # Mock rationale: Patching datetime to control the 'now' value for deterministic tests.
    def test_exact_now(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.strptime = datetime.strptime

        target_dt_str = "2024-01-01 12:00:00"
        # When time_left.total_seconds() is 0, it should fall into the 'past' category with 0 days/hours/minutes/seconds ago.
        expected_output = "The apocalypse was 0 days, 0 hours, 0 minutes, and 0 seconds ago. You survived (or missed it)!"
        self.assertEqual(calculate_countdown(target_dt_str), expected_output)

    def test_invalid_format(self):
        target_dt_str = "2024-01-01" # Missing time
        expected_output = "Error: Invalid date/time format. Please use YYYY-MM-DD HH:MM:SS."
        self.assertEqual(calculate_countdown(target_dt_str), expected_output)

        target_dt_str_bad = "not-a-date"
        self.assertEqual(calculate_countdown(target_dt_str_bad), expected_output)

    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture stdout to verify printed output without affecting console.
    @patch('sys.argv', ['countdown.py', '2024-01-02 12:00:00']) # Mock rationale: Simulate command-line arguments for main function.
    @patch('src.countdown.datetime') # Mock rationale: Patching datetime to control the 'now' value for deterministic tests.
    def test_main_future_output(self, mock_datetime, mock_stdout):
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.strptime = datetime.strptime

        main()
        self.assertIn("Time until apocalypse: 1 days, 0 hours, 0 minutes, 0 seconds.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture stdout to verify printed output without affecting console.
    @patch('sys.argv', ['countdown.py', '2023-12-31 12:00:00']) # Mock rationale: Simulate command-line arguments for main function.
    @patch('src.countdown.datetime') # Mock rationale: Patching datetime to control the 'now' value for deterministic tests.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_past_output_and_exit_code(self, mock_exit, mock_datetime, mock_stdout):
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.strptime = datetime.strptime

        main()
        self.assertIn("The apocalypse was 1 days, 0 hours, 0 minutes, and 0 seconds ago.", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture stdout to verify printed output without affecting console.
    @patch('sys.argv', ['countdown.py', 'invalid-date']) # Mock rationale: Simulate command-line arguments for main function.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_invalid_format_output_and_exit_code(self, mock_exit, mock_stdout):
        # No need to mock datetime here as it won't be called for invalid format
        main()
        self.assertIn("Error: Invalid date/time format.", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
