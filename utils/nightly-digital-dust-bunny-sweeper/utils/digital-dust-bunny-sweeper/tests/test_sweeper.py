import unittest
import os
import time
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

# Add the src directory to the path to allow importing sweeper.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sweeper

class TestDigitalDustBunnySweeper(unittest.TestCase):

    # Mock rationale: We need a consistent 'current time' for age calculations to make tests deterministic.
    # This prevents tests from failing based on when they are run.
    MOCK_CURRENT_TIME = 1678886400.0 # March 15, 2023 12:00:00 PM UTC

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_dust_bunnies_age_only(self, mock_os_walk, mock_getmtime, mock_time):
        # Mock rationale: os.walk is mocked to simulate a file system structure without actually creating files.
        # This makes the test self-contained and fast.
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['old_file.txt', 'new_file.log', 'ancient_report.pdf']),
            ('/mock/dir/subdir', [], ['temp.tmp', 'another_old.bak'])
        ]

        # Mock rationale: os.path.getmtime is mocked to return specific modification times for each file.
        # This allows precise control over which files are considered 'old' based on the MOCK_CURRENT_TIME.
        # Files older than 30 days (MOCK_CURRENT_TIME - 30*24*60*60) should be found.
        # MOCK_CURRENT_TIME = 1678886400.0
        # 30 days ago = 1676380800.0 (approx Feb 13, 2023)
        mock_getmtime.side_effect = lambda x: {
            '/mock/dir/old_file.txt': self.MOCK_CURRENT_TIME - (31 * 24 * 60 * 60), # 31 days old
            '/mock/dir/new_file.log': self.MOCK_CURRENT_TIME - (10 * 24 * 60 * 60), # 10 days old
            '/mock/dir/ancient_report.pdf': self.MOCK_CURRENT_TIME - (100 * 24 * 60 * 60), # 100 days old
            '/mock/dir/subdir/temp.tmp': self.MOCK_CURRENT_TIME - (5 * 24 * 60 * 60), # 5 days old
            '/mock/dir/subdir/another_old.bak': self.MOCK_CURRENT_TIME - (40 * 24 * 60 * 60) # 40 days old
        }.get(x, self.MOCK_CURRENT_TIME)

        # Test with default age (30 days), no patterns
        bunnies = sweeper.find_dust_bunnies('/mock/dir', age_days=30, patterns=None)
        expected_bunnies = [
            '/mock/dir/old_file.txt',
            '/mock/dir/ancient_report.pdf',
            '/mock/dir/subdir/another_old.bak'
        ]
        self.assertCountEqual(bunnies, expected_bunnies)

        # Test with custom age (10 days), no patterns
        bunnies_10_days = sweeper.find_dust_bunnies('/mock/dir', age_days=10, patterns=None)
        expected_bunnies_10_days = [
            '/mock/dir/old_file.txt',
            '/mock/dir/new_file.log',
            '/mock/dir/ancient_report.pdf',
            '/mock/dir/subdir/another_old.bak'
        ]
        self.assertCountEqual(bunnies_10_days, expected_bunnies_10_days)

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_dust_bunnies_patterns_only(self, mock_os_walk, mock_getmtime, mock_time):
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['file.txt', 'log.log', 'temp.tmp', 'report.pdf', 'backup.bak'])
        ]
        # Mock rationale: When testing patterns only, age still applies with default 30 days. 
        # To effectively test patterns only, we make all files 'old enough' by setting their mtime far in the past.
        mock_getmtime.return_value = self.MOCK_CURRENT_TIME - (100 * 24 * 60 * 60) # All files 100 days old

        # Test with patterns only (default age 30 days, which all files satisfy)
        bunnies = sweeper.find_dust_bunnies('/mock/dir', patterns=['*.log', '*.tmp'])
        expected_bunnies = [
            '/mock/dir/log.log',
            '/mock/dir/temp.tmp'
        ]
        self.assertCountEqual(bunnies, expected_bunnies)

        bunnies_all_patterns = sweeper.find_dust_bunnies('/mock/dir', patterns=['*.log', '*.tmp', '*.bak', '*.txt'])
        expected_bunnies_all_patterns = [
            '/mock/dir/log.log',
            '/mock/dir/temp.tmp',
            '/mock/dir/backup.bak',
            '/mock/dir/file.txt'
        ]
        self.assertCountEqual(bunnies_all_patterns, expected_bunnies_all_patterns)

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_dust_bunnies_age_and_patterns(self, mock_os_walk, mock_getmtime, mock_time):
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['old.log', 'new.log', 'old.tmp', 'new.txt', 'ancient.bak'])
        ]

        # Mock rationale: Specific modification times to test combined age and pattern filtering.
        # Age threshold for 30 days: 1676380800.0
        mock_getmtime.side_effect = lambda x: {
            '/mock/dir/old.log': self.MOCK_CURRENT_TIME - (40 * 24 * 60 * 60), # Old log
            '/mock/dir/new.log': self.MOCK_CURRENT_TIME - (10 * 24 * 60 * 60), # New log
            '/mock/dir/old.tmp': self.MOCK_CURRENT_TIME - (50 * 24 * 60 * 60), # Old tmp
            '/mock/dir/new.txt': self.MOCK_CURRENT_TIME - (5 * 24 * 60 * 60),  # New txt
            '/mock/dir/ancient.bak': self.MOCK_CURRENT_TIME - (100 * 24 * 60 * 60) # Ancient bak
        }.get(x, self.MOCK_CURRENT_TIME)

        # Find files older than 30 days AND matching *.log or *.tmp
        bunnies = sweeper.find_dust_bunnies('/mock/dir', age_days=30, patterns=['*.log', '*.tmp'])
        expected_bunnies = [
            '/mock/dir/old.log',
            '/mock/dir/old.tmp'
        ]
        self.assertCountEqual(bunnies, expected_bunnies)

        # Find files older than 50 days AND matching *.bak
        bunnies_strict = sweeper.find_dust_bunnies('/mock/dir', age_days=50, patterns=['*.bak'])
        expected_bunnies_strict = [
            '/mock/dir/ancient.bak'
        ]
        self.assertCountEqual(bunnies_strict, expected_bunnies_strict)

    @patch('os.remove')
    def test_delete_files_dry_run(self, mock_os_remove):
        file_list = ['/path/to/file1.txt', '/path/to/file2.log']
        sweeper.delete_files(file_list, dry_run=True)

        # Mock rationale: os.remove is mocked to ensure no actual files are deleted during tests.
        # In dry-run mode, os.remove should not be called at all.
        mock_os_remove.assert_not_called()
        output = self.mock_stdout.getvalue()
        self.assertIn("[DRY RUN] Would delete: /path/to/file1.txt", output)
        self.assertIn("[DRY RUN] Would delete: /path/to/file2.log", output)
        self.assertIn("Found 2 digital dust bunnies. Run with --delete to actually sweep them.", output)

    @patch('os.remove')
    def test_delete_files_actual_delete(self, mock_os_remove):
        file_list = ['/path/to/file1.txt', '/path/to/file2.log']
        sweeper.delete_files(file_list, dry_run=False)

        # Mock rationale: os.remove is mocked to ensure no actual files are deleted during tests.
        # In actual delete mode, os.remove should be called for each file.
        self.assertEqual(mock_os_remove.call_count, len(file_list))
        mock_os_remove.assert_any_call('/path/to/file1.txt')
        mock_os_remove.assert_any_call('/path/to/file2.log')
        output = self.mock_stdout.getvalue()
        self.assertIn("Deleted: /path/to/file1.txt", output)
        self.assertIn("Deleted: /path/to/file2.log", output)
        self.assertIn("Successfully swept away 2 digital dust bunnies.", output)

    @patch('os.remove')
    def test_delete_files_no_bunnies(self, mock_os_remove):
        sweeper.delete_files([], dry_run=True)
        mock_os_remove.assert_not_called()
        output = self.mock_stdout.getvalue()
        self.assertIn("No digital dust bunnies found to sweep.", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.find_dust_bunnies', return_value=['/mock/file1.log', '/mock/file2.tmp'])
    @patch('sweeper.delete_files')
    def test_main_dry_run_default(self, mock_delete_files, mock_find_dust_bunnies, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to simulate command-line arguments.
        # This allows testing the main function's argument parsing logic without actual CLI interaction.
        mock_parse_args.return_value = MagicMock(path='/mock/dir', age=30, patterns=None, dry_run=False, delete=False)
        sweeper.main()
        mock_find_dust_bunnies.assert_called_once_with('/mock/dir', 30, None)
        mock_delete_files.assert_called_once_with(['/mock/file1.log', '/mock/file2.tmp'], dry_run=True)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.find_dust_bunnies', return_value=['/mock/file1.log'])
    @patch('sweeper.delete_files')
    def test_main_delete_mode(self, mock_delete_files, mock_find_dust_bunnies, mock_parse_args):
        mock_parse_args.return_value = MagicMock(path='/mock/dir', age=10, patterns=['*.log'], dry_run=False, delete=True)
        sweeper.main()
        mock_find_dust_bunnies.assert_called_once_with('/mock/dir', 10, ['*.log'])
        mock_delete_files.assert_called_once_with(['/mock/file1.log'], dry_run=False)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_delete_and_dry_run_error(self, mock_sys_exit, mock_parse_args):
        mock_parse_args.return_value = MagicMock(path='/mock/dir', age=30, patterns=None, dry_run=True, delete=True)
        sweeper.main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Error: Cannot use --delete and --dry-run simultaneously. Choose one.", output)
        mock_sys_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
