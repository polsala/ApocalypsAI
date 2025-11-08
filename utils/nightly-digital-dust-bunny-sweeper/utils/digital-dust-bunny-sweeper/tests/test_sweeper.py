import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Mock rationale: We need to simulate a filesystem without actually creating files
# or directories on the disk. This allows for deterministic, fast, and isolated tests.
# We mock `Path.rglob`, `Path.is_file`, `Path.is_dir`, `Path.stat`, and `Path.iterdir`
# to control the filesystem state and file metadata (like modification times).

# Adjust sys.path to allow importing the sweeper module from src/
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
import sweeper
sys.path.pop(0)

class MockStat:
    """A mock object for os.stat_result."""
    def __init__(self, st_mtime):
        self.st_mtime = st_mtime

class MockPath(Path):
    """A mock Path object that can simulate file/directory properties."""
    _mock_current_time = datetime.now() # Will be set by setUp

    def __new__(cls, path_str, is_file=False, is_dir=False, mtime_days_ago=0, children=None):
        # Path.__new__ expects a string, so we pass it through
        obj = super().__new__(cls, path_str)
        obj._is_file = is_file
        obj._is_dir = is_dir
        obj._mtime_days_ago = mtime_days_ago
        obj._children = children if children is not None else []
        return obj

    def is_file(self):
        return self._is_file

    def is_dir(self):
        return self._is_dir

    def stat(self):
        mock_timestamp = (self._mock_current_time - timedelta(days=self._mtime_days_ago)).timestamp()
        return MockStat(mock_timestamp)

    def iterdir(self):
        # Simulate an empty directory if _children is empty
        return iter(self._children)


class TestSweeper(unittest.TestCase):

    @patch('sweeper.datetime')
    def setUp(self, mock_datetime):
        # Set a fixed 'current time' for deterministic age calculations
        self.fixed_now = datetime(2023, 1, 15, 12, 0, 0)
        mock_datetime.now.return_value = self.fixed_now
        mock_datetime.fromtimestamp = datetime.fromtimestamp # Use real fromtimestamp
        mock_datetime.timedelta = timedelta # Use real timedelta

        MockPath._mock_current_time = self.fixed_now # Ensure MockPath uses fixed time

    @patch('pathlib.Path.rglob') # Patch the rglob method that sweeper.py calls
    def test_scan_directory_finds_old_file(self, mock_rglob):
        root = MockPath('/test_root', is_dir=True) # This root is just for the argument, its rglob is patched
        old_file = MockPath('/test_root/old_file.txt', is_file=True, mtime_days_ago=400)
        new_file = MockPath('/test_root/new_file.txt', is_file=True, mtime_days_ago=10)

        # Mock rglob to yield our simulated files
        mock_rglob.return_value = [old_file, new_file]

        dust_bunnies = sweeper.scan_directory(root, 365, [], [])

        self.assertEqual(len(dust_bunnies), 1)
        self.assertEqual(dust_bunnies[0][0], old_file)
        self.assertIn("File, 400 days old", dust_bunnies[0][1])

    @patch('pathlib.Path.rglob')
    def test_scan_directory_finds_empty_directory(self, mock_rglob):
        root = MockPath('/test_root', is_dir=True)
        # A directory with no children in its iterdir() is considered empty
        empty_dir = MockPath('/test_root/empty_dir', is_dir=True, children=[])
        non_empty_dir = MockPath('/test_root/non_empty_dir', is_dir=True, children=[MockPath('child.txt')])

        mock_rglob.return_value = [empty_dir, non_empty_dir]

        dust_bunnies = sweeper.scan_directory(root, 365, [], [])

        self.assertEqual(len(dust_bunnies), 1)
        self.assertEqual(dust_bunnies[0][0], empty_dir)
        self.assertEqual(dust_bunnies[0][1], "Empty Directory")

    @patch('pathlib.Path.rglob')
    def test_scan_directory_with_include_patterns(self, mock_rglob):
        root = MockPath('/test_root', is_dir=True)
        old_log = MockPath('/test_root/old.log', is_file=True, mtime_days_ago=400)
        old_txt = MockPath('/test_root/old.txt', is_file=True, mtime_days_ago=400)
        new_log = MockPath('/test_root/new.log', is_file=True, mtime_days_ago=10)

        mock_rglob.return_value = [old_log, old_txt, new_log]

        dust_bunnies = sweeper.scan_directory(root, 365, ['*.log'], [])

        self.assertEqual(len(dust_bunnies), 1)
        self.assertEqual(dust_bunnies[0][0], old_log)

    @patch('pathlib.Path.rglob')
    def test_scan_directory_with_exclude_patterns(self, mock_rglob):
        root = MockPath('/test_root', is_dir=True)
        old_log = MockPath('/test_root/old.log', is_file=True, mtime_days_ago=400)
        old_bak = MockPath('/test_root/old.bak', is_file=True, mtime_days_ago=400)

        mock_rglob.return_value = [old_log, old_bak]

        dust_bunnies = sweeper.scan_directory(root, 365, [], ['*.bak'])

        self.assertEqual(len(dust_bunnies), 1)
        self.assertEqual(dust_bunnies[0][0], old_log)

    @patch('pathlib.Path.rglob')
    def test_scan_directory_no_dust_bunnies(self, mock_rglob):
        root = MockPath('/test_root', is_dir=True)
        new_file = MockPath('/test_root/new_file.txt', is_file=True, mtime_days_ago=10)
        non_empty_dir = MockPath('/test_root/non_empty_dir', is_dir=True, children=[MockPath('child.txt')])

        mock_rglob.return_value = [new_file, non_empty_dir]

        dust_bunnies = sweeper.scan_directory(root, 365, [], [])

        self.assertEqual(len(dust_bunnies), 0)

    @patch('pathlib.Path.rglob')
    def test_scan_directory_permission_error_handling(self, mock_rglob):
        root = MockPath('/test_root', is_dir=True)
        # Create a mock path that raises PermissionError on stat()
        bad_path = MagicMock(spec=Path)
        bad_path.__str__.return_value = '/test_root/unreadable_file'
        bad_path.is_file.return_value = True
        bad_path.is_dir.return_value = False
        bad_path.stat.side_effect = PermissionError("Permission denied")
        bad_path.name = 'unreadable_file'

        old_file = MockPath('/test_root/old_file.txt', is_file=True, mtime_days_ago=400)

        mock_rglob.return_value = [bad_path, old_file]

        # Capture stderr output to check if the warning is printed
        with patch('sys.stderr', new_callable=MagicMock) as mock_stderr:
            dust_bunnies = sweeper.scan_directory(root, 365, [], [])
            mock_stderr.write.assert_called_with("Warning: Could not access /test_root/unreadable_file: Permission denied\n")

        self.assertEqual(len(dust_bunnies), 1)
        self.assertEqual(dust_bunnies[0][0], old_file)


if __name__ == '__main__':
    unittest.main()
