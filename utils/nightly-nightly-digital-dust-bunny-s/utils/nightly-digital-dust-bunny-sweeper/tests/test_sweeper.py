import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions from the sweeper module
from src.sweeper import get_file_age_in_days, find_old_files, delete_files

class TestDigitalDustBunnySweeper(unittest.TestCase):

    @patch('src.sweeper.datetime')
    def test_get_file_age_in_days(self, mock_datetime):
        # Mock rationale: `datetime.now()` needs to be controlled to simulate current time
        # for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2023, 10, 26)
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

        # Mock rationale: `os.path.getmtime` needs to be controlled to simulate file modification times.
        with patch('os.path.getmtime', return_value=datetime(2023, 9, 26).timestamp()):
            self.assertEqual(get_file_age_in_days("/path/to/old_file.txt"), 30)

        with patch('os.path.getmtime', return_value=datetime(2023, 10, 25).timestamp()):
            self.assertEqual(get_file_age_in_days("/path/to/recent_file.txt"), 1)

        with patch('os.path.getmtime', return_value=datetime(2023, 10, 26).timestamp()):
            self.assertEqual(get_file_age_in_days("/path/to/today_file.txt"), 0)

        # Test file not found scenario
        with patch('os.path.getmtime', side_effect=FileNotFoundError):
            self.assertEqual(get_file_age_in_days("/path/to/non_existent.txt"), -1)

    @patch('src.sweeper.os.path.isdir', return_value=True)
    @patch('src.sweeper.os.walk')
    @patch('src.sweeper.get_file_age_in_days')
    def test_find_old_files(self, mock_get_file_age, mock_os_walk, mock_isdir):
        # Mock rationale: `os.path.isdir` needs to be controlled to simulate valid directories.
        # Mock rationale: `os.walk` needs to be controlled to simulate directory structure and files.
        # Mock rationale: `get_file_age_in_days` is already tested, so we mock it here to control file ages directly.

        # Scenario 1: No files found
        mock_os_walk.return_value = []
        self.assertEqual(find_old_files(["/test/dir"], 30), [])

        # Scenario 2: Some old files, some recent files
        mock_os_walk.return_value = [
            ("/test/dir", [], ["old_file.txt", "recent_file.txt", "another_old.log"]),
            ("/test/dir/subdir", [], ["sub_recent.txt", "sub_old.dat"])
        ]
        # Define ages for each file
        def mock_age_side_effect(filepath):
            if "old_file.txt" in filepath: return 35
            if "recent_file.txt" in filepath: return 10
            if "another_old.log" in filepath: return 95
            if "sub_recent.txt" in filepath: return 20
            if "sub_old.dat" in filepath: return 40
            return 0 # Default for unexpected files

        mock_get_file_age.side_effect = mock_age_side_effect

        expected_files = [
            os.path.join("/test/dir", "old_file.txt"),
            os.path.join("/test/dir", "another_old.log"),
            os.path.join("/test/dir/subdir", "sub_old.dat")
        ]
        self.assertCountEqual(find_old_files(["/test/dir"], 30), expected_files)

        # Scenario 3: Invalid path
        mock_isdir.side_effect = [False, True] # First path invalid, second valid
        mock_os_walk.return_value = [("/valid/dir", [], ["file.txt"])]
        mock_get_file_age.return_value = 100 # Make file.txt old
        
        # Capture print output to check warning
        with patch('builtins.print') as mock_print:
            result = find_old_files(["/invalid/dir", "/valid/dir"], 30)
            mock_print.assert_any_call("Warning: Path '/invalid/dir' is not a valid directory. Skipping.")
            self.assertCountEqual(result, [os.path.join("/valid/dir", "file.txt")])

    @patch('src.sweeper.os.remove')
    @patch('builtins.input', return_value='y') # Mock rationale: `input()` needs to be controlled for user confirmation.
    @patch('builtins.print') # Mock rationale: `print()` needs to be captured to verify output messages.
    @patch('src.sweeper.get_file_age_in_days', return_value=100) # Mock rationale: `get_file_age_in_days` is already tested.
    def test_delete_files_confirmation(self, mock_get_file_age, mock_print, mock_input, mock_os_remove):
        file_list = ["/path/to/file1.txt", "/path/to/file2.log"]

        # Test with confirmation
        delete_files(file_list, dry_run=False, confirm_delete=False)
        mock_input.assert_called_once_with("\nDo you want to delete these files? (y/N): ")
        self.assertEqual(mock_os_remove.call_count, 2)
        mock_os_remove.assert_any_call("/path/to/file1.txt")
        mock_os_remove.assert_any_call("/path/to/file2.log")
        mock_print.assert_any_call("Successfully deleted 2 files.")

        # Test without confirmation (user says 'n')
        mock_input.reset_mock()
        mock_os_remove.reset_mock()
        mock_print.reset_mock()
        mock_input.return_value = 'n'
        delete_files(file_list, dry_run=False, confirm_delete=False)
        mock_input.assert_called_once()
        mock_os_remove.assert_not_called()
        mock_print.assert_any_call("Deletion cancelled.")

    @patch('src.sweeper.os.remove')
    @patch('builtins.print')
    @patch('src.sweeper.get_file_age_in_days', return_value=100)
    def test_delete_files_dry_run(self, mock_get_file_age, mock_print, mock_os_remove):
        file_list = ["/path/to/file1.txt", "/path/to/file2.log"]
        delete_files(file_list, dry_run=True, confirm_delete=False)
        mock_os_remove.assert_not_called()
        mock_print.assert_any_call("--- Dry Run Complete ---")
        mock_print.assert_any_call("No files were deleted. Run without --dry-run to perform actual deletion.")

    @patch('src.sweeper.os.remove')
    @patch('builtins.input') # Mock rationale: `input()` should not be called when confirm_delete is True.
    @patch('builtins.print')
    @patch('src.sweeper.get_file_age_in_days', return_value=100)
    def test_delete_files_auto_confirm(self, mock_get_file_age, mock_print, mock_input, mock_os_remove):
        file_list = ["/path/to/file1.txt", "/path/to/file2.log"]
        delete_files(file_list, dry_run=False, confirm_delete=True)
        mock_input.assert_not_called() # No prompt
        self.assertEqual(mock_os_remove.call_count, 2)
        mock_os_remove.assert_any_call("/path/to/file1.txt")
        mock_os_remove.assert_any_call("/path/to/file2.log")
        mock_print.assert_any_call("Successfully deleted 2 files.")

    @patch('src.sweeper.os.remove', side_effect=OSError("Permission denied"))
    @patch('builtins.input', return_value='y')
    @patch('builtins.print')
    @patch('src.sweeper.get_file_age_in_days', return_value=100)
    def test_delete_files_with_error(self, mock_get_file_age, mock_print, mock_input, mock_os_remove):
        file_list = ["/path/to/file1.txt", "/path/to/file2.log"]
        delete_files(file_list, dry_run=False, confirm_delete=False)
        self.assertEqual(mock_os_remove.call_count, 2) # Attempted to delete both
        mock_print.assert_any_call("Error deleting /path/to/file1.txt: Permission denied")
        mock_print.assert_any_call("Error deleting /path/to/file2.log: Permission denied")
        mock_print.assert_any_call("Successfully deleted 0 files.") # None were successful

    @patch('src.sweeper.os.remove')
    @patch('builtins.print')
    def test_delete_files_empty_list(self, mock_print, mock_os_remove):
        delete_files([], dry_run=False, confirm_delete=False)
        mock_os_remove.assert_not_called()
        mock_print.assert_any_call("No old files found to delete. Your digital space is pristine!")

if __name__ == '__main__':
    unittest.main()
