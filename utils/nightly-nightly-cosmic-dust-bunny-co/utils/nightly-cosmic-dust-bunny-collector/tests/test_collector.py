import unittest
from unittest.mock import patch, MagicMock
import os
import datetime
from pathlib import Path

# Import the class to be tested
from src.collector import CosmicDustBunnyCollector

class TestCosmicDustBunnyCollector(unittest.TestCase):

    def setUp(self):
        # Define a consistent 'now' for testing age-based cleanup
        self.mock_now = datetime.datetime(2023, 10, 26, 10, 0, 0)

    @patch('os.walk')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.iterdir')
    @patch('pathlib.Path.stat')
    @patch('datetime.datetime')
    def test_find_dust_bunnies_dry_run(self, mock_datetime, mock_stat, mock_iterdir, mock_is_dir, mock_is_file, mock_exists, mock_os_walk):
        # Mock rationale: datetime.datetime.now is mocked to ensure deterministic age calculations.
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp

        # Mock rationale: pathlib.Path.exists is mocked to simulate the existence of the root path.
        mock_exists.return_value = True

        # Mock rationale: os.walk is mocked to simulate a file system structure without creating actual files.
        # This ensures tests are fast, isolated, and don't leave artifacts.
        mock_os_walk.return_value = [
            ('/root', ['subdir1', '__pycache__', 'empty_dir'], ['file.txt', '.DS_Store', 'old.log', 'new.log', 'temp.tmp']),
            ('/root/subdir1', [], ['another.txt']),
            ('/root/__pycache__', [], ['cache_file.pyc']),
            ('/root/empty_dir', [], []),
        ]

        # Mock rationale: pathlib.Path.is_file and .is_dir are mocked to control file/directory types.
        # This allows testing specific file/directory behaviors without actual file system interaction.
        def mock_path_is_type(path_obj):
            path_str = str(path_obj)
            if path_str.endswith('.txt') or path_str.endswith('.log') or path_str.endswith('.tmp') or path_str.endswith('.DS_Store') or path_str.endswith('.pyc'):
                return True
            return False
        mock_is_file.side_effect = mock_path_is_type
        mock_is_dir.side_effect = lambda p: not mock_path_is_type(p)

        # Mock rationale: pathlib.Path.iterdir is mocked to simulate directory contents for empty dir check.
        mock_iterdir.side_effect = lambda: [] # Default to empty for empty_dir

        # Mock rationale: pathlib.Path.stat is mocked to control file modification times for log age checks.
        # This ensures that 'old.log' is identified as old and 'new.log' is not.
        mock_stat_obj_old = MagicMock()
        mock_stat_obj_old.st_mtime = (self.mock_now - datetime.timedelta(days=10)).timestamp()
        mock_stat_obj_new = MagicMock()
        mock_stat_obj_new.st_mtime = (self.mock_now - datetime.timedelta(days=1)).timestamp()

        def mock_stat_side_effect(path_obj):
            if 'old.log' in str(path_obj):
                return mock_stat_obj_old
            elif 'new.log' in str(path_obj):
                return mock_stat_obj_new
            return MagicMock(st_mtime=self.mock_now.timestamp()) # Default for others
        mock_stat.side_effect = mock_stat_side_effect

        collector = CosmicDustBunnyCollector(['/root'], log_age_days=7, dry_run=True)
        bunnies = collector.find_dust_bunnies()

        expected_bunnies = sorted([
            Path('/root/.DS_Store'),
            Path('/root/old.log'),
            Path('/root/temp.tmp'),
            Path('/root/__pycache__/cache_file.pyc'),
            Path('/root/empty_dir') # Should be identified as empty
        ])
        actual_bunnies = sorted(bunnies)

        self.assertEqual(len(actual_bunnies), len(expected_bunnies))
        for i in range(len(actual_bunnies)):
            self.assertEqual(actual_bunnies[i], expected_bunnies[i])

    @patch('os.walk')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.iterdir')
    @patch('pathlib.Path.stat')
    @patch('datetime.datetime')
    @patch('os.remove')
    @patch('os.rmdir')
    def test_clean_dust_bunnies_actual_run(self, mock_os_rmdir, mock_os_remove, mock_datetime, mock_stat, mock_iterdir, mock_is_dir, mock_is_file, mock_exists, mock_os_walk):
        # Mock rationale: datetime.datetime.now is mocked to ensure deterministic age calculations.
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp

        # Mock rationale: pathlib.Path.exists is mocked to simulate the existence of the root path.
        mock_exists.return_value = True

        # Mock rationale: os.walk is mocked to simulate a file system structure.
        mock_os_walk.return_value = [
            ('/root', ['empty_dir'], ['.DS_Store', 'old.log']),
            ('/root/empty_dir', [], []),
        ]

        # Mock rationale: pathlib.Path.is_file and .is_dir are mocked to control file/directory types.
        def mock_path_is_type(path_obj):
            path_str = str(path_obj)
            if path_str.endswith('.DS_Store') or path_str.endswith('.log'):
                return True
            return False
        mock_is_file.side_effect = mock_path_is_type
        mock_is_dir.side_effect = lambda p: not mock_path_is_type(p)

        # Mock rationale: pathlib.Path.iterdir is mocked to simulate directory contents for empty dir check.
        mock_iterdir.side_effect = lambda: [] # Default to empty for empty_dir

        # Mock rationale: pathlib.Path.stat is mocked to control file modification times.
        mock_stat_obj_old = MagicMock()
        mock_stat_obj_old.st_mtime = (self.mock_now - datetime.timedelta(days=10)).timestamp()
        mock_stat.return_value = mock_stat_obj_old

        collector = CosmicDustBunnyCollector(['/root'], log_age_days=7, dry_run=False)
        collector.find_dust_bunnies()
        collector.clean_dust_bunnies()

        # Mock rationale: os.remove and os.rmdir are mocked to prevent actual file system changes.
        # We assert that these mocks were called with the expected paths.
        mock_os_remove.assert_any_call(Path('/root/.DS_Store'))
        mock_os_remove.assert_any_call(Path('/root/old.log'))
        mock_os_rmdir.assert_any_call(Path('/root/empty_dir'))

        self.assertEqual(mock_os_remove.call_count, 2)
        self.assertEqual(mock_os_rmdir.call_count, 1)

    @patch('os.walk')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.iterdir')
    @patch('pathlib.Path.stat')
    @patch('datetime.datetime')
    @patch('os.remove')
    @patch('os.rmdir')
    def test_clean_dust_bunnies_dry_run_no_deletion(self, mock_os_rmdir, mock_os_remove, mock_datetime, mock_stat, mock_iterdir, mock_is_dir, mock_is_file, mock_exists, mock_os_walk):
        # Mock rationale: datetime.datetime.now is mocked to ensure deterministic age calculations.
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp

        # Mock rationale: pathlib.Path.exists is mocked to simulate the existence of the root path.
        mock_exists.return_value = True

        # Mock rationale: os.walk is mocked to simulate a file system structure.
        mock_os_walk.return_value = [
            ('/root', [], ['.DS_Store']),
        ]

        # Mock rationale: pathlib.Path.is_file and .is_dir are mocked to control file/directory types.
        mock_is_file.return_value = True
        mock_is_dir.return_value = False

        # Mock rationale: pathlib.Path.iterdir is mocked to simulate directory contents.
        mock_iterdir.return_value = []

        # Mock rationale: pathlib.Path.stat is mocked to control file modification times.
        mock_stat_obj_old = MagicMock()
        mock_stat_obj_old.st_mtime = (self.mock_now - datetime.timedelta(days=10)).timestamp()
        mock_stat.return_value = mock_stat_obj_old

        collector = CosmicDustBunnyCollector(['/root'], log_age_days=7, dry_run=True)
        collector.find_dust_bunnies()
        collector.clean_dust_bunnies()

        # Mock rationale: os.remove and os.rmdir are mocked to prevent actual file system changes.
        # In a dry run, these should *not* be called.
        mock_os_remove.assert_not_called()
        mock_os_rmdir.assert_not_called()

    @patch('os.walk')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.iterdir')
    @patch('pathlib.Path.stat')
    @patch('datetime.datetime')
    @patch('os.remove')
    @patch('os.rmdir')
    def test_empty_dir_not_deleted_if_not_empty(self, mock_os_rmdir, mock_os_remove, mock_datetime, mock_stat, mock_iterdir, mock_is_dir, mock_is_file, mock_exists, mock_os_walk):
        # Mock rationale: datetime.datetime.now is mocked to ensure deterministic age calculations.
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp

        # Mock rationale: pathlib.Path.exists is mocked to simulate the existence of the root path.
        mock_exists.return_value = True

        # Mock rationale: os.walk is mocked to simulate a file system structure.
        mock_os_walk.return_value = [
            ('/root', ['non_empty_dir'], []),
            ('/root/non_empty_dir', [], ['important_file.txt']),
        ]

        # Mock rationale: pathlib.Path.is_file and .is_dir are mocked to control file/directory types.
        def mock_path_is_type(path_obj):
            path_str = str(path_obj)
            if path_str.endswith('.txt'):
                return True
            return False
        mock_is_file.side_effect = mock_path_is_type
        mock_is_dir.side_effect = lambda p: not mock_path_is_type(p)

        # Mock rationale: pathlib.Path.iterdir is mocked to simulate directory contents.
        # For 'non_empty_dir', it should return a non-empty list.
        def iterdir_side_effect():
            if str(mock_iterdir.mock_current_path) == '/root/non_empty_dir':
                yield Path('/root/non_empty_dir/important_file.txt')
            else:
                yield from []
        mock_iterdir.side_effect = iterdir_side_effect
        # Store the path being iterated for iterdir_side_effect
        mock_iterdir.mock_current_path = None
        original_iterdir = Path.iterdir
        def patched_iterdir(self):
            mock_iterdir.mock_current_path = self
            return original_iterdir(self)
        Path.iterdir = patched_iterdir

        # Mock rationale: pathlib.Path.stat is mocked to control file modification times.
        mock_stat.return_value = MagicMock(st_mtime=self.mock_now.timestamp())

        collector = CosmicDustBunnyCollector(['/root'], log_age_days=7, dry_run=False)
        collector.find_dust_bunnies()
        collector.clean_dust_bunnies()

        # The 'non_empty_dir' should not be deleted because it contains 'important_file.txt'
        mock_os_rmdir.assert_not_called()
        mock_os_remove.assert_not_called()

if __name__ == '__main__':
    unittest.main()
