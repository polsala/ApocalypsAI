import unittest
from unittest.mock import patch, mock_open
import datetime
import os
import sys

# Add the src directory to the path to allow importing chronicle_keeper
# Mock rationale: Allows the test script to find and import the module under test
# when run from the 'tests' directory, without requiring complex package installation.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from chronicle_keeper import append_to_logbook
sys.path.pop(0)

class TestChronicleKeeper(unittest.TestCase):

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    def test_append_to_new_logbook(self, mock_dt, mock_file_open, mock_exists):
        # Mock rationale: Simulate a new file not existing to test file creation.
        mock_exists.return_value = False
        # Mock rationale: Control the current time for deterministic timestamp generation.
        mock_dt.now.return_value = datetime.datetime(2024, 7, 20, 10, 30, 0)

        message = "Found a shiny new wrench."
        log_file = "test_logbook.md"
        append_to_logbook(message, log_file)

        mock_exists.assert_called_once_with(log_file)
        mock_file_open.assert_called_once_with(log_file, 'w', encoding='utf-8')
        handle = mock_file_open()
        expected_content = "## 2024-07-20 10:30:00\n\nFound a shiny new wrench.\n\n---\n\n"
        handle.write.assert_called_once_with(expected_content)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    def test_append_to_existing_logbook(self, mock_dt, mock_file_open, mock_exists):
        # Mock rationale: Simulate an existing file to test appending.
        mock_exists.return_value = True
        # Mock rationale: Control the current time for deterministic timestamp generation.
        mock_dt.now.return_value = datetime.datetime(2024, 7, 21, 11, 0, 0)

        message = "Repaired the water purifier."
        log_file = "test_logbook.md"
        append_to_logbook(message, log_file)

        mock_exists.assert_called_once_with(log_file)
        mock_file_open.assert_called_once_with(log_file, 'a', encoding='utf-8')
        handle = mock_file_open()
        expected_content = "## 2024-07-21 11:00:00\n\nRepaired the water purifier.\n\n---\n\n"
        handle.write.assert_called_once_with(expected_content)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    def test_append_multiple_entries(self, mock_dt, mock_file_open, mock_exists):
        # Mock rationale: Simulate file existence for sequential appends.
        mock_exists.side_effect = [False, True] # First call: new file, second call: existing
        # Mock rationale: Control the current time for deterministic timestamp generation.
        mock_dt.now.side_effect = [
            datetime.datetime(2024, 7, 20, 10, 0, 0),
            datetime.datetime(2024, 7, 20, 11, 0, 0)
        ]

        log_file = "test_logbook.md"

        # First entry
        append_to_logbook("First entry.", log_file)
        first_expected_content = "## 2024-07-20 10:00:00\n\nFirst entry.\n\n---\n\n"
        mock_file_open.assert_called_with(log_file, 'w', encoding='utf-8')
        mock_file_open().write.assert_called_with(first_expected_content)

        # Reset mock for second call
        mock_file_open.reset_mock()
        mock_file_open().write.reset_mock()

        # Second entry
        append_to_logbook("Second entry.", log_file)
        second_expected_content = "## 2024-07-20 11:00:00\n\nSecond entry.\n\n---\n\n"
        mock_file_open.assert_called_with(log_file, 'a', encoding='utf-8')
        mock_file_open().write.assert_called_with(second_expected_content)

        self.assertEqual(mock_exists.call_count, 2)
        self.assertEqual(mock_file_open.call_count, 2)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    def test_custom_file_name(self, mock_dt, mock_file_open, mock_exists):
        # Mock rationale: Simulate a new file not existing to test file creation with custom name.
        mock_exists.return_value = False
        # Mock rationale: Control the current time for deterministic timestamp generation.
        mock_dt.now.return_value = datetime.datetime(2024, 7, 22, 9, 15, 0)

        message = "Custom log entry."
        custom_log_file = "my_special_chronicle.md"
        append_to_logbook(message, custom_log_file)

        mock_exists.assert_called_once_with(custom_log_file)
        mock_file_open.assert_called_once_with(custom_log_file, 'w', encoding='utf-8')
        handle = mock_file_open()
        expected_content = "## 2024-07-22 09:15:00\n\nCustom log entry.\n\n---\n\n"
        handle.write.assert_called_once_with(expected_content)

if __name__ == '__main__':
    unittest.main()
