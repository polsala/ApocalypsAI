import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Adjust sys.path to allow importing from the src directory
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from dust_collector import collect_dust, format_size

class TestCosmicDustCollector(unittest.TestCase):

    # Mock rationale: We need to control the file system structure and file modification times
    # to ensure deterministic tests for file age and pattern matching without
    # actually creating files on disk or relying on the host system's clock.
    # `os.walk` and `os.path.getmtime` are key functions for this.
    # `time.time` is mocked to fix the "current" time for consistent age calculations.

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.stat')
    @patch('os.walk')
    def test_collect_dust_basic_age_filter(self, mock_os_walk, mock_os_stat, mock_os_isdir, mock_os_getmtime, mock_time_time):
        # Mock rationale: Fix current time to a known point for consistent age calculations.
        fixed_current_time = datetime(2023, 3, 15, 10, 0, 0).timestamp()
        mock_time_time.return_value = fixed_current_time

        # Mock rationale: Simulate a valid directory for the scan path.
        mock_os_isdir.return_value = True

        # Mock rationale: Simulate file modification times.
        # Files older than 30 days from fixed_current_time (Feb 13, 2023) should be picked up.
        # File 1: Jan 15, 2023 (older)
        # File 2: Feb 14, 2023 (newer)
        # File 3: Mar 10, 2023 (newer)
        file_mtimes = {
            '/test_repo/old_log.log': datetime(2023, 1, 15, 9, 0, 0).timestamp(),
            '/test_repo/recent_file.txt': datetime(2023, 2, 14, 9, 0, 0).timestamp(),
            '/test_repo/another_recent.py': datetime(2023, 3, 10, 9, 0, 0).timestamp(),
        }
        mock_os_getmtime.side_effect = lambda p: file_mtimes.get(p, fixed_current_time)

        # Mock rationale: Simulate file system structure and contents.
        mock_os_walk.return_value = [
            ('/test_repo', [], ['old_log.log', 'recent_file.txt', 'another_recent.py'])
        ]

        # Mock rationale: Simulate os.stat for file size.
        mock_os_stat.side_effect = lambda p: MagicMock(st_mtime=file_mtimes.get(p, fixed_current_time), st_size=100)

        dust = collect_dust('/test_repo', age_days=30)

        self.assertEqual(len(dust), 1)
        self.assertEqual(dust[0]['path'], '/test_repo/old_log.log')
        self.assertEqual(dust[0]['size'], 100)
        self.assertAlmostEqual(dust[0]['mtime'], file_mtimes['/test_repo/old_log.log'])

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.stat')
    @patch('os.walk')
    def test_collect_dust_with_patterns(self, mock_os_walk, mock_os_stat, mock_os_isdir, mock_os_getmtime, mock_time_time):
        # Mock rationale: Fix current time to a known point for consistent age calculations.
        fixed_current_time = datetime(2023, 3, 15, 10, 0, 0).timestamp()
        mock_time_time.return_value = fixed_current_time

        # Mock rationale: Simulate a valid directory for the scan path.
        mock_os_isdir.return_value = True

        # Mock rationale: Simulate file modification times. All files are older than 30 days.
        mtime_old = datetime(2023, 1, 1, 9, 0, 0).timestamp()
        file_mtimes = {
            '/test_repo/data.log': mtime_old,
            '/test_repo/temp_file.tmp': mtime_old,
            '/test_repo/important.txt': mtime_old,
            '/test_repo/backup/config.bak': mtime_old,
        }
        mock_os_getmtime.side_effect = lambda p: file_mtimes.get(p, fixed_current_time)

        # Mock rationale: Simulate file system structure and contents.
        mock_os_walk.return_value = [
            ('/test_repo', ['backup'], ['data.log', 'temp_file.tmp', 'important.txt']),
            ('/test_repo/backup', [], ['config.bak'])
        ]

        # Mock rationale: Simulate os.stat for file size.
        mock_os_stat.side_effect = lambda p: MagicMock(st_mtime=file_mtimes.get(p, fixed_current_time), st_size=100)

        # Test with specific patterns
        dust = collect_dust('/test_repo', age_days=30, patterns=['*.log', '*.tmp'])

        self.assertEqual(len(dust), 2)
        paths = sorted([f['path'] for f in dust])
        self.assertEqual(paths, ['/test_repo/data.log', '/test_repo/temp_file.tmp'])

        # Test with a different pattern
        dust_bak = collect_dust('/test_repo', age_days=30, patterns=['*.bak'])
        self.assertEqual(len(dust_bak), 1)
        self.assertEqual(dust_bak[0]['path'], '/test_repo/backup/config.bak')

        # Test with no patterns (should pick up all old files)
        dust_all = collect_dust('/test_repo', age_days=30, patterns=[])
        self.assertEqual(len(dust_all), 4)
        paths_all = sorted([f['path'] for f in dust_all])
        self.assertEqual(paths_all, [
            '/test_repo/backup/config.bak',
            '/test_repo/data.log',
            '/test_repo/important.txt',
            '/test_repo/temp_file.tmp'
        ])

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.stat')
    @patch('os.walk')
    def test_collect_dust_with_exclude_dirs(self, mock_os_walk, mock_os_stat, mock_os_isdir, mock_os_getmtime, mock_time_time):
        # Mock rationale: Fix current time to a known point for consistent age calculations.
        fixed_current_time = datetime(2023, 3, 15, 10, 0, 0).timestamp()
        mock_time_time.return_value = fixed_current_time

        # Mock rationale: Simulate a valid directory for the scan path.
        mock_os_isdir.return_value = True

        # Mock rationale: Simulate file modification times. All files are old.
        mtime_old = datetime(2023, 1, 1, 9, 0, 0).timestamp()
        file_mtimes = {
            '/test_repo/file.log': mtime_old,
            '/test_repo/temp/temp.txt': mtime_old,
            '/test_repo/.git/config': mtime_old,
            '/test_repo/node_modules/package.json': mtime_old,
            '/test_repo/build/output.js': mtime_old,
        }
        mock_os_getmtime.side_effect = lambda p: file_mtimes.get(p, fixed_current_time)

        # Mock rationale: Simulate file system structure and contents.
        mock_os_walk.return_value = [
            ('/test_repo', ['temp', '.git', 'node_modules', 'build'], ['file.log']),
            ('/test_repo/temp', [], ['temp.txt']),
            ('/test_repo/.git', [], ['config']),
            ('/test_repo/node_modules', [], ['package.json']),
            ('/test_repo/build', [], ['output.js']),
        ]

        # Test excluding .git and node_modules
        dust = collect_dust('/test_repo', age_days=30, exclude_dirs=['.git', 'node_modules'])

        self.assertEqual(len(dust), 3)
        paths = sorted([f['path'] for f in dust])
        self.assertEqual(paths, [
            '/test_repo/build/output.js',
            '/test_repo/file.log',
            '/test_repo/temp/temp.txt'
        ])

        # Test excluding 'temp' and 'build'
        dust_alt_exclude = collect_dust('/test_repo', age_days=30, exclude_dirs=['temp', 'build'])
        self.assertEqual(len(dust_alt_exclude), 3)
        paths_alt_exclude = sorted([f['path'] for f in dust_alt_exclude])
        self.assertEqual(paths_alt_exclude, [
            '/test_repo/.git/config',
            '/test_repo/file.log',
            '/test_repo/node_modules/package.json'
        ])

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.stat')
    @patch('os.walk')
    def test_collect_dust_empty_directory(self, mock_os_walk, mock_os_stat, mock_os_isdir, mock_os_getmtime, mock_time_time):
        # Mock rationale: Fix current time to a known point for consistent age calculations.
        fixed_current_time = datetime(2023, 3, 15, 10, 0, 0).timestamp()
        mock_time_time.return_value = fixed_current_time

        # Mock rationale: Simulate a valid directory for the scan path.
        mock_os_isdir.return_value = True

        # Mock rationale: Simulate an empty directory.
        mock_os_walk.return_value = [
            ('/test_repo', [], [])
        ]
        mock_os_stat.side_effect = FileNotFoundError # No files to stat

        dust = collect_dust('/test_repo', age_days=30)
        self.assertEqual(len(dust), 0)

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.stat')
    @patch('os.walk')
    def test_collect_dust_non_existent_path(self, mock_os_walk, mock_os_stat, mock_os_isdir, mock_os_getmtime, mock_time_time):
        # Mock rationale: Simulate an invalid directory for the scan path.
        mock_os_isdir.return_value = False
        
        # Mock rationale: Fix current time (though not strictly needed for this test, good practice).
        mock_time_time.return_value = datetime(2023, 3, 15, 10, 0, 0).timestamp()

        dust = collect_dust('/non_existent_repo', age_days=30)
        self.assertEqual(len(dust), 0) # Should return empty list and print error

    def test_format_size(self):
        self.assertEqual(format_size(0), "0 B")
        self.assertEqual(format_size(100), "100 B")
        self.assertEqual(format_size(1023), "1023 B")
        self.assertEqual(format_size(1024), "1.0 KB")
        self.assertEqual(format_size(1536), "1.5 KB")
        self.assertEqual(format_size(1024 * 1024 - 1), "1024.0 KB") # Just under 1MB
        self.assertEqual(format_size(1024 * 1024), "1.0 MB")
        self.assertEqual(format_size(1024 * 1024 * 1024), "1.0 GB")
        self.assertEqual(format_size(1024 * 1024 * 1024 * 1.5), "1.5 GB")


if __name__ == '__main__':
    unittest.main()
