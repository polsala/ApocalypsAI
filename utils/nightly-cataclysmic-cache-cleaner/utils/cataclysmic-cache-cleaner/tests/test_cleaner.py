import unittest
import os
import time
import builtins
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions from the cleaner script
# Assuming cleaner.py is in src/ and tests/ is at the same level as src/
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cleaner import get_old_files, delete_files, main

class TestCleaner(unittest.TestCase):

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_get_old_files_finds_old(self, mock_getmtime, mock_walk):
        # Mock rationale: os.walk simulates directory traversal, os.path.getmtime simulates file modification times.
        # This allows testing file age logic without actual file system interaction.

        # Simulate a directory structure:
        # /test_dir
        #   ├── old_file.txt
        #   ├── new_file.txt
        #   └── subdir/
        #       └── another_old_file.log
        mock_walk.return_value = [
            ('/test_dir', ['subdir'], ['old_file.txt', 'new_file.txt']),
            ('/test_dir/subdir', [], ['another_old_file.log'])
        ]

        # Define current time and cutoff for 'old' files (e.g., 30 days ago)
        now = datetime.now()
        thirty_days_ago = now - timedelta(days=30)

        # Mock modification times:
        # old_file.txt: 31 days old
        # new_file.txt: 1 day old
        # another_old_file.log: 40 days old
        def mock_getmtime_side_effect(path):
            if 'old_file.txt' in path:
                return (now - timedelta(days=31)).timestamp()
            elif 'new_file.txt' in path:
                return (now - timedelta(days=1)).timestamp()
            elif 'another_old_file.log' in path:
                return (now - timedelta(days=40)).timestamp()
            return now.timestamp() # Default for other paths

        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Test with 30 days cutoff
        old_files = get_old_files('/test_dir', 30)

        # Expect two files to be found: old_file.txt and another_old_file.log
        self.assertEqual(len(old_files), 2)
        self.assertTrue(any('old_file.txt' in f[0] for f in old_files))
        self.assertTrue(any('another_old_file.log' in f[0] for f in old_files))
        self.assertFalse(any('new_file.txt' in f[0] for f in old_files))

        # Test with 5 days cutoff (should find all three)
        old_files_5_days = get_old_files('/test_dir', 5)
        self.assertEqual(len(old_files_5_days), 3)

    @patch('os.remove')
    @patch('builtins.input', return_value='y')
    @patch('builtins.print')
    def test_delete_files_confirmed(self, mock_print, mock_input, mock_remove):
        # Mock rationale: os.remove simulates file deletion, builtins.input simulates user confirmation,
        # builtins.print captures output for verification. This prevents actual file deletion.
        files_to_delete = [
            ('/test_dir/file1.txt', (datetime.now() - timedelta(days=31)).timestamp()),
            ('/test_dir/file2.txt', (datetime.now() - timedelta(days=40)).timestamp())
        ]

        delete_files(files_to_delete, dry_run=False, force=False)

        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('/test_dir/file1.txt')
        mock_remove.assert_any_call('/test_dir/file2.txt')
        mock_input.assert_called_once_with('\nProceed with deletion? (y/N): ')
        self.assertTrue(any("Cataclysmic cleanup complete! 2 files purged." in call[0][0] for call in mock_print.call_args_list))

    @patch('os.remove')
    @patch('builtins.input', return_value='n')
    @patch('builtins.print')
    def test_delete_files_aborted(self, mock_print, mock_input, mock_remove):
        # Mock rationale: Same as above, but builtins.input simulates user declining deletion.
        files_to_delete = [
            ('/test_dir/file1.txt', (datetime.now() - timedelta(days=31)).timestamp())
        ]

        delete_files(files_to_delete, dry_run=False, force=False)

        mock_remove.assert_not_called()
        mock_input.assert_called_once_with('\nProceed with deletion? (y/N): ')
        self.assertTrue(any("Deletion aborted." in call[0][0] for call in mock_print.call_args_list))

    @patch('os.remove')
    @patch('builtins.print')
    def test_delete_files_dry_run(self, mock_print, mock_remove):
        # Mock rationale: os.remove ensures no deletion, builtins.print captures output.
        files_to_delete = [
            ('/test_dir/file1.txt', (datetime.now() - timedelta(days=31)).timestamp())
        ]

        delete_files(files_to_delete, dry_run=True, force=False)

        mock_remove.assert_not_called()
        self.assertTrue(any("Dry run complete. No files were deleted." in call[0][0] for call in mock_print.call_args_list))

    @patch('os.remove')
    @patch('builtins.input') # Should not be called in force mode
    @patch('builtins.print')
    def test_delete_files_force(self, mock_print, mock_input, mock_remove):
        # Mock rationale: os.remove simulates deletion, builtins.input ensures no prompt, builtins.print captures output.
        files_to_delete = [
            ('/test_dir/file1.txt', (datetime.now() - timedelta(days=31)).timestamp())
        ]

        delete_files(files_to_delete, dry_run=False, force=True)

        self.assertEqual(mock_remove.call_count, 1)
        mock_remove.assert_called_once_with('/test_dir/file1.txt')
        mock_input.assert_not_called()
        self.assertTrue(any("Cataclysmic cleanup complete! 1 files purged." in call[0][0] for call in mock_print.call_args_list))

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.input', return_value='y')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_integration(self, mock_parse_args, mock_print, mock_input, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: This tests the main function's argument parsing and flow.
        # argparse.ArgumentParser.parse_args simulates CLI arguments.
        # os.path.isdir, os.walk, os.path.getmtime, os.remove, builtins.input, builtins.print
        # are mocked to control file system interactions and user input, ensuring determinism.

        # Simulate CLI arguments: --path /test_dir --days 30
        mock_parse_args.return_value = MagicMock(
            path=['/test_dir'],
            days=30,
            dry_run=False,
            force=False
        )

        # Simulate directory structure and old file
        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.txt', 'new_file.txt'])
        ]
        now = datetime.now()
        def mock_getmtime_side_effect(path):
            if 'old_file.txt' in path:
                return (now - timedelta(days=31)).timestamp()
            elif 'new_file.txt' in path:
                return (now - timedelta(days=1)).timestamp()
            return now.timestamp()
        mock_getmtime.side_effect = mock_getmtime_side_effect

        main()

        mock_isdir.assert_called_once_with('/test_dir')
        mock_walk.assert_called_once_with('/test_dir')
        mock_getmtime.assert_any_call('/test_dir/old_file.txt')
        mock_getmtime.assert_any_call('/test_dir/new_file.txt')
        mock_input.assert_called_once()
        mock_remove.assert_called_once_with('/test_dir/old_file.txt')
        self.assertTrue(any("Cataclysmic cleanup complete! 1 files purged." in call[0][0] for call in mock_print.call_args_list))

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_path(self, mock_parse_args, mock_print, mock_isdir):
        # Mock rationale: Tests handling of invalid paths. os.path.isdir simulates path validity.
        mock_parse_args.return_value = MagicMock(
            path=['/invalid_dir'],
            days=30,
            dry_run=False,
            force=False
        )

        main()

        mock_isdir.assert_called_once_with('/invalid_dir')
        self.assertTrue(any("Error: Path '/invalid_dir' is not a valid directory. Skipping." in call[0][0] for call in mock_print.call_args_list))

if __name__ == '__main__':
    unittest.main()
