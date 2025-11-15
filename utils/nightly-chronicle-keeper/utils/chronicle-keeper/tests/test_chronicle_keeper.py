import unittest
from unittest.mock import patch, mock_open
import os
import datetime
import shutil
import io # Required for sys.stdout mock

# Import the function to be tested
from src.chronicle_keeper import generate_log_entry

class TestChronicleKeeper(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for tests to run in
        self.original_cwd = os.getcwd()
        self.test_dir = 'temp_test_chronicle_keeper_dir'
        os.makedirs(self.test_dir, exist_ok=True)
        os.chdir(self.test_dir)
        # Mock rationale: Isolate file system operations to a temporary directory
        # to ensure tests are self-contained and don't affect the actual project structure.

    def tearDown(self):
        # Change back to original directory and clean up the temporary directory
        os.chdir(self.original_cwd)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('builtins.input', side_effect=[
        'Scavenged Sector 7. Encountered feral drones.',
        'Food: 3 days, Water: 5 days, Ammo: 17 rounds',
        '3',
        'Saw strange lights in the northern sky.'
    ])
    @patch('datetime.date')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=io.StringIO) # Mock rationale: Capture print statements to verify output.
    def test_generate_log_entry(self, mock_stdout, mock_file_open, mock_date, mock_input):
        # Mock rationale: Simulate user input for deterministic testing.
        # Mock rationale: Fix the date to ensure consistent filename and content.
        # Mock rationale: Capture file write operations without actually touching the disk.

        # Set a fixed date for testing
        fixed_date = datetime.date(2023, 10, 27)
        mock_date.today.return_value = fixed_date
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw) # Allow actual date object creation

        # Call the function
        generate_log_entry()

        # Expected filename and content
        expected_filename = os.path.join('logs', '2023-10-27-chronicle.md')
        expected_content = """# Chronicle Entry - 2023-10-27

## Key Events:

Scavenged Sector 7. Encountered feral drones.

## Resource Status:

Food: 3 days, Water: 5 days, Ammo: 17 rounds

## Morale:

3/5

## Observations & Reflections:

Saw strange lights in the northern sky.
"""

        # Assert that open was called with the correct filename and mode
        mock_file_open.assert_called_once_with(expected_filename, 'w', encoding='utf-8')

        # Assert that the correct content was written to the file
        mock_file_open().write.assert_called_once_with(expected_content)

        # Assert print output
        self.assertIn(f"Chronicle entry saved to {expected_filename}", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=[
        'Event',
        'Resources',
        '1',
        'Obs'
    ])
    @patch('datetime.date')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs', side_effect=IOError('Disk full')) # Mock rationale: Simulate an IOError during directory creation.
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_generate_log_entry_io_error(self, mock_stdout, mock_makedirs, mock_file_open, mock_date, mock_input):
        # Mock rationale: Simulate user input and fixed date as in the successful case.
        # Mock rationale: Simulate an IOError when trying to create the 'logs' directory.
        # Mock rationale: Capture print statements to verify error output.

        fixed_date = datetime.date(2023, 10, 27)
        mock_date.today.return_value = fixed_date
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)

        generate_log_entry()

        # Assert that an error message was printed
        self.assertIn("Error saving chronicle entry: Disk full", mock_stdout.getvalue())
        # Ensure open was not called if makedirs failed
        mock_file_open.assert_not_called()
