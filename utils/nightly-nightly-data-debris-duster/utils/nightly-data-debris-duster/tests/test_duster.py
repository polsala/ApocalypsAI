import unittest
import os
import sys
import io
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the src directory to the path to allow importing duster
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import duster

class TestDuster(unittest.TestCase):

    @patch('os.path.getmtime')
    def test_get_file_age_in_days(self, mock_getmtime):
        # Mock rationale: os.path.getmtime returns a timestamp, which is non-deterministic
        # and depends on the current time and file creation. We need to control it for testing.
        
        # Test case 1: File modified exactly 10 days ago
        ten_days_ago = datetime.now() - timedelta(days=10)
        mock_getmtime.return_value = ten_days_ago.timestamp()
        self.assertEqual(duster.get_file_age_in_days("/fake/path/file1.txt"), 10)

        # Test case 2: File modified less than a day ago (0 days)
        one_hour_ago = datetime.now() - timedelta(hours=1)
        mock_getmtime.return_value = one_hour_ago.timestamp()
        self.assertEqual(duster.get_file_age_in_days("/fake/path/file2.txt"), 0)

        # Test case 3: File modified 365 days ago
        one_year_ago = datetime.now() - timedelta(days=365)
        mock_getmtime.return_value = one_year_ago.timestamp()
        self.assertEqual(duster.get_file_age_in_days("/fake/path/file3.txt"), 365)

    @patch('os.walk')
    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('duster.get_file_age_in_days')
    def test_find_old_files_non_recursive(self, mock_get_file_age, mock_isfile, mock_exists, mock_walk):
        # Mock rationale: os.walk, os.path.exists, os.path.isfile, and get_file_age_in_days
        # interact with the file system and current time, making them non-deterministic.
        # We mock them to control the file structure and ages for consistent testing.

        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.txt', 'new_file.txt', 'another_old.log'])
        ]
        mock_exists.return_value = True
        mock_isfile.return_value = True

        # Simulate ages: old_file.txt (15 days), new_file.txt (5 days), another_old.log (12 days)
        mock_get_file_age.side_effect = [15, 5, 12]

        # Test with threshold 10 days
        result = duster.find_old_files('/test_dir', 10, recursive=False)
        self.assertIn(os.path.join('/test_dir', 'old_file.txt'), result)
        self.assertNotIn(os.path.join('/test_dir', 'new_file.txt'), result)
        self.assertIn(os.path.join('/test_dir', 'another_old.log'), result)
        self.assertEqual(len(result), 2)

        # Test with threshold 20 days (no files should be found)
        mock_get_file_age.side_effect = [15, 5, 12] # Reset side_effect for new call
        result = duster.find_old_files('/test_dir', 20, recursive=False)
        self.assertEqual(len(result), 0)

    @patch('os.walk')
    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('duster.get_file_age_in_days')
    def test_find_old_files_recursive(self, mock_get_file_age, mock_isfile, mock_exists, mock_walk):
        # Mock rationale: Same as above, controlling file system interactions and time-dependent logic.

        mock_walk.return_value = [
            ('/test_dir', ['subdir1', 'subdir2'], ['old_file.txt', 'new_file.txt']),
            ('/test_dir/subdir1', [], ['sub_old.txt']),
            ('/test_dir/subdir2', [], ['sub_new.txt', 'sub_another_old.log'])
        ]
        mock_exists.return_value = True
        mock_isfile.return_value = True

        # Simulate ages for files in order of os.walk traversal:
        # /test_dir/old_file.txt (15 days)
        # /test_dir/new_file.txt (5 days)
        # /test_dir/subdir1/sub_old.txt (20 days)
        # /test_dir/subdir2/sub_new.txt (8 days)
        # /test_dir/subdir2/sub_another_old.log (12 days)
        mock_get_file_age.side_effect = [15, 5, 20, 8, 12]

        # Test with threshold 10 days, recursive
        result = duster.find_old_files('/test_dir', 10, recursive=True)
        self.assertIn(os.path.join('/test_dir', 'old_file.txt'), result)
        self.assertNotIn(os.path.join('/test_dir', 'new_file.txt'), result)
        self.assertIn(os.path.join('/test_dir', 'subdir1', 'sub_old.txt'), result)
        self.assertNotIn(os.path.join('/test_dir', 'subdir2', 'sub_new.txt'), result)
        self.assertIn(os.path.join('/test_dir', 'subdir2', 'sub_another_old.log'), result)
        self.assertEqual(len(result), 3)

    @patch('os.remove')
    @patch('builtins.input', return_value='yes')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_files_with_confirmation(self, mock_stdout, mock_input, mock_remove):
        # Mock rationale: os.remove modifies the file system, which is undesirable in tests.
        # builtins.input is mocked to provide deterministic user input for confirmation.
        # sys.stdout is captured to verify print statements.

        file_list = ['/fake/path/file1.txt', '/fake/path/file2.txt']
        duster.delete_files(file_list, force=False)

        mock_input.assert_called_once_with("\nAre you sure you want to delete these files? (yes/no): ")
        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('/fake/path/file1.txt')
        mock_remove.assert_any_call('/fake/path/file2.txt')
        self.assertIn("Successfully deleted 2 files.", mock_stdout.getvalue())

    @patch('os.remove')
    @patch('builtins.input', return_value='no')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_files_confirmation_cancelled(self, mock_stdout, mock_input, mock_remove):
        # Mock rationale: Same as above, ensuring cancellation logic works.

        file_list = ['/fake/path/file1.txt']
        duster.delete_files(file_list, force=False)

        mock_input.assert_called_once()
        mock_remove.assert_not_called()
        self.assertIn("Deletion cancelled.", mock_stdout.getvalue())

    @patch('os.remove')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_files_force_deletion(self, mock_stdout, mock_remove):
        # Mock rationale: Same as above, testing the --force flag bypasses confirmation.

        file_list = ['/fake/path/file1.txt', '/fake/path/file2.txt']
        duster.delete_files(file_list, force=True)

        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('/fake/path/file1.txt')
        mock_remove.assert_any_call('/fake/path/file2.txt')
        self.assertIn("Successfully deleted 2 files.", mock_stdout.getvalue())

    @patch('os.remove', side_effect=OSError("Permission denied"))
    @patch('builtins.input', return_value='yes')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_files_with_error(self, mock_stdout, mock_input, mock_remove):
        # Mock rationale: Simulating an OSError during deletion to ensure error handling.

        file_list = ['/fake/path/file1.txt']
        duster.delete_files(file_list, force=False)

        mock_input.assert_called_once()
        mock_remove.assert_called_once_with('/fake/path/file1.txt')
        self.assertIn("Error deleting /fake/path/file1.txt: Permission denied", mock_stdout.getvalue())
        self.assertIn("Successfully deleted 0 files.", mock_stdout.getvalue()) # 0 because the one file failed

    @patch('duster.find_old_files', return_value=['/fake/path/old_file.txt'])
    @patch('duster.delete_files')
    @patch('os.path.isdir', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_delete_mode(self, mock_stdout, mock_isdir, mock_delete_files, mock_find_old_files):
        # Mock rationale: Mocking main components to test the main function's flow without
        # actual file system interaction or parsing real arguments.

        test_args = ['duster.py', '--path', '/test_dir', '--days', '10', '--delete']
        with patch('sys.argv', test_args):
            duster.main()
        mock_find_old_files.assert_called_once_with('/test_dir', 10, False)
        mock_delete_files.assert_called_once_with(['/fake/path/old_file.txt'], False)
        self.assertNotIn("No files were deleted.", mock_stdout.getvalue()) # Should not print this in delete mode

    @patch('duster.find_old_files', return_value=['/fake/path/old_file.txt', '/fake/path/another_old.txt'])
    @patch('duster.delete_files')
    @patch('os.path.isdir', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_list_mode(self, mock_stdout, mock_isdir, mock_delete_files, mock_find_old_files):
        # Mock rationale: Same as above, testing list mode.

        test_args = ['duster.py', '--path', '/test_dir', '--days', '10']
        with patch('sys.argv', test_args):
            duster.main()
        mock_find_old_files.assert_called_once_with('/test_dir', 10, False)
        mock_delete_files.assert_not_called()
        self.assertIn("Found 2 files older than 10 days", mock_stdout.getvalue())
        self.assertIn("- /fake/path/old_file.txt", mock_stdout.getvalue())
        self.assertIn("- /fake/path/another_old.txt", mock_stdout.getvalue())
        self.assertIn("No files were deleted. To delete, run again with the --delete flag.", mock_stdout.getvalue())

    @patch('duster.find_old_files', return_value=[])
    @patch('os.path.isdir', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_no_old_files(self, mock_exit, mock_stdout, mock_isdir, mock_find_old_files):
        # Mock rationale: Testing the scenario where no old files are found.
        # sys.exit is mocked to prevent the test runner from exiting.

        test_args = ['duster.py', '--path', '/test_dir', '--days', '10']
        with patch('sys.argv', test_args):
            duster.main()
        mock_find_old_files.assert_called_once_with('/test_dir', 10, False)
        self.assertIn("No old files found matching the criteria.", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(0)

    @patch('os.path.isdir', return_value=False)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_stdout, mock_isdir):
        # Mock rationale: Testing error handling for invalid directory path.
        # sys.exit is mocked to prevent the test runner from exiting.

        test_args = ['duster.py', '--path', '/non_existent_dir', '--days', '10']
        with patch('sys.argv', test_args):
            duster.main()
        self.assertIn("Error: Directory '/non_existent_dir' not found.", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('duster.find_old_files', return_value=['/fake/path/old_file.txt'])
    @patch('duster.delete_files')
    @patch('os.path.isdir', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_recursive_flag(self, mock_stdout, mock_isdir, mock_delete_files, mock_find_old_files):
        # Mock rationale: Verifying the recursive flag is passed correctly.

        test_args = ['duster.py', '--path', '/test_dir', '--days', '10', '--recursive']
        with patch('sys.argv', test_args):
            duster.main()
        mock_find_old_files.assert_called_once_with('/test_dir', 10, True) # Check recursive=True
        mock_delete_files.assert_not_called() # Still in list mode

    @patch('duster.find_old_files', return_value=['/fake/path/old_file.txt'])
    @patch('duster.delete_files')
    @patch('os.path.isdir', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_force_flag(self, mock_stdout, mock_isdir, mock_delete_files, mock_find_old_files):
        # Mock rationale: Verifying the force flag is passed correctly to delete_files.

        test_args = ['duster.py', '--path', '/test_dir', '--days', '10', '--delete', '--force']
        with patch('sys.argv', test_args):
            duster.main()
        mock_find_old_files.assert_called_once_with('/test_dir', 10, False)
        mock_delete_files.assert_called_once_with(['/fake/path/old_file.txt'], True) # Check force=True

if __name__ == '__main__':
    unittest.main()
