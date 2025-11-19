import unittest
from unittest.mock import patch, MagicMock, call
import os
import shutil
from datetime import datetime, timedelta
import sys

# Import the functions to be tested
# Assuming dust_collector.py is in src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dust_collector import get_file_age_days, is_dust, collect_dust

class TestDustCollector(unittest.TestCase):

    @patch('dust_collector.datetime')
    def test_get_file_age_days(self, mock_datetime):
        # Mock rationale: `datetime.now()` and `os.path.getmtime` are non-deterministic
        # and depend on the current time and file system state.
        # We mock them to control the time for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2023, 1, 31)
        mock_datetime.fromtimestamp.return_value = datetime(2023, 1, 1)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow actual datetime object creation

        with patch('os.path.getmtime', return_value=datetime(2023, 1, 1).timestamp()):
            self.assertEqual(get_file_age_days("dummy_file.txt"), 30)

        # Test error case
        with patch('os.path.getmtime', side_effect=OSError):
            self.assertEqual(get_file_age_days("non_existent_file.txt"), -1)

    @patch('dust_collector.os.path.isfile', return_value=True)
    @patch('dust_collector.os.path.getsize')
    @patch('dust_collector.get_file_age_days')
    def test_is_dust(self, mock_get_file_age_days, mock_get_size, mock_isfile):
        # Mock rationale: `os.path.isfile`, `os.path.getsize`, and `get_file_age_days`
        # are file system operations and internal function calls.
        # We mock them to control file properties (existence, size, age) for deterministic testing.

        # Test empty file
        mock_get_size.return_value = 0
        mock_get_file_age_days.return_value = 10 # Not old enough
        self.assertTrue(is_dust("empty.txt", max_size_bytes=100, min_age_days=30))

        # Test small file
        mock_get_size.return_value = 50
        mock_get_file_age_days.return_value = 10 # Not old enough
        self.assertTrue(is_dust("small.txt", max_size_bytes=100, min_age_days=30))

        # Test old file
        mock_get_size.return_value = 200 # Not small
        mock_get_file_age_days.return_value = 40
        self.assertTrue(is_dust("old.txt", max_size_bytes=100, min_age_days=30))

        # Test not dust (large, new)
        mock_get_size.return_value = 200
        mock_get_file_age_days.return_value = 10
        self.assertFalse(is_dust("not_dust.txt", max_size_bytes=100, min_age_days=30))

        # Test file not existing
        mock_isfile.return_value = False
        self.assertFalse(is_dust("non_existent.txt", max_size_bytes=100, min_age_days=30))
        mock_isfile.return_value = True # Reset for other tests

        # Test OSError during file access
        mock_get_size.side_effect = OSError("Permission denied")
        self.assertFalse(is_dust("unreadable.txt", max_size_bytes=100, min_age_days=30))
        mock_get_size.side_effect = None # Reset

        # Test min_age_days = 0 (ignore age)
        mock_get_size.return_value = 50
        mock_get_file_age_days.return_value = 100 # Very old
        self.assertTrue(is_dust("small_ignore_age.txt", max_size_bytes=100, min_age_days=0))
        mock_get_size.return_value = 200 # Not small
        self.assertFalse(is_dust("large_ignore_age.txt", max_size_bytes=100, min_age_days=0))


    @patch('dust_collector.os.path.isdir', return_value=True)
    @patch('dust_collector.os.walk')
    @patch('dust_collector.is_dust')
    @patch('dust_collector.os.makedirs')
    @patch('dust_collector.shutil.move')
    @patch('dust_collector.os.path.exists', return_value=False) # For shutil.move collision check
    @patch('dust_collector.os.path.getsize', return_value=10) # For verbose output
    @patch('dust_collector.get_file_age_days', return_value=40) # For verbose output
    @patch('builtins.print') # Mock print to capture output
    def test_collect_dust_list_action(self, mock_print, mock_get_file_age_days, mock_get_size, mock_exists, mock_move, mock_makedirs, mock_is_dust, mock_os_walk, mock_isdir):
        # Mock rationale: `os.path.isdir`, `os.walk`, `is_dust`, `os.makedirs`, `shutil.move`,
        # `os.path.exists`, `os.path.getsize`, `get_file_age_days`, and `print` are
        # file system operations, internal logic, and output functions.
        # We mock them to simulate file system structure, control dust detection,
        # prevent actual file modifications, and capture output for verification.

        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file1.txt', 'file2.log']),
            ('/root/dir1', [], ['file3.tmp'])
        ]
        # Simulate file1.txt and file3.tmp as dust
        mock_is_dust.side_effect = lambda f, *args: f in ['/root/file1.txt', '/root/dir1/file3.tmp']

        collect_dust(
            paths=['/root'],
            action='list',
            quarantine_path='./dust_quarantine',
            max_size_bytes=1024,
            min_age_days=30,
            exclude_dirs=[],
            verbose=False
        )

        mock_os_walk.assert_called_once_with('/root')
        self.assertEqual(mock_is_dust.call_count, 3) # file1, file2, file3
        mock_makedirs.assert_not_called()
        mock_move.assert_not_called()

        # Check if the dust files were printed
        mock_print.assert_any_call('\n--- Cosmic Dust Report (2 files found) ---')
        mock_print.assert_any_call('- /root/file1.txt')
        mock_print.assert_any_call('- /root/dir1/file3.tmp')
        mock_print.assert_any_call('\n--- Action: List only. No files were moved. ---')

    @patch('dust_collector.os.path.isdir', return_value=True)
    @patch('dust_collector.os.walk')
    @patch('dust_collector.is_dust')
    @patch('dust_collector.os.makedirs')
    @patch('dust_collector.shutil.move')
    @patch('dust_collector.os.path.exists', return_value=False) # For shutil.move collision check
    @patch('dust_collector.os.path.getsize', return_value=10) # For verbose output
    @patch('dust_collector.get_file_age_days', return_value=40) # For verbose output
    @patch('builtins.print')
    @patch('dust_collector.datetime') # For timestamp in case of collision
    def test_collect_dust_quarantine_action(self, mock_datetime, mock_print, mock_get_file_age_days, mock_get_size, mock_exists, mock_move, mock_makedirs, mock_is_dust, mock_os_walk, mock_isdir):
        # Mock rationale: Same as above, plus `datetime` for collision timestamp.
        mock_datetime.now.return_value = datetime(2023, 1, 31, 10, 0, 0)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow actual datetime object creation

        mock_os_walk.return_value = [
            ('/root', ['dir1'], ['file1.txt']),
            ('/root/dir1', [], ['file2.tmp'])
        ]
        mock_is_dust.side_effect = lambda f, *args: f in ['/root/file1.txt', '/root/dir1/file2.tmp']

        quarantine_path = '/tmp/quarantine_dust'
        collect_dust(
            paths=['/root'],
            action='quarantine',
            quarantine_path=quarantine_path,
            max_size_bytes=1024,
            min_age_days=30,
            exclude_dirs=[],
            verbose=False
        )

        mock_makedirs.assert_called_once_with(quarantine_path, exist_ok=True)
        mock_move.assert_has_calls([
            call('/root/file1.txt', os.path.join(quarantine_path, 'file1.txt')),
            call('/root/dir1/file2.tmp', os.path.join(quarantine_path, 'file2.tmp'))
        ], any_order=True)
        mock_print.assert_any_call(f'\n--- Moving dust to quarantine: {quarantine_path} ---')
        mock_print.assert_any_call(f'Moved: /root/file1.txt -> {os.path.join(quarantine_path, "file1.txt")}')

    @patch('dust_collector.os.path.isdir', return_value=True)
    @patch('dust_collector.os.walk')
    @patch('dust_collector.is_dust', return_value=False) # No dust found
    @patch('builtins.print')
    def test_collect_dust_no_dust_found(self, mock_print, mock_is_dust, mock_os_walk, mock_isdir):
        # Mock rationale: Simulating a scenario where no dust is found to test the corresponding output.
        mock_os_walk.return_value = [
            ('/root', [], ['file1.txt'])
        ]

        collect_dust(
            paths=['/root'],
            action='list',
            quarantine_path='./dust_quarantine',
            max_size_bytes=1024,
            min_age_days=30,
            exclude_dirs=[],
            verbose=False
        )
        mock_print.assert_called_once_with("No cosmic dust found. Your digital space is sparkling clean!")

    @patch('dust_collector.os.path.isdir')
    @patch('dust_collector.os.walk')
    @patch('dust_collector.is_dust')
    @patch('builtins.print')
    def test_collect_dust_exclude_dirs(self, mock_print, mock_is_dust, mock_os_walk, mock_isdir):
        # Mock rationale: Testing the directory exclusion logic within `os.walk`.
        mock_isdir.return_value = True
        # Simulate os.walk behavior where 'dirs' list is modified in-place
        def mock_walk_side_effect(path):
            if path == '/root':
                yield '/root', ['node_modules', 'src', 'venv'], ['file.txt']
            elif path == '/root/src':
                yield '/root/src', [], ['code.py']
        mock_os_walk.side_effect = mock_walk_side_effect

        collect_dust(
            paths=['/root'],
            action='list',
            quarantine_path='./dust_quarantine',
            max_size_bytes=1024,
            min_age_days=30,
            exclude_dirs=['node_modules', 'venv'],
            verbose=False
        )

        # Ensure os.walk was called for /root
        mock_os_walk.assert_any_call('/root')
        # Ensure that 'src' was traversed, but 'node_modules' and 'venv' were not
        mock_os_walk.assert_any_call('/root/src')
        # is_dust should be called for file.txt and code.py, but not for files in excluded dirs
        self.assertEqual(mock_is_dust.call_count, 2)
        mock_is_dust.assert_any_call('/root/file.txt', 1024, 30)
        mock_is_dust.assert_any_call('/root/src/code.py', 1024, 30)

    @patch('dust_collector.os.path.isdir')
    @patch('builtins.print')
    def test_collect_dust_invalid_path(self, mock_print, mock_isdir):
        # Mock rationale: Testing error handling for invalid input paths.
        mock_isdir.return_value = False # Simulate an invalid path

        collect_dust(
            paths=['/non/existent/path'],
            action='list',
            quarantine_path='./dust_quarantine',
            max_size_bytes=1024,
            min_age_days=30,
            exclude_dirs=[],
            verbose=False
        )
        mock_print.assert_any_call("Error: Path '/non/existent/path' is not a valid directory. Skipping.", file=sys.stderr)
        mock_print.assert_any_call("No cosmic dust found. Your digital space is sparkling clean!") # Because no valid paths were processed

    @patch('dust_collector.os.path.isdir', return_value=True)
    @patch('dust_collector.os.walk')
    @patch('dust_collector.is_dust')
    @patch('dust_collector.os.makedirs')
    @patch('dust_collector.shutil.move', side_effect=Exception("Move error"))
    @patch('dust_collector.os.path.exists', return_value=False)
    @patch('builtins.print')
    def test_collect_dust_quarantine_move_error(self, mock_print, mock_exists, mock_move, mock_makedirs, mock_is_dust, mock_os_walk, mock_isdir):
        # Mock rationale: Testing error handling during the file moving process.
        mock_os_walk.return_value = [
            ('/root', [], ['file1.txt'])
        ]
        mock_is_dust.return_value = True

        quarantine_path = '/tmp/quarantine_dust'
        collect_dust(
            paths=['/root'],
            action='quarantine',
            quarantine_path=quarantine_path,
            max_size_bytes=1024,
            min_age_days=30,
            exclude_dirs=[],
            verbose=False
        )

        mock_makedirs.assert_called_once_with(quarantine_path, exist_ok=True)
        mock_move.assert_called_once_with('/root/file1.txt', os.path.join(quarantine_path, 'file1.txt'))
        mock_print.assert_any_call(f"Error moving /root/file1.txt: Move error", file=sys.stderr)

    @patch('dust_collector.os.path.isdir', return_value=True)
    @patch('dust_collector.os.walk')
    @patch('dust_collector.is_dust')
    @patch('dust_collector.os.makedirs')
    @patch('dust_collector.shutil.move')
    @patch('dust_collector.os.path.exists') # This needs to return True for collision
    @patch('dust_collector.datetime') # For timestamp in case of collision
    @patch('builtins.print')
    def test_collect_dust_quarantine_collision(self, mock_print, mock_datetime, mock_exists, mock_move, mock_makedirs, mock_is_dust, mock_os_walk, mock_isdir):
        # Mock rationale: Testing the collision resolution logic when moving files to quarantine.
        mock_datetime.now.return_value = datetime(2023, 1, 31, 10, 0, 0)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow actual datetime object creation

        mock_os_walk.return_value = [
            ('/root', [], ['file1.txt'])
        ]
        mock_is_dust.return_value = True
        mock_exists.side_effect = [True, False] # First check for original name returns True, second for timestamped name returns False

        quarantine_path = '/tmp/quarantine_dust'
        collect_dust(
            paths=['/root'],
            action='quarantine',
            quarantine_path=quarantine_path,
            max_size_bytes=1024,
            min_age_days=30,
            exclude_dirs=[],
            verbose=False
        )

        expected_dest_path = os.path.join(quarantine_path, 'file1_20230131100000000000.txt')
        mock_move.assert_called_once_with('/root/file1.txt', expected_dest_path)
        mock_print.assert_any_call(f'Moved: /root/file1.txt -> {expected_dest_path}')


if __name__ == '__main__':
    unittest.main()
