import unittest
from unittest import mock
import os
import sys
import datetime
from io import StringIO

# Adjust path to import logbook.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import logbook

class TestLogbook(unittest.TestCase):

    def setUp(self):
        # Ensure the log file does not exist before each test
        if os.path.exists(logbook.LOG_FILE):
            os.remove(logbook.LOG_FILE)

        # Mock datetime.datetime.now() for deterministic timestamps
        self.mock_datetime = mock.patch('datetime.datetime')
        self.mock_now = self.mock_datetime.start()
        self.mock_now.now.return_value = datetime.datetime(2024, 7, 20, 10, 0, 0)
        self.addCleanup(self.mock_datetime.stop)

        # Mock sys.stdout for capturing print output
        self.held_stdout = StringIO()
        self.stdout_patch = mock.patch('sys.stdout', self.held_stdout)
        self.stdout_patch.start()
        self.addCleanup(self.stdout_patch.stop)

    def tearDown(self):
        # Clean up the log file after each test
        if os.path.exists(logbook.LOG_FILE):
            os.remove(logbook.LOG_FILE)

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('os.path.exists', return_value=True)
    def test_add_entry(self, mock_exists, mock_open):
        # Mock rationale: We need to control file system interactions (open, write) and ensure
        # os.path.exists returns True for the file to be considered present for writing.
        # We also mock datetime.datetime.now() in setUp for consistent timestamps.

        test_message = "Found a shiny new wrench."
        logbook.add_entry(test_message)

        # Assert that open was called with the correct file and mode
        mock_open.assert_called_once_with(logbook.LOG_FILE, 'a')

        # Assert that the correct content was written
        expected_content = "[2024-07-20 10:00:00] Found a shiny new wrench.\n"
        mock_open().write.assert_called_once_with(expected_content)

        # Assert print output
        self.assertIn(f"Entry added to {logbook.LOG_FILE}.", self.held_stdout.getvalue())

    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data="[2024-07-20 10:00:00] First entry.\n[2024-07-20 10:01:00] Second entry.\n")
    @mock.patch('os.path.exists', return_value=True)
    def test_view_entries_with_content(self, mock_exists, mock_open):
        # Mock rationale: We need to simulate the log file existing and containing specific data
        # without actually creating a file. os.path.exists is mocked to confirm existence.

        logbook.view_entries()

        # Assert that open was called with the correct file and mode
        mock_open.assert_called_once_with(logbook.LOG_FILE, 'r')

        # Assert that the content was printed correctly
        expected_output = "[2024-07-20 10:00:00] First entry.\n[2024-07-20 10:01:00] Second entry.\n"
        self.assertEqual(self.held_stdout.getvalue().strip(), expected_output.strip())

    @mock.patch('os.path.exists', return_value=False)
    def test_view_entries_no_file(self, mock_exists):
        # Mock rationale: We need to simulate the log file not existing without actually deleting it.

        logbook.view_entries()

        # Assert that the correct message is printed
        self.assertIn(f"No chronicle found at {logbook.LOG_FILE}. Start by adding an entry!", self.held_stdout.getvalue())

    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data="")
    @mock.patch('os.path.exists', return_value=True)
    def test_view_entries_empty_file(self, mock_exists, mock_open):
        # Mock rationale: We need to simulate an empty log file existing without actually creating it.

        logbook.view_entries()

        # Assert that the correct message is printed
        self.assertIn(f"The chronicle at {logbook.LOG_FILE} is empty.", self.held_stdout.getvalue())

    @mock.patch('builtins.open', side_effect=IOError("Permission denied"))
    @mock.patch('os.path.exists', return_value=True)
    def test_add_entry_io_error(self, mock_exists, mock_open):
        # Mock rationale: Simulate an IOError during file write operations to test error handling.

        test_message = "Attempting to write."
        logbook.add_entry(test_message)

        self.assertIn("Error writing to log file: Permission denied", self.held_stdout.getvalue())

    @mock.patch('builtins.open', side_effect=IOError("Disk full"))
    @mock.patch('os.path.exists', return_value=True)
    def test_view_entries_io_error(self, mock_exists, mock_open):
        # Mock rationale: Simulate an IOError during file read operations to test error handling.

        logbook.view_entries()

        self.assertIn("Error reading log file: Disk full", self.held_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
