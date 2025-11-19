import unittest
from unittest.mock import patch, mock_open, MagicMock
import datetime
import os
import sys
from io import StringIO

# Adjust path to import journal.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import journal

class TestJournal(unittest.TestCase):

    # Mock rationale: We need a consistent date and time for testing
    # timestamping, independent of when the test is run.
    MOCK_DATE = datetime.date(2077, 10, 23)
    MOCK_DATETIME = datetime.datetime(2077, 10, 23, 14, 30, 0)

    @patch('journal.datetime.datetime')
    @patch('journal.os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_add_entry(self, mock_file_open, mock_makedirs, mock_dt):
        # Mock rationale: Ensure deterministic timestamp.
        mock_dt.now.return_value = self.MOCK_DATETIME
        mock_dt.date.return_value = self.MOCK_DATE
        mock_dt.strptime = datetime.datetime.strptime # Keep original strptime for date parsing if needed elsewhere

        entry_text = "Found a shiny bottle cap!"
        
        # Mock rationale: Capture print output for assertion.
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            journal.add_entry(entry_text)
            
            # Assert file operations
            expected_log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
            expected_log_file = os.path.join(expected_log_dir, '2077-10-23.txt')
            
            mock_makedirs.assert_called_once_with(expected_log_dir, exist_ok=True) # Mock rationale: Prevent actual directory creation.
            mock_file_open.assert_called_once_with(expected_log_file, 'a', encoding='utf-8') # Mock rationale: Prevent actual file write.
            mock_file_open().write.assert_called_once_with(f"[14:30:00] {entry_text}\n")

            # Assert print output
            self.assertIn("Gratitude logged for 2077-10-23.", mock_stdout.getvalue())

    @patch('journal.datetime.datetime')
    @patch('journal.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_entries_today(self, mock_file_open, mock_path_exists, mock_dt):
        # Mock rationale: Ensure deterministic 'today' for viewing.
        mock_dt.today.return_value = self.MOCK_DATE
        mock_dt.strptime = datetime.datetime.strptime # Keep original strptime

        mock_path_exists.return_value = True # Mock rationale: Simulate file existing.
        mock_file_open.return_value.__enter__.return_value.read.return_value = "[14:30:00] Test entry 1\n[15:00:00] Test entry 2\n"

        # Mock rationale: Capture print output for assertion.
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            journal.view_entries()
            
            expected_log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
            expected_log_file = os.path.join(expected_log_dir, '2077-10-23.txt')
            
            mock_path_exists.assert_called_once_with(expected_log_file) # Mock rationale: Check if file existence is queried.
            mock_file_open.assert_called_once_with(expected_log_file, 'r', encoding='utf-8') # Mock rationale: Prevent actual file read.
            
            output = mock_stdout.getvalue()
            self.assertIn("--- Gratitude for 2077-10-23 ---", output)
            self.assertIn("[14:30:00] Test entry 1", output)
            self.assertIn("[15:00:00] Test entry 2", output)

    @patch('journal.datetime.datetime')
    @patch('journal.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_entries_specific_date(self, mock_file_open, mock_path_exists, mock_dt):
        # Mock rationale: Ensure deterministic 'today' for viewing.
        mock_dt.today.return_value = datetime.date(2077, 10, 24) # Different from target date
        mock_dt.strptime = datetime.datetime.strptime # Keep original strptime

        mock_path_exists.return_value = True # Mock rationale: Simulate file existing.
        mock_file_open.return_value.__enter__.return_value.read.return_value = "[10:00:00] Specific date entry.\n"

        # Mock rationale: Capture print output for assertion.
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            journal.view_entries("2077-10-23")
            
            expected_log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
            expected_log_file = os.path.join(expected_log_dir, '2077-10-23.txt')
            
            mock_path_exists.assert_called_once_with(expected_log_file) # Mock rationale: Check if file existence is queried.
            mock_file_open.assert_called_once_with(expected_log_file, 'r', encoding='utf-8') # Mock rationale: Prevent actual file read.
            
            output = mock_stdout.getvalue()
            self.assertIn("--- Gratitude for 2077-10-23 ---", output)
            self.assertIn("[10:00:00] Specific date entry.", output)

    @patch('journal.datetime.datetime')
    @patch('journal.os.path.exists')
    @patch('journal.os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_entries_all(self, mock_file_open, mock_listdir, mock_path_exists, mock_dt):
        # Mock rationale: Ensure deterministic 'today' for viewing.
        mock_dt.today.return_value = self.MOCK_DATE
        mock_dt.strptime = datetime.datetime.strptime # Keep original strptime

        mock_path_exists.side_effect = lambda p: 'logs' in p # Mock rationale: Simulate logs directory existing.
        mock_listdir.return_value = ['2077-10-22.txt', '2077-10-23.txt'] # Mock rationale: Simulate log files.

        # Configure mock_open to return different content for different files
        mock_file_content = {
            os.path.join(journal.get_log_directory(), '2077-10-22.txt'): "[09:00:00] Entry from yesterday.\n",
            os.path.join(journal.get_log_directory(), '2077-10-23.txt'): "[14:30:00] Entry from today.\n"
        }
        
        def mock_open_side_effect(file_path, mode, encoding):
            if file_path in mock_file_content:
                mock_file = MagicMock()
                mock_file.read.return_value = mock_file_content[file_path]
                mock_file.readlines.return_value = mock_file_content[file_path].splitlines(keepends=True)
                return mock_file
            raise FileNotFoundError
        
        mock_file_open.side_effect = mock_open_side_effect # Mock rationale: Simulate reading different files.

        # Mock rationale: Capture print output for assertion.
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            journal.view_entries(view_all=True)
            
            output = mock_stdout.getvalue()
            self.assertIn("--- 2077-10-22 ---", output)
            self.assertIn("[09:00:00] Entry from yesterday.", output)
            self.assertIn("--- 2077-10-23 ---", output)
            self.assertIn("[14:30:00] Entry from today.", output)
            
            # Ensure files were opened in correct order
            calls = mock_file_open.call_args_list
            self.assertEqual(len(calls), 2)
            self.assertIn('2077-10-22.txt', calls[0].args[0])
            self.assertIn('2077-10-23.txt', calls[1].args[0])

    @patch('journal.datetime.datetime')
    @patch('journal.os.path.exists')
    @patch('journal.os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_entries_all_no_logs_dir(self, mock_file_open, mock_listdir, mock_path_exists, mock_dt):
        # Mock rationale: Ensure deterministic 'today' for viewing.
        mock_dt.today.return_value = self.MOCK_DATE
        mock_dt.strptime = datetime.datetime.strptime # Keep original strptime

        mock_path_exists.return_value = False # Mock rationale: Simulate logs directory not existing.

        # Mock rationale: Capture print output for assertion.
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            journal.view_entries(view_all=True)
            
            self.assertIn("No gratitude entries found yet.", mock_stdout.getvalue())
            mock_listdir.assert_not_called() # Mock rationale: listdir should not be called if dir doesn't exist.
            mock_file_open.assert_not_called() # Mock rationale: No files should be opened.

    @patch('journal.datetime.datetime')
    @patch('journal.os.path.exists')
    @patch('journal.os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_entries_all_empty_logs_dir(self, mock_file_open, mock_listdir, mock_path_exists, mock_dt):
        # Mock rationale: Ensure deterministic 'today' for viewing.
        mock_dt.today.return_value = self.MOCK_DATE
        mock_dt.strptime = datetime.datetime.strptime # Keep original strptime

        mock_path_exists.return_value = True # Mock rationale: Simulate logs directory existing.
        mock_listdir.return_value = [] # Mock rationale: Simulate empty logs directory.

        # Mock rationale: Capture print output for assertion.
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            journal.view_entries(view_all=True)
            
            self.assertIn("No gratitude entries found yet.", mock_stdout.getvalue())
            mock_listdir.assert_called_once() # Mock rationale: listdir should be called.
            mock_file_open.assert_not_called() # Mock rationale: No files should be opened.

    @patch('journal.argparse.ArgumentParser.parse_args')
    @patch('journal.add_entry')
    @patch('journal.view_entries')
    def test_main_add_command(self, mock_view_entries, mock_add_entry, mock_parse_args):
        # Mock rationale: Simulate CLI arguments for 'add' command.
        mock_parse_args.return_value = MagicMock(command='add', entry='Test gratitude')
        journal.main()
        mock_add_entry.assert_called_once_with('Test gratitude')
        mock_view_entries.assert_not_called()

    @patch('journal.argparse.ArgumentParser.parse_args')
    @patch('journal.add_entry')
    @patch('journal.view_entries')
    def test_main_view_command_today(self, mock_view_entries, mock_add_entry, mock_parse_args):
        # Mock rationale: Simulate CLI arguments for 'view' command (today).
        mock_parse_args.return_value = MagicMock(command='view', date=None, all=False)
        journal.main()
        mock_view_entries.assert_called_once_with(None, False)
        mock_add_entry.assert_not_called()

    @patch('journal.argparse.ArgumentParser.parse_args')
    @patch('journal.add_entry')
    @patch('journal.view_entries')
    def test_main_view_command_specific_date(self, mock_view_entries, mock_add_entry, mock_parse_args):
        # Mock rationale: Simulate CLI arguments for 'view' command (specific date).
        mock_parse_args.return_value = MagicMock(command='view', date='2077-10-23', all=False)
        journal.main()
        mock_view_entries.assert_called_once_with('2077-10-23', False)
        mock_add_entry.assert_not_called()

    @patch('journal.argparse.ArgumentParser.parse_args')
    @patch('journal.add_entry')
    @patch('journal.view_entries')
    def test_main_view_command_all(self, mock_view_entries, mock_add_entry, mock_parse_args):
        # Mock rationale: Simulate CLI arguments for 'view' command (--all).
        mock_parse_args.return_value = MagicMock(command='view', date=None, all=True)
        journal.main()
        mock_view_entries.assert_called_once_with(None, True)
        mock_add_entry.assert_not_called()

    @patch('journal.argparse.ArgumentParser.parse_args')
    @patch('journal.argparse.ArgumentParser.print_help')
    @patch('journal.add_entry')
    @patch('journal.view_entries')
    def test_main_no_command(self, mock_view_entries, mock_add_entry, mock_print_help, mock_parse_args):
        # Mock rationale: Simulate no command provided.
        mock_parse_args.return_value = MagicMock(command=None)
        journal.main()
        mock_print_help.assert_called_once()
        mock_add_entry.assert_not_called()
        mock_view_entries.assert_not_called()

    def test_get_log_directory(self):
        # This test doesn't need mocks as it only deals with path construction
        # relative to the script's location, which is deterministic.
        expected_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
        self.assertEqual(journal.get_log_directory(), expected_dir)

    @patch('journal.os.makedirs')
    def test_get_log_file_path(self, mock_makedirs):
        # This test also primarily deals with path construction.
        # Mock rationale: Prevent actual directory creation.
        mock_date = datetime.date(2077, 10, 23)
        expected_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
        expected_path = os.path.join(expected_dir, '2077-10-23.txt')
        
        self.assertEqual(journal.get_log_file_path(mock_date), expected_path)
        mock_makedirs.assert_called_once_with(expected_dir, exist_ok=True)

    @patch('journal.datetime.datetime')
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_entries_invalid_date_format(self, mock_stdout, mock_dt):
        # Mock rationale: Ensure deterministic 'today' for viewing.
        mock_dt.today.return_value = self.MOCK_DATE
        mock_dt.strptime = datetime.datetime.strptime # Keep original strptime

        journal.view_entries("invalid-date")
        self.assertIn("Error: Invalid date format 'invalid-date'. Please use YYYY-MM-DD.", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
