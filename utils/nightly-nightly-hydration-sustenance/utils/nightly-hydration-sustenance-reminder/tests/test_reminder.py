import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timedelta

# Import the main function and other necessary components from the reminder script
from src.reminder import main, REMINDER_INTERVAL_HOURS, MESSAGES, get_timestamp_file_path

class TestReminder(unittest.TestCase):

    @patch('src.reminder.datetime')
    @patch('src.reminder.os.path.exists')
    @patch('src.reminder.open', new_callable=mock_open)
    @patch('src.reminder.random.choice')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_reminder_given_when_no_timestamp_file(self, mock_exit, mock_stdout, mock_random_choice, mock_file_open, mock_exists, mock_datetime):
        # Mock rationale:
        # - sys.exit: Prevent the script from actually exiting during tests.
        # - sys.stdout: Capture printed output to verify messages.
        # - random.choice: Ensure a predictable message is chosen for verification.
        # - open: Simulate file system interactions (reading/writing timestamp).
        # - os.path.exists: Control whether the timestamp file is reported as existing.
        # - datetime: Control the current time for time-based logic.

        mock_exists.return_value = False # No timestamp file exists
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 0, 0) # Arbitrary current time
        mock_random_choice.return_value = MESSAGES[0] # Predictable message

        main()

        mock_random_choice.assert_called_once_with(MESSAGES)
        mock_stdout.write.assert_called_once_with(MESSAGES[0] + '\n')
        mock_file_open.assert_called_once_with(get_timestamp_file_path(), 'w')
        mock_file_open().write.assert_called_once_with(mock_datetime.now.return_value.isoformat())
        mock_exit.assert_called_once_with(0) # Expect success exit code

    @patch('src.reminder.datetime')
    @patch('src.reminder.os.path.exists')
    @patch('src.reminder.open', new_callable=mock_open)
    @patch('src.reminder.random.choice')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_reminder_given_when_interval_passed(self, mock_exit, mock_stdout, mock_random_choice, mock_file_open, mock_exists, mock_datetime):
        # Mock rationale:
        # - sys.exit: Prevent the script from actually exiting during tests.
        # - sys.stdout: Capture printed output to verify messages.
        # - random.choice: Ensure a predictable message is chosen for verification.
        # - open: Simulate file system interactions (reading/writing timestamp).
        # - os.path.exists: Control whether the timestamp file is reported as existing.
        # - datetime: Control the current time for time-based logic.

        mock_exists.return_value = True # Timestamp file exists
        # Last reminded time was 3 hours ago (more than 2-hour interval)
        last_reminded_dt = datetime(2023, 10, 27, 7, 0, 0)
        mock_file_open.return_value.__enter__.return_value.read.return_value = last_reminded_dt.isoformat()
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 0, 0) # Current time
        mock_random_choice.return_value = MESSAGES[1] # Predictable message

        main()

        mock_random_choice.assert_called_once_with(MESSAGES)
        mock_stdout.write.assert_called_once_with(MESSAGES[1] + '\n')
        # Check that open was called to read and then to write
        self.assertEqual(mock_file_open.call_count, 2)
        mock_file_open.assert_any_call(get_timestamp_file_path(), 'r')
        mock_file_open.assert_any_call(get_timestamp_file_path(), 'w')
        mock_file_open().write.assert_called_once_with(mock_datetime.now.return_value.isoformat())
        mock_exit.assert_called_once_with(0) # Expect success exit code

    @patch('src.reminder.datetime')
    @patch('src.reminder.os.path.exists')
    @patch('src.reminder.open', new_callable=mock_open)
    @patch('src.reminder.random.choice')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_no_reminder_given_when_interval_not_passed(self, mock_exit, mock_stdout, mock_random_choice, mock_file_open, mock_exists, mock_datetime):
        # Mock rationale:
        # - sys.exit: Prevent the script from actually exiting during tests.
        # - sys.stdout: Capture printed output to verify messages.
        # - random.choice: Ensure a predictable message is chosen for verification (shouldn't be called).
        # - open: Simulate file system interactions (reading timestamp).
        # - os.path.exists: Control whether the timestamp file is reported as existing.
        # - datetime: Control the current time for time-based logic.

        mock_exists.return_value = True # Timestamp file exists
        # Last reminded time was 1 hour ago (less than 2-hour interval)
        last_reminded_dt = datetime(2023, 10, 27, 9, 0, 0)
        mock_file_open.return_value.__enter__.return_value.read.return_value = last_reminded_dt.isoformat()
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 0, 0) # Current time

        main()

        mock_random_choice.assert_not_called() # No message should be chosen or printed
        mock_stdout.write.assert_not_called()
        # Only read operation should happen
        mock_file_open.assert_called_once_with(get_timestamp_file_path(), 'r')
        mock_file_open().write.assert_not_called() # No write operation
        mock_exit.assert_called_once_with(2) # Expect no-op exit code

    @patch('src.reminder.datetime')
    @patch('src.reminder.os.path.exists')
    @patch('src.reminder.open', new_callable=mock_open)
    @patch('src.reminder.random.choice')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_reminder_given_when_timestamp_file_corrupted(self, mock_exit, mock_stdout, mock_random_choice, mock_file_open, mock_exists, mock_datetime):
        # Mock rationale:
        # - sys.exit: Prevent the script from actually exiting during tests.
        # - sys.stdout: Capture printed output to verify messages.
        # - random.choice: Ensure a predictable message is chosen for verification.
        # - open: Simulate file system interactions (reading/writing timestamp).
        # - os.path.exists: Control whether the timestamp file is reported as existing.
        # - datetime: Control the current time for time-based logic.

        mock_exists.return_value = True # Timestamp file exists
        # Simulate a corrupted file content
        mock_file_open.return_value.__enter__.return_value.read.return_value = "NOT_A_VALID_TIMESTAMP"
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 0, 0) # Current time
        mock_random_choice.return_value = MESSAGES[0] # Predictable message

        main()

        mock_random_choice.assert_called_once_with(MESSAGES)
        mock_stdout.write.assert_called_once_with(MESSAGES[0] + '\n')
        # Check that open was called to read and then to write
        self.assertEqual(mock_file_open.call_count, 2)
        mock_file_open.assert_any_call(get_timestamp_file_path(), 'r')
        mock_file_open.assert_any_call(get_timestamp_file_path(), 'w')
        mock_file_open().write.assert_called_once_with(mock_datetime.now.return_value.isoformat())
        mock_exit.assert_called_once_with(0) # Expect success exit code
