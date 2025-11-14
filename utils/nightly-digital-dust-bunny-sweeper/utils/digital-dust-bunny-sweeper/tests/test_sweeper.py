import unittest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime, timedelta

# Import the functions to be tested
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sweeper import find_dust_bunnies, generate_report

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Define a fixed 'now' for deterministic age calculations
        self.mock_now = datetime(2024, 7, 20, 10, 0, 0) # July 20, 2024
        self.age_threshold_days = 90
        self.age_threshold_timestamp = (self.mock_now - timedelta(days=self.age_threshold_days)).timestamp()

    @patch('sweeper.datetime')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies_empty_dir(self, mock_os_walk, mock_os_isdir, mock_os_getmtime, mock_datetime):
        # Mock rationale: Simulate a directory structure with an empty directory.
        # os.walk: Controls the directory traversal, returning predefined tuples of (dirpath, dirnames, filenames).
        # os.path.isdir: Confirms a path is a directory, crucial for the empty directory check.
        # os.path.getmtime: Not directly called for empty dir detection, but mocked for consistency.
        # datetime: Fixes the 'current time' for age calculations, ensuring deterministic results.

        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp # Allow real conversion for formatting

        mock_os_walk.return_value = [
            ('/root', ['empty_folder', 'non_empty_folder'], []), # root dir
            ('/root/empty_folder', [], []), # empty folder
            ('/root/non_empty_folder', [], ['file.txt']) # non-empty folder
        ]
        mock_os_isdir.side_effect = lambda p: p in ['/root', '/root/empty_folder', '/root/non_empty_folder']
        mock_os_getmtime.return_value = self.mock_now.timestamp() # Files are new, not relevant for empty dir test

        result = find_dust_bunnies('/root', self.age_threshold_days)
        self.assertIn('/root/empty_folder', result['empty_dirs'])
        self.assertEqual(len(result['old_files']), 0)
        self.assertEqual(len(result['empty_dirs']), 1)

    @patch('sweeper.datetime')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies_old_files(self, mock_os_walk, mock_os_isdir, mock_os_getmtime, mock_datetime):
        # Mock rationale: Simulate a directory with old files matching default extensions.
        # os.walk: Provides directory and file names for traversal.
        # os.path.isdir: Confirms paths are directories.
        # os.path.getmtime: Returns specific modification times to make files appear 'old' or 'new'.
        # datetime: Fixes the 'current time' for age calculations.

        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp

        old_file_timestamp = (self.mock_now - timedelta(days=self.age_threshold_days + 1)).timestamp()
        new_file_timestamp = (self.mock_now - timedelta(days=self.age_threshold_days - 1)).timestamp()

        mock_os_walk.return_value = [
            ('/root', [], ['old.log', 'new.log', 'temp.tmp', 'recent.txt', 'another.bak'])
        ]
        mock_os_isdir.return_value = True
        mock_os_getmtime.side_effect = {
            '/root/old.log': old_file_timestamp,
            '/root/new.log': new_file_timestamp,
            '/root/temp.tmp': old_file_timestamp,
            '/root/recent.txt': old_file_timestamp, # .txt is not a default extension, should be ignored
            '/root/another.bak': old_file_timestamp
        }.get

        result = find_dust_bunnies('/root', self.age_threshold_days)
        self.assertEqual(len(result['empty_dirs']), 0)
        self.assertEqual(len(result['old_files']), 3) # old.log, temp.tmp, another.bak
        self.assertIn(('/root/old.log', (self.mock_now - timedelta(days=self.age_threshold_days + 1)).strftime('%Y-%m-%d')), result['old_files'])
        self.assertIn(('/root/temp.tmp', (self.mock_now - timedelta(days=self.age_threshold_days + 1)).strftime('%Y-%m-%d')), result['old_files'])
        self.assertIn(('/root/another.bak', (self.mock_now - timedelta(days=self.age_threshold_days + 1)).strftime('%Y-%m-%d')), result['old_files'])
        self.assertNotIn(('/root/new.log', (self.mock_now - timedelta(days=self.age_threshold_days - 1)).strftime('%Y-%m-%d')), result['old_files'])
        self.assertNotIn(('/root/recent.txt', (self.mock_now - timedelta(days=self.age_threshold_days + 1)).strftime('%Y-%m-%d')), result['old_files'])

    @patch('sweeper.datetime')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies_custom_extensions(self, mock_os_walk, mock_os_isdir, mock_os_getmtime, mock_datetime):
        # Mock rationale: Test with a custom list of file extensions to ensure filtering works as expected.
        # os.walk, os.path.isdir, os.path.getmtime, datetime: Same as above, controlling file system state and time.

        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp

        old_file_timestamp = (self.mock_now - timedelta(days=self.age_threshold_days + 1)).timestamp()

        mock_os_walk.return_value = [
            ('/root', [], ['report.csv', 'data.json', 'old.log'])
        ]
        mock_os_isdir.return_value = True
        mock_os_getmtime.side_effect = {
            '/root/report.csv': old_file_timestamp,
            '/root/data.json': old_file_timestamp,
            '/root/old.log': old_file_timestamp
        }.get

        result = find_dust_bunnies('/root', self.age_threshold_days, file_extensions=['.csv', '.json'])
        self.assertEqual(len(result['empty_dirs']), 0)
        self.assertEqual(len(result['old_files']), 2) # report.csv, data.json
        self.assertIn(('/root/report.csv', (self.mock_now - timedelta(days=self.age_threshold_days + 1)).strftime('%Y-%m-%d')), result['old_files'])
        self.assertIn(('/root/data.json', (self.mock_now - timedelta(days=self.age_threshold_days + 1)).strftime('%Y-%m-%d')), result['old_files'])
        self.assertNotIn(('/root/old.log', (self.mock_now - timedelta(days=self.age_threshold_days + 1)).strftime('%Y-%m-%d')), result['old_files'])

    def test_generate_report_with_findings(self):
        # Mock rationale: Test the report generation with predefined findings. This function is pure and doesn't interact with OS/time.

        dust_bunnies = {
            'empty_dirs': ['/path/to/empty_dir1', '/path/to/empty_dir2'],
            'old_files': [
                ('/path/to/old_file.log', '2023-01-01'),
                ('/path/to/another_old.tmp', '2023-02-15')
            ]
        }
        report = generate_report(dust_bunnies, '/path/to/scan')

        self.assertIn('✨ Initiating Cosmic Debris Scan for: /path/to/scan ✨', report)
        self.assertIn('🌌 Empty Voids Discovered (Empty Directories):', report)
        self.assertIn('  - /path/to/empty_dir1', report)
        self.assertIn('⏳ Ancient Relics Unearthed (Old Files):', report)
        self.assertIn('  - /path/to/old_file.log (Last modified: 2023-01-01)', report)
        self.assertIn('🧹 A clean sweep for your cosmic data-verse! 🧹', report)

    def test_generate_report_no_findings(self):
        # Mock rationale: Test the report generation when no dust bunnies are found. This function is pure and doesn't interact with OS/time.

        dust_bunnies = {
            'empty_dirs': [],
            'old_files': []
        }
        report = generate_report(dust_bunnies, '/path/to/scan')

        self.assertIn('🌌 No Empty Voids detected. Your space is efficiently utilized!', report)
        self.assertIn('⏳ No Ancient Relics found. Your files are spry and current!', report)
        self.assertIn('🧹 A clean sweep for your cosmic data-verse! 🧹', report)

if __name__ == '__main__':
    unittest.main()
