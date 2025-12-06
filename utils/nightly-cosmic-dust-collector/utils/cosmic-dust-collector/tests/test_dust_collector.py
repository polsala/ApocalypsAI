import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from datetime import datetime, timedelta
import time

# Add the src directory to the path to allow importing dust_collector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import dust_collector

class TestCosmicDustCollector(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_untracked_files_success(self, mock_subprocess_run):
        # Mock rationale: Simulate git command success and output untracked files.
        mock_subprocess_run.return_value = MagicMock(
            stdout='file1.txt\0dir/file2.log\0',
            stderr='',
            returncode=0,
            check=True
        )
        files = dust_collector.get_untracked_files('.')
        self.assertEqual(files, ['file1.txt', 'dir/file2.log'])
        mock_subprocess_run.assert_called_once_with(
            ['git', 'ls-files', '--others', '--exclude-standard', '-z'],
            cwd='.',
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    def test_get_untracked_files_no_git(self, mock_subprocess_run):
        # Mock rationale: Simulate git command not found.
        mock_subprocess_run.side_effect = FileNotFoundError
        with patch('builtins.print') as mock_print:
            files = dust_collector.get_untracked_files('.')
            self.assertEqual(files, [])
            mock_print.assert_called_with("Error: Git command not found. Please ensure Git is installed and in your PATH.")

    @patch('subprocess.run')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_find_dust_basic(self, mock_getmtime, mock_getsize, mock_isfile, mock_exists, mock_subprocess_run):
        # Mock rationale: Simulate a repository with untracked files and control their properties.
        mock_subprocess_run.return_value = MagicMock(
            stdout='temp_file.log\0large_old_data.bin\0recent_small.txt\0',
            stderr='',
            returncode=0,
            check=True
        )

        # Simulate file properties
        # temp_file.log: 1MB, 10 days old
        # large_old_data.bin: 20MB, 60 days old
        # recent_small.txt: 10KB, 1 day old

        now = datetime.now()
        file_times = {
            './temp_file.log': (now - timedelta(days=10)).timestamp(),
            './large_old_data.bin': (now - timedelta(days=60)).timestamp(),
            './recent_small.txt': (now - timedelta(days=1)).timestamp(),
        }
        file_sizes = {
            './temp_file.log': 1 * 1024 * 1024, # 1MB
            './large_old_data.bin': 20 * 1024 * 1024, # 20MB
            './recent_small.txt': 10 * 1024, # 10KB
        }

        mock_getmtime.side_effect = lambda f: file_times.get(f, time.time())
        mock_getsize.side_effect = lambda f: file_sizes.get(f, 0)

        # Test 1: No filters
        dust = dust_collector.find_dust('.', 0, timedelta(seconds=0))
        self.assertEqual(len(dust), 3)
        self.assertIn(('./temp_file.log', file_sizes['./temp_file.log'], datetime.fromtimestamp(file_times['./temp_file.log'])), dust)

        # Test 2: Min size 2MB
        dust = dust_collector.find_dust('.', dust_collector.parse_size('2M'), timedelta(seconds=0))
        self.assertEqual(len(dust), 1)
        self.assertIn(('./large_old_data.bin', file_sizes['./large_old_data.bin'], datetime.fromtimestamp(file_times['./large_old_data.bin'])), dust)

        # Test 3: Older than 15 days
        dust = dust_collector.find_dust('.', 0, timedelta(days=15))
        self.assertEqual(len(dust), 1)
        self.assertIn(('./large_old_data.bin', file_sizes['./large_old_data.bin'], datetime.fromtimestamp(file_times['./large_old_data.bin'])), dust)

        # Test 4: Min size 2MB AND Older than 15 days
        dust = dust_collector.find_dust('.', dust_collector.parse_size('2M'), timedelta(days=15))
        self.assertEqual(len(dust), 1)
        self.assertIn(('./large_old_data.bin', file_sizes['./large_old_data.bin'], datetime.fromtimestamp(file_times['./large_old_data.bin'])), dust)

        # Test 5: No files match
        dust = dust_collector.find_dust('.', dust_collector.parse_size('100M'), timedelta(days=100))
        self.assertEqual(len(dust), 0)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('os.remove')
    @patch('os.path.getmtime', return_value=(datetime.now() - timedelta(days=30)).timestamp())
    @patch('os.path.getsize', return_value=1000)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run') # This will be the first argument to the method
    def test_main_dry_run(self, mock_subprocess_run, mock_exists, mock_isfile, mock_getsize, mock_getmtime, mock_remove, mock_print, mock_parse_args):
        # Mock rationale: Simulate a dry run execution of the main function.
        mock_parse_args.return_value = MagicMock(
            path='.', dry_run=True, min_size='0', older_than='0d', delete=False
        )
        mock_subprocess_run.return_value = MagicMock(
            stdout='dry_run_file.txt\0',
            stderr='',
            returncode=0,
            check=True
        )

        dust_collector.main()

        mock_remove.assert_not_called() # No deletion in dry run
        mock_print.assert_any_call(unittest.mock.ANY)
        mock_print.assert_any_call("This was a dry run. No files were deleted. Use --delete to remove them.")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('os.remove')
    @patch('os.path.getmtime', return_value=(datetime.now() - timedelta(days=30)).timestamp())
    @patch('os.path.getsize', return_value=1000)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run') # This will be the first argument to the method
    def test_main_delete_mode(self, mock_subprocess_run, mock_exists, mock_isfile, mock_getsize, mock_getmtime, mock_remove, mock_print, mock_parse_args):
        # Mock rationale: Simulate a deletion execution of the main function.
        mock_parse_args.return_value = MagicMock(
            path='.', dry_run=False, min_size='0', older_than='0d', delete=True
        )
        mock_subprocess_run.return_value = MagicMock(
            stdout='file_to_delete.tmp\0',
            stderr='',
            returncode=0,
            check=True
        )

        dust_collector.main()

        mock_remove.assert_called_once_with('./file_to_delete.tmp') # Deletion should occur
        mock_print.assert_any_call(unittest.mock.ANY)
        mock_print.assert_any_call("Cosmic dust successfully swept away!")

    def test_parse_size(self):
        self.assertEqual(dust_collector.parse_size('100K'), 100 * 1024)
        self.assertEqual(dust_collector.parse_size('5M'), 5 * 1024 * 1024)
        self.assertEqual(dust_collector.parse_size('1G'), 1 * 1024 * 1024 * 1024)
        self.assertEqual(dust_collector.parse_size('123'), 123)
        self.assertEqual(dust_collector.parse_size('0'), 0)
        self.assertEqual(dust_collector.parse_size(''), 0)

    def test_parse_duration(self):
        self.assertEqual(dust_collector.parse_duration('7d'), timedelta(days=7))
        self.assertEqual(dust_collector.parse_duration('2w'), timedelta(weeks=2))
        self.assertEqual(dust_collector.parse_duration('1y'), timedelta(days=365))
        self.assertEqual(dust_collector.parse_duration('0d'), timedelta(seconds=0))
        self.assertEqual(dust_collector.parse_duration(''), timedelta(seconds=0))
        self.assertEqual(dust_collector.parse_duration('invalid'), timedelta(seconds=0))

if __name__ == '__main__':
    unittest.main()
