import unittest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime, timedelta

# Import the functions to be tested
from src.collector import find_dust_bunnies, clean_dust_bunnies

class TestCosmicDustBunnyCollector(unittest.TestCase):

    def setUp(self):
        # Define a fixed 'now' for deterministic time calculations
        self.mock_now = datetime(2023, 10, 26, 10, 0, 0) # October 26, 2023, 10:00:00
        # Patch datetime.now() to return our fixed time
        self.patcher_datetime_now = patch('src.collector.datetime')
        self.mock_datetime = self.patcher_datetime_now.start()
        self.mock_datetime.now.return_value = self.mock_now
        self.mock_datetime.fromtimestamp = datetime.fromtimestamp # Keep original for conversion
        self.mock_datetime.timedelta = timedelta # Keep original for timedelta

    def tearDown(self):
        self.patcher_datetime_now.stop()

    @patch('src.collector.os.path.isdir')
    @patch('src.collector.os.walk')
    @patch('src.collector.os.path.getmtime')
    def test_find_dust_bunnies_age_filter(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory structure and file modification times
        # to test age-based filtering without actual file system interaction.
        mock_isdir.return_value = True
        test_dir = '/test/data'

        # Simulate files:
        # file_old.txt: 60 days old (should be collected if age_days <= 60)
        # file_new.txt: 10 days old (should not be collected)
        # file_recent.txt: 29 days old (should not be collected if age_days > 29)

        # Calculate timestamps relative to mock_now
        old_timestamp = (self.mock_now - timedelta(days=60)).timestamp()
        new_timestamp = (self.mock_now - timedelta(days=10)).timestamp()
        recent_timestamp = (self.mock_now - timedelta(days=29)).timestamp()

        mock_walk.return_value = [
            (test_dir, [], ['file_old.txt', 'file_new.txt', 'file_recent.txt'])
        ]

        # Map file paths to their mocked modification times
        def getmtime_side_effect(path):
            if path == os.path.join(test_dir, 'file_old.txt'):
                return old_timestamp
            elif path == os.path.join(test_dir, 'file_new.txt'):
                return new_timestamp
            elif path == os.path.join(test_dir, 'file_recent.txt'):
                return recent_timestamp
            return self.mock_now.timestamp() # Default for others

        mock_getmtime.side_effect = getmtime_side_effect

        # Test 1: Age threshold 30 days (should find file_old.txt)
        bunnies = find_dust_bunnies(test_dir, 30)
        self.assertIn(os.path.join(test_dir, 'file_old.txt'), bunnies)
        self.assertNotIn(os.path.join(test_dir, 'file_new.txt'), bunnies)
        self.assertNotIn(os.path.join(test_dir, 'file_recent.txt'), bunnies)
        self.assertEqual(len(bunnies), 1)

        # Test 2: Age threshold 70 days (should find nothing, as file_old is 60 days)
        bunnies = find_dust_bunnies(test_dir, 70)
        self.assertEqual(len(bunnies), 0)

        # Test 3: Age threshold 20 days (should find file_old.txt)
        bunnies = find_dust_bunnies(test_dir, 20)
        self.assertIn(os.path.join(test_dir, 'file_old.txt'), bunnies)
        self.assertEqual(len(bunnies), 1)

    @patch('src.collector.os.path.isdir')
    @patch('src.collector.os.walk')
    @patch('src.collector.os.path.getmtime')
    def test_find_dust_bunnies_pattern_filter(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory structure, file modification times, and filenames
        # to test pattern-based filtering in conjunction with age without actual file system interaction.
        mock_isdir.return_value = True
        test_dir = '/test/data'

        # All files are older than 30 days for simplicity in this test
        old_timestamp = (self.mock_now - timedelta(days=60)).timestamp()

        mock_walk.return_value = [
            (test_dir, [], ['log_file.txt', 'data.csv', 'temp_report.log', 'image.jpg'])
        ]

        # All files will return old_timestamp
        mock_getmtime.return_value = old_timestamp

        # Test 1: Filter for '*.log'
        bunnies = find_dust_bunnies(test_dir, 30, patterns=['*.log'])
        self.assertIn(os.path.join(test_dir, 'temp_report.log'), bunnies)
        self.assertIn(os.path.join(test_dir, 'log_file.txt'), bunnies)
        self.assertEqual(len(bunnies), 2)

        # Test 2: Filter for '*.csv'
        bunnies = find_dust_bunnies(test_dir, 30, patterns=['*.csv'])
        self.assertIn(os.path.join(test_dir, 'data.csv'), bunnies)
        self.assertEqual(len(bunnies), 1)

        # Test 3: Filter for multiple patterns
        bunnies = find_dust_bunnies(test_dir, 30, patterns=['*.jpg', '*.csv'])
        self.assertIn(os.path.join(test_dir, 'image.jpg'), bunnies)
        self.assertIn(os.path.join(test_dir, 'data.csv'), bunnies)
        self.assertEqual(len(bunnies), 2)

        # Test 4: No matching patterns
        bunnies = find_dust_bunnies(test_dir, 30, patterns=['*.xyz'])
        self.assertEqual(len(bunnies), 0)

    @patch('src.collector.os.path.isdir')
    @patch('src.collector.os.walk')
    @patch('src.collector.os.path.getmtime')
    def test_find_dust_bunnies_no_patterns(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory structure and file modification times
        # to test behavior when no patterns are provided, ensuring all old files are collected.
        mock_isdir.return_value = True
        test_dir = '/test/data'

        old_timestamp = (self.mock_now - timedelta(days=60)).timestamp()
        new_timestamp = (self.mock_now - timedelta(days=10)).timestamp()

        mock_walk.return_value = [
            (test_dir, [], ['file_old.txt', 'file_new.txt', 'another_old.log'])
        ]

        def getmtime_side_effect(path):
            if 'old' in path:
                return old_timestamp
            else:
                return new_timestamp

        mock_getmtime.side_effect = getmtime_side_effect

        # Should find all files older than 30 days, regardless of extension
        bunnies = find_dust_bunnies(test_dir, 30, patterns=None)
        self.assertIn(os.path.join(test_dir, 'file_old.txt'), bunnies)
        self.assertIn(os.path.join(test_dir, 'another_old.log'), bunnies)
        self.assertNotIn(os.path.join(test_dir, 'file_new.txt'), bunnies)
        self.assertEqual(len(bunnies), 2)

    @patch('src.collector.os.path.isdir')
    @patch('src.collector.os.walk')
    @patch('src.collector.os.path.getmtime')
    def test_find_dust_bunnies_non_existent_directory(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Test error handling for non-existent directories without actual file system interaction.
        mock_isdir.return_value = False
        test_dir = '/non/existent/path'

        bunnies = find_dust_bunnies(test_dir, 30)
        self.assertEqual(len(bunnies), 0)
        mock_walk.assert_not_called() # os.walk should not be called if isdir is False

    @patch('src.collector.os.remove')
    @patch('builtins.print')
    def test_clean_dust_bunnies_dry_run(self, mock_print, mock_remove):
        # Mock rationale: Simulate printing output and ensure os.remove is NOT called
        # during a dry run, without actual file deletion.
        files = ['/path/to/file1.txt', '/path/to/file2.log']
        clean_dust_bunnies(files, dry_run=True)

        mock_remove.assert_not_called()
        mock_print.assert_any_call('\n[DRY RUN] Would delete:')
        mock_print.assert_any_call('  - /path/to/file1.txt')
        mock_print.assert_any_call('  - /path/to/file2.log')

    @patch('src.collector.os.remove')
    @patch('builtins.print')
    def test_clean_dust_bunnies_actual_delete(self, mock_print, mock_remove):
        # Mock rationale: Simulate actual deletion by checking if os.remove is called
        # for each file, and verify print statements, without actual file deletion.
        files = ['/path/to/file1.txt', '/path/to/file2.log']
        clean_dust_bunnies(files, dry_run=False)

        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('/path/to/file1.txt')
        mock_remove.assert_any_call('/path/to/file2.log')
        mock_print.assert_any_call('\nDeleting:')
        mock_print.assert_any_call('    Successfully deleted: /path/to/file1.txt')
        mock_print.assert_any_call('    Successfully deleted: /path/to/file2.log')

    @patch('src.collector.os.remove', side_effect=OSError('Permission denied'))
    @patch('builtins.print')
    def test_clean_dust_bunnies_delete_error(self, mock_print, mock_remove):
        # Mock rationale: Simulate an OSError during deletion to ensure error handling
        # and appropriate messages are printed, without actual file system errors.
        files = ['/path/to/file_unwritable.txt']
        clean_dust_bunnies(files, dry_run=False)

        mock_remove.assert_called_once_with('/path/to/file_unwritable.txt')
        mock_print.assert_any_call('\nDeleting:')
        mock_print.assert_any_call("    Error deleting '/path/to/file_unwritable.txt': Permission denied")

    @patch('builtins.print')
    def test_clean_dust_bunnies_no_files(self, mock_print):
        # Mock rationale: Test the scenario where no files are provided for cleaning
        # to ensure the correct message is printed.
        clean_dust_bunnies([], dry_run=True)
        mock_print.assert_called_once_with('No cosmic dust bunnies found to clean.')

    @patch('src.collector.os.path.isdir')
    @patch('src.collector.os.walk')
    @patch('src.collector.os.path.getmtime', side_effect=OSError('Access denied'))
    @patch('builtins.print')
    def test_find_dust_bunnies_getmtime_error(self, mock_print, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate an OSError when trying to get file modification time
        # to ensure the utility handles inaccessible files gracefully without crashing.
        mock_isdir.return_value = True
        test_dir = '/test/data'
        mock_walk.return_value = [
            (test_dir, [], ['inaccessible_file.txt'])
        ]

        bunnies = find_dust_bunnies(test_dir, 30)
        self.assertEqual(len(bunnies), 0)
        mock_print.assert_any_call("Warning: Could not access file '/test/data/inaccessible_file.txt': Access denied")
