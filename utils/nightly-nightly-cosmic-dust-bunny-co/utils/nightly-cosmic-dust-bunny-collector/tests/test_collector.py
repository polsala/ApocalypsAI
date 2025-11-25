import unittest
import os
import time
import argparse
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions to be tested
from src.collector import find_dust_bunnies, main

class TestCosmicDustBunnyCollector(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_basic(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate directory existence.
        # os.walk is mocked to simulate file system traversal without actual disk access.
        # os.path.getmtime is mocked to control file modification times for age filtering.

        mock_isdir.return_value = True
        
        # Simulate a directory structure
        # /test_dir/
        #   file1.log (old)
        #   file2.tmp (new)
        #   file3.txt (old, but wrong pattern)
        #   subdir/
        #     file4.log (old)

        # Mock os.walk to return a specific directory structure
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.log', 'file2.tmp', 'file3.txt']),
            ('/test_dir/subdir', [], ['file4.log'])
        ]

        # Define current time and age threshold
        now = time.time()
        age_days = 7
        old_timestamp = now - (age_days + 1) * 24 * 60 * 60 # Older than threshold
        new_timestamp = now - (age_days - 1) * 24 * 60 * 60 # Newer than threshold

        # Mock os.path.getmtime for each file
        def mock_getmtime_side_effect(filepath):
            if 'file1.log' in filepath:
                return old_timestamp
            elif 'file2.tmp' in filepath:
                return new_timestamp
            elif 'file3.txt' in filepath:
                return old_timestamp
            elif 'file4.log' in filepath:
                return old_timestamp
            return now # Default for any other unexpected file
        
        mock_getmtime.side_effect = mock_getmtime_side_effect

        paths = ['/test_dir']
        patterns = ['*.log', '*.tmp']

        bunnies = find_dust_bunnies(paths, patterns, age_days)
        
        # Expected: file1.log (old, matches pattern), file4.log (old, matches pattern)
        # Not expected: file2.tmp (new), file3.txt (wrong pattern)
        self.assertIn(os.path.join('/test_dir', 'file1.log'), bunnies)
        self.assertIn(os.path.join('/test_dir/subdir', 'file4.log'), bunnies)
        self.assertNotIn(os.path.join('/test_dir', 'file2.tmp'), bunnies)
        self.assertNotIn(os.path.join('/test_dir', 'file3.txt'), bunnies)
        self.assertEqual(len(bunnies), 2)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_no_match(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Same as above, simulating no files matching criteria.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['file.txt', 'another.doc'])
        ]
        mock_getmtime.return_value = time.time() - (10 * 24 * 60 * 60) # All files are old

        paths = ['/test_dir']
        patterns = ['*.log']
        age_days = 5

        bunnies = find_dust_bunnies(paths, patterns, age_days)
        self.assertEqual(len(bunnies), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_non_existent_path(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to return False for a non-existent path.
        mock_isdir.return_value = False # Simulate path does not exist

        paths = ['/non_existent_dir']
        patterns = ['*.log']
        age_days = 7

        # We expect a warning print, but no error, and an empty list
        with patch('builtins.print') as mock_print:
            bunnies = find_dust_bunnies(paths, patterns, age_days)
            self.assertEqual(len(bunnies), 0)
            mock_print.assert_called_with("Warning: Path '/non_existent_dir' is not a valid directory. Skipping.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_multiple_paths(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulating multiple root directories for scanning.
        mock_isdir.return_value = True
        
        now = time.time()
        old_timestamp = now - (10 * 24 * 60 * 60) # Older than 7 days

        # Simulate files in two different paths
        mock_walk.side_effect = [
            ('/path1', [], ['file1.log', 'file2.tmp']),
            ('/path2', [], ['file3.log'])
        ]
        
        def mock_getmtime_side_effect(filepath):
            return old_timestamp
        mock_getmtime.side_effect = mock_getmtime_side_effect

        paths = ['/path1', '/path2']
        patterns = ['*.log']
        age_days = 7

        bunnies = find_dust_bunnies(paths, patterns, age_days)
        self.assertIn(os.path.join('/path1', 'file1.log'), bunnies)
        self.assertIn(os.path.join('/path2', 'file3.log'), bunnies)
        self.assertNotIn(os.path.join('/path1', 'file2.tmp'), bunnies) # Does not match pattern
        self.assertEqual(len(bunnies), 2)

    @patch('src.collector.find_dust_bunnies')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_dry_run(self, mock_parse_args, mock_print, mock_find_dust_bunnies):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control CLI arguments.
        # builtins.print is mocked to capture output without printing to console.
        # find_dust_bunnies is mocked to control the list of files found, isolating main's logic.

        mock_args = MagicMock()
        mock_args.path = ['/test_dir']
        mock_args.patterns = ['*.log']
        mock_args.age = 7
        mock_args.dry_run = True
        mock_args.delete = False
        mock_parse_args.return_value = mock_args

        mock_find_dust_bunnies.return_value = [
            os.path.join('/test_dir', 'old.log'),
            os.path.join('/test_dir', 'another_old.log')
        ]

        main()

        mock_find_dust_bunnies.assert_called_once_with(['/test_dir'], ['*.log'], 7)
        mock_print.assert_any_call("\n(Dry run complete. No files were deleted.)")
        mock_print.assert_any_call(f"Found 2 cosmic dust bunnies:")
        mock_print.assert_any_call(f"  - {os.path.join('/test_dir', 'old.log')}")
        mock_print.assert_any_call(f"  - {os.path.join('/test_dir', 'another_old.log')}")

    @patch('src.collector.find_dust_bunnies')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.remove')
    def test_main_delete_mode(self, mock_remove, mock_parse_args, mock_print, mock_find_dust_bunnies):
        # Mock rationale: os.remove is mocked to prevent actual file deletion during tests.
        # Other mocks are for controlling arguments, output, and found files.

        mock_args = MagicMock()
        mock_args.path = ['/test_dir']
        mock_args.patterns = ['*.log']
        mock_args.age = 7
        mock_args.dry_run = False
        mock_args.delete = True
        mock_parse_args.return_value = mock_args

        dust_bunnies_to_delete = [
            os.path.join('/test_dir', 'old.log'),
            os.path.join('/test_dir', 'another_old.log')
        ]
        mock_find_dust_bunnies.return_value = dust_bunnies_to_delete

        main()

        mock_find_dust_bunnies.assert_called_once_with(['/test_dir'], ['*.log'], 7)
        mock_remove.assert_called_with(dust_bunnies_to_delete[0])
        mock_remove.assert_called_with(dust_bunnies_to_delete[1])
        self.assertEqual(mock_remove.call_count, len(dust_bunnies_to_delete))
        mock_print.assert_any_call("\nInitiating cosmic dust bunny purge...")
        mock_print.assert_any_call(f"  Deleted: {dust_bunnies_to_delete[0]}")
        mock_print.assert_any_call(f"  Deleted: {dust_bunnies_to_delete[1]}")
        mock_print.assert_any_call(f"\nPurge complete. {len(dust_bunnies_to_delete)} cosmic dust bunnies removed. 🚀")

    @patch('src.collector.find_dust_bunnies')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_bunnies_found(self, mock_parse_args, mock_print, mock_find_dust_bunnies):
        # Mock rationale: Simulating a scenario where no files match the criteria.
        mock_args = MagicMock()
        mock_args.path = ['/test_dir']
        mock_args.patterns = ['*.log']
        mock_args.age = 7
        mock_args.dry_run = True
        mock_args.delete = False
        mock_parse_args.return_value = mock_args

        mock_find_dust_bunnies.return_value = [] # No bunnies found

        main()

        mock_find_dust_bunnies.assert_called_once_with(['/test_dir'], ['*.log'], 7)
        mock_print.assert_any_call("\nNo cosmic dust bunnies found. Your system is sparkling clean! ✨")
        # Ensure no deletion messages
        self.assertFalse(any("Deleted:" in call.args[0] for call in mock_print.call_args_list))

    @patch('argparse.ArgumentParser.parse_args')
    @patch('argparse.ArgumentParser.error')
    def test_main_delete_and_dry_run_error(self, mock_error, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.error is mocked to catch the expected error.
        mock_args = MagicMock()
        mock_args.path = ['/test_dir']
        mock_args.patterns = ['*.log']
        mock_args.age = 7
        mock_args.dry_run = True
        mock_args.delete = True
        mock_parse_args.return_value = mock_args

        main()
        mock_error.assert_called_once_with("Cannot use --delete and --dry-run together. Choose one.")

    @patch('src.collector.find_dust_bunnies')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.remove')
    def test_main_delete_mode_with_os_error(self, mock_remove, mock_parse_args, mock_print, mock_find_dust_bunnies):
        # Mock rationale: os.remove is mocked to raise an OSError, simulating permission issues or similar.
        mock_args = MagicMock()
        mock_args.path = ['/test_dir']
        mock_args.patterns = ['*.log']
        mock_args.age = 7
        mock_args.dry_run = False
        mock_args.delete = True
        mock_parse_args.return_value = mock_args

        dust_bunnies_to_delete = [
            os.path.join('/test_dir', 'old.log'),
            os.path.join('/test_dir', 'another_old.log')
        ]
        mock_find_dust_bunnies.return_value = dust_bunnies_to_delete

        # Make the first remove succeed, the second fail
        mock_remove.side_effect = [None, OSError("Permission denied")]

        main()

        mock_find_dust_bunnies.assert_called_once_with(['/test_dir'], ['*.log'], 7)
        self.assertEqual(mock_remove.call_count, 2)
        mock_print.assert_any_call(f"  Deleted: {dust_bunnies_to_delete[0]}")
        mock_print.assert_any_call(f"  Error deleting '{dust_bunnies_to_delete[1]}': Permission denied")
        mock_print.assert_any_call(f"\nPurge complete. 1 cosmic dust bunnies removed. 🚀") # Only one was successfully deleted

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_getmtime_error(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: os.path.getmtime is mocked to raise an OSError, simulating unreadable file metadata.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.log'])
        ]
        mock_getmtime.side_effect = OSError("Cannot access file metadata")

        paths = ['/test_dir']
        patterns = ['*.log']
        age_days = 7

        with patch('builtins.print') as mock_print:
            bunnies = find_dust_bunnies(paths, patterns, age_days)
            self.assertEqual(len(bunnies), 0) # No bunnies should be added if mtime fails
            mock_print.assert_called_with(f"Warning: Could not get modification time for '{os.path.join('/test_dir', 'file1.log')}': Cannot access file metadata")


if __name__ == '__main__':
    unittest.main()
