import unittest
from unittest.mock import patch, mock_open
import datetime
import os
import sys
from io import StringIO

# Adjust path to import the module from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from chronicle_keeper import add_entry, view_entries, _get_log_path, LOG_FILE_NAME

class TestChronicleKeeper(unittest.TestCase):

    @patch('chronicle_keeper.datetime')
    @patch('chronicle_keeper.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_add_entry_no_tags(self, mock_file_open, mock_exists, mock_dt):
        # Mock rationale: Simulate file system operations without actually touching the disk.
        # mock_file_open replaces 'open', mock_exists replaces 'os.path.exists'.
        # mock_dt replaces 'datetime' to ensure deterministic timestamps.

        mock_exists.return_value = True # Assume file exists for append
        mock_dt.datetime.now.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)
        mock_dt.datetime.strftime.return_value = '2023-01-01 12:00:00'

        message = "A new day, a new entry."
        add_entry(message)

        expected_entry = "[2023-01-01 12:00:00] A new day, a new entry.\n"
        mock_file_open.assert_called_once_with(_get_log_path(), 'a', encoding='utf-8')
        mock_file_open().write.assert_called_once_with(expected_entry)

    @patch('chronicle_keeper.datetime')
    @patch('chronicle_keeper.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_add_entry_with_tags(self, mock_file_open, mock_exists, mock_dt):
        # Mock rationale: Same as above, ensuring tags are correctly formatted and written.
        mock_exists.return_value = True
        mock_dt.datetime.now.return_value = datetime.datetime(2023, 1, 2, 13, 30, 0)
        mock_dt.datetime.strftime.return_value = '2023-01-02 13:30:00'

        message = "Found some rare berries."
        tags = ['#food', '#discovery']
        add_entry(message, tags)

        expected_entry = "[2023-01-02 13:30:00] #food #discovery Found some rare berries.\n"
        mock_file_open.assert_called_once_with(_get_log_path(), 'a', encoding='utf-8')
        mock_file_open().write.assert_called_once_with(expected_entry)

    @patch('chronicle_keeper.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_all_entries(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate reading from a log file and capture stdout to verify output.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = (
            "[2023-01-01 12:00:00] Entry 1.\n"
            "[2023-01-02 13:30:00] #tag1 Entry 2.\n"
        )

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        view_entries()

        sys.stdout = sys.__stdout__ # Reset stdout
        self.assertEqual(captured_output.getvalue().strip(),
                         "[2023-01-01 12:00:00] Entry 1.\n[2023-01-02 13:30:00] #tag1 Entry 2.")
        mock_file_open.assert_called_once_with(_get_log_path(), 'r', encoding='utf-8')

    @patch('chronicle_keeper.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_filtered_entries(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate reading from a log file and filtering by tag.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = (
            "[2023-01-01 12:00:00] #weather Clear skies.\n"
            "[2023-01-02 13:30:00] #resource Found water.\n"
            "[2023-01-03 14:00:00] #weather Storm approaching.\n"
        )

        captured_output = StringIO()
        sys.stdout = captured_output

        view_entries(tag='#weather')

        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(),
                         "[2023-01-01 12:00:00] #weather Clear skies.\n[2023-01-03 14:00:00] #weather Storm approaching.")
        mock_file_open.assert_called_once_with(_get_log_path(), 'r', encoding='utf-8')

    @patch('chronicle_keeper.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_no_matching_tag(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a log file with no entries matching the filter.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = (
            "[2023-01-01 12:00:00] #weather Clear skies.\n"
        )

        captured_output = StringIO()
        sys.stdout = captured_output

        view_entries(tag='#food')

        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "No entries found with tag '#food'.")

    @patch('chronicle_keeper.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_empty_log_file(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate an empty log file.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = ""

        captured_output = StringIO()
        sys.stdout = captured_output

        view_entries()

        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "No entries found in the chronicle.")

    @patch('chronicle_keeper.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_log_file_not_found(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate the scenario where the log file does not exist.
        mock_exists.return_value = False

        captured_output = StringIO()
        sys.stdout = captured_output

        view_entries()

        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "Chronicle log file not found. Start by adding an entry!")
        mock_file_open.assert_not_called() # Ensure open is not called if file doesn't exist

    @patch('chronicle_keeper.datetime')
    @patch('chronicle_keeper.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_add_entry_creates_file_if_not_exists(self, mock_file_open, mock_exists, mock_dt):
        # Mock rationale: Verify that 'open' is called with 'a' mode even if the file doesn't exist,
        # which implicitly creates it.
        mock_exists.return_value = False # Simulate file not existing initially
        mock_dt.datetime.now.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)
        mock_dt.datetime.strftime.return_value = '2023-01-01 12:00:00'

        message = "First entry ever."
        add_entry(message)

        mock_file_open.assert_called_once_with(_get_log_path(), 'a', encoding='utf-8')
        mock_file_open().write.assert_called_once() # Just check it was written to

    @patch('chronicle_keeper.os.path.abspath')
    @patch('chronicle_keeper.os.path.dirname')
    def test_get_log_path(self, mock_dirname, mock_abspath):
        # Mock rationale: Ensure _get_log_path constructs the correct path.
        mock_abspath.return_value = '/path/to/src/chronicle_keeper.py'
        mock_dirname.return_value = '/path/to/src'
        
        expected_path = os.path.join('/path/to/src', LOG_FILE_NAME)
        self.assertEqual(_get_log_path(), expected_path)

if __name__ == '__main__':
    unittest.main()
