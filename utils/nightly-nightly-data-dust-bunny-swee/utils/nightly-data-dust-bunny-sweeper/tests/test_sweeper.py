import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
from datetime import datetime, timedelta
import time
import hashlib

# Add the src directory to the path to allow importing sweeper.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sweeper

class TestSweeper(unittest.TestCase):

    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash(self, mock_file_open, mock_isfile):
        # Mock rationale: We need to control the file content to ensure hash calculation is deterministic.
        # `mock_open` allows us to simulate reading from a file, and `os.path.isfile` ensures the function proceeds.
        mock_file_open.return_value.read.side_effect = [b'content1', b'']
        self.assertEqual(sweeper.calculate_file_hash('/path/to/file1.txt'), hashlib.md5(b'content1').hexdigest())

        mock_file_open.return_value.read.side_effect = [b'content2', b'']
        self.assertEqual(sweeper.calculate_file_hash('/path/to/file2.txt'), hashlib.md5(b'content2').hexdigest())

        # Test IOError handling
        mock_file_open.side_effect = IOError('Permission denied')
        self.assertIsNone(sweeper.calculate_file_hash('/path/to/unreadable.txt'))

    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('sweeper.calculate_file_hash')
    def test_find_duplicates(self, mock_calculate_hash, mock_isfile, mock_os_walk):
        # Mock rationale: `os.walk` is mocked to simulate a directory structure.
        # `os.path.isfile` is mocked to ensure all paths are treated as files.
        # `sweeper.calculate_file_hash` is mocked to provide deterministic hashes without actual file I/O.
        mock_os_walk.return_value = [
            ('/root', [], ['fileA.txt', 'fileB.txt', 'fileC.txt'])
        ]
        mock_calculate_hash.side_effect = [
            'hash1', # fileA.txt
            'hash2', # fileB.txt
            'hash1'  # fileC.txt (duplicate of fileA.txt)
        ]

        duplicates = sweeper.find_duplicates('/root')
        self.assertEqual(len(duplicates), 1)
        self.assertIn(('/root/fileC.txt', '/root/fileA.txt'), duplicates)

        # Test no duplicates
        mock_calculate_hash.side_effect = ['hash1', 'hash2', 'hash3']
        duplicates = sweeper.find_duplicates('/root')
        self.assertEqual(len(duplicates), 0)

    @patch('os.walk')
    def test_find_empty_dirs(self, mock_os_walk):
        # Mock rationale: `os.walk` is mocked to simulate a directory structure with empty and non-empty directories.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file.txt']), # /root is not empty
            ('/root/dir1', ['subdir'], []), # /root/dir1 is not empty (has subdir)
            ('/root/dir1/subdir', [], []), # /root/dir1/subdir is empty
            ('/root/dir2', [], []) # /root/dir2 is empty
        ]

        empty_dirs = sweeper.find_empty_dirs('/root')
        self.assertEqual(len(empty_dirs), 2)
        self.assertIn('/root/dir1/subdir', empty_dirs)
        self.assertIn('/root/dir2', empty_dirs)

        # Test no empty dirs
        mock_os_walk.return_value = [
            ('/root', ['dir1'], ['file.txt']),
            ('/root/dir1', [], ['another_file.txt'])
        ]
        empty_dirs = sweeper.find_empty_dirs('/root')
        self.assertEqual(len(empty_dirs), 0)

    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getmtime')
    def test_find_old_files(self, mock_getmtime, mock_isfile, mock_os_walk):
        # Mock rationale: `os.walk` simulates directory structure. `os.path.isfile` ensures paths are files.
        # `os.path.getmtime` is crucial to control the modification time of files deterministically.
        # We use `time.time()` and `timedelta` to create predictable timestamps for 'old' and 'new' files.
        now = datetime.now()
        old_timestamp = (now - timedelta(days=366)).timestamp()
        new_timestamp = (now - timedelta(days=10)).timestamp()

        mock_os_walk.return_value = [
            ('/root', [], ['old_file.txt', 'new_file.txt', 'unreadable_mtime.txt'])
        ]
        mock_getmtime.side_effect = [
            old_timestamp, # old_file.txt
            new_timestamp, # new_file.txt
            OSError # unreadable_mtime.txt
        ]

        old_files = sweeper.find_old_files('/root', 365)
        self.assertEqual(len(old_files), 1)
        self.assertIn('/root/old_file.txt', old_files)

        # Test no old files
        mock_getmtime.side_effect = [new_timestamp, new_timestamp]
        old_files = sweeper.find_old_files('/root', 365)
        self.assertEqual(len(old_files), 0)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=True)
    @patch('sweeper.find_duplicates', return_value=[('/path/to/file_b.txt', '/path/to/file_a.txt')])
    @patch('sweeper.find_empty_dirs', return_value=['/path/to/empty_dir'])
    @patch('sweeper.find_old_files', return_value=['/path/to/old_file.txt'])
    @patch('os.remove')
    @patch('os.rmdir')
    def test_main_list_only(self, mock_rmdir, mock_remove, mock_find_old_files, mock_find_empty_dirs, mock_find_duplicates, mock_isdir, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: `argparse.ArgumentParser.parse_args` is mocked to control command-line arguments.
        # `os.path.isdir` is mocked to validate the path without actual filesystem checks.
        # `find_duplicates`, `find_empty_dirs`, `find_old_files` are mocked to provide deterministic results for testing output.
        # `os.remove` and `os.rmdir` are mocked to ensure no actual deletions occur in 'list-only' mode.
        # `sys.stdout` and `sys.stderr` are mocked to capture printed output for assertion.
        mock_parse_args.return_value = MagicMock(
            path='/path/to/scan',
            duplicates=True,
            empty_dirs=True,
            old_files=100,
            delete=False # List only mode
        )

        sweeper.main()

        mock_find_duplicates.assert_called_once_with('/path/to/scan')
        mock_find_empty_dirs.assert_called_once_with('/path/to/scan')
        mock_find_old_files.assert_called_once_with('/path/to/scan', 100)
        mock_remove.assert_not_called()
        mock_rmdir.assert_not_called()

        output = mock_stdout.getvalue()
        self.assertIn("Duplicate pair: '/path/to/file_b.txt' and '/path/to/file_a.txt'", output)
        self.assertIn("Empty directory: '/path/to/empty_dir'", output)
        self.assertIn("Old file: '/path/to/old_file.txt'", output)
        self.assertNotIn("Deleted", output)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=True)
    @patch('sweeper.find_duplicates', return_value=[('/path/to/file_b.txt', '/path/to/file_a.txt')])
    @patch('sweeper.find_empty_dirs', return_value=['/path/to/empty_dir'])
    @patch('sweeper.find_old_files', return_value=['/path/to/old_file.txt'])
    @patch('os.remove')
    @patch('os.rmdir')
    def test_main_delete_mode(self, mock_rmdir, mock_remove, mock_find_old_files, mock_find_empty_dirs, mock_find_duplicates, mock_isdir, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Similar to `test_main_list_only`, but `delete=True` is set to test deletion calls.
        # `os.remove` and `os.rmdir` are mocked to verify they are called with the correct arguments.
        mock_parse_args.return_value = MagicMock(
            path='/path/to/scan',
            duplicates=True,
            empty_dirs=True,
            old_files=100,
            delete=True # Delete mode
        )

        sweeper.main()

        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('/path/to/file_b.txt') # One of the duplicates is removed
        mock_remove.assert_any_call('/path/to/old_file.txt')
        mock_rmdir.assert_called_once_with('/path/to/empty_dir')

        output = mock_stdout.getvalue()
        self.assertIn("Deleted '/path/to/file_b.txt'", output)
        self.assertIn("Deleted '/path/to/empty_dir'", output)
        self.assertIn("Deleted '/path/to/old_file.txt'", output)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_no_operation_specified(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: `argparse.ArgumentParser.parse_args` is mocked to simulate no operation arguments.
        # `sys.exit` is mocked to prevent the test from terminating the runner.
        # `sys.stderr` is mocked to capture error messages.
        mock_parse_args.return_value = MagicMock(
            path='/path/to/scan',
            duplicates=False,
            empty_dirs=False,
            old_files=None,
            delete=False
        )

        sweeper.main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Please specify at least one operation", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=False)
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_isdir, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: `os.path.isdir` is mocked to simulate an invalid path.
        # `sys.exit` is mocked to prevent test termination.
        # `sys.stderr` is mocked to capture error messages.
        mock_parse_args.return_value = MagicMock(
            path='/invalid/path',
            duplicates=True,
            empty_dirs=False,
            old_files=None,
            delete=False
        )

        sweeper.main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Path '/invalid/path' is not a valid directory.", mock_stderr.getvalue())
