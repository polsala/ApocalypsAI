import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Suppress logging during tests for cleaner output unless explicitly needed
logging.disable(logging.CRITICAL)

# Import the function to be tested
from src.dust_collector import collect_dust

class TestDustCollector(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.mock_now = datetime(2023, 10, 26, 10, 0, 0) # Fixed current time for deterministic tests

    def tearDown(self):
        # Clean up the temporary directory after tests
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def _create_test_file(self, filename: str, mtime: datetime):
        """Helper to create a file in the temp directory and set its modification time."""
        file_path = self.temp_dir / filename
        file_path.touch()
        # Note: os.utime is used to set mtime, but for testing collect_dust, we will mock Path.stat().st_mtime
        return file_path

    @patch('datetime.datetime')
    @patch('pathlib.Path.unlink')
    @patch('pathlib.Path.stat')
    def test_no_files_deleted_if_all_new(self, mock_stat, mock_unlink, mock_dt):
        # Mock rationale: We need to control the current time to deterministically test file age.
        mock_dt.now.return_value = self.mock_now
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow other datetime calls

        # Create files that are newer than the threshold
        new_file1 = self._create_test_file("new_file1.log", self.mock_now - timedelta(days=1))
        new_file2 = self._create_test_file("new_file2.txt", self.mock_now - timedelta(days=2))

        # Mock rationale: We need to control file modification times to deterministically test file age.
        # Path.stat() will be called for each file, so we need to provide mock stat objects.
        mock_stat_results = {
            new_file1: MagicMock(st_mtime=(self.mock_now - timedelta(days=1)).timestamp()),
            new_file2: MagicMock(st_mtime=(self.mock_now - timedelta(days=2)).timestamp()),
        }
        mock_stat.side_effect = lambda: mock_stat_results[mock_stat.call_args.self]

        # Mock rationale: We need to control Path.iterdir() to simulate directory contents.
        with patch('pathlib.Path.iterdir', return_value=[new_file1, new_file2]):
            collect_dust(self.temp_dir, age_days=3)

        mock_unlink.assert_not_called()

    @patch('datetime.datetime')
    @patch('pathlib.Path.unlink')
    @patch('pathlib.Path.stat')
    def test_files_deleted_if_older_than_threshold(self, mock_stat, mock_unlink, mock_dt):
        # Mock rationale: We need to control the current time to deterministically test file age.
        mock_dt.now.return_value = self.mock_now
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Create files: one old, one new
        old_file = self._create_test_file("old_file.log", self.mock_now - timedelta(days=5))
        new_file = self._create_test_file("new_file.txt", self.mock_now - timedelta(days=1))

        # Mock rationale: We need to control file modification times to deterministically test file age.
        mock_stat_results = {
            old_file: MagicMock(st_mtime=(self.mock_now - timedelta(days=5)).timestamp()),
            new_file: MagicMock(st_mtime=(self.mock_now - timedelta(days=1)).timestamp()),
        }
        mock_stat.side_effect = lambda: mock_stat_results[mock_stat.call_args.self]

        # Mock rationale: We need to control Path.iterdir() to simulate directory contents.
        with patch('pathlib.Path.iterdir', return_value=[old_file, new_file]):
            collect_dust(self.temp_dir, age_days=3)

        mock_unlink.assert_called_once_with()
        self.assertEqual(mock_unlink.call_args.self, old_file)

    @patch('datetime.datetime')
    @patch('pathlib.Path.unlink')
    @patch('pathlib.Path.stat')
    def test_dry_run_mode_does_not_delete(self, mock_stat, mock_unlink, mock_dt):
        # Mock rationale: We need to control the current time to deterministically test file age.
        mock_dt.now.return_value = self.mock_now
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Create an old file
        old_file = self._create_test_file("old_file.log", self.mock_now - timedelta(days=5))

        # Mock rationale: We need to control file modification times to deterministically test file age.
        mock_stat_results = {
            old_file: MagicMock(st_mtime=(self.mock_now - timedelta(days=5)).timestamp()),
        }
        mock_stat.side_effect = lambda: mock_stat_results[mock_stat.call_args.self]

        # Mock rationale: We need to control Path.iterdir() to simulate directory contents.
        with patch('pathlib.Path.iterdir', return_value=[old_file]):
            collect_dust(self.temp_dir, age_days=3, dry_run=True)

        mock_unlink.assert_not_called()

    @patch('datetime.datetime')
    @patch('pathlib.Path.unlink')
    @patch('pathlib.Path.stat')
    def test_ignores_directories(self, mock_stat, mock_unlink, mock_dt):
        # Mock rationale: We need to control the current time to deterministically test file age.
        mock_dt.now.return_value = self.mock_now
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Create an old file and a directory
        old_file = self._create_test_file("old_file.log", self.mock_now - timedelta(days=5))
        sub_dir = self.temp_dir / "sub_directory"
        sub_dir.mkdir()

        # Mock rationale: We need to control file modification times to deterministically test file age.
        mock_stat_results = {
            old_file: MagicMock(st_mtime=(self.mock_now - timedelta(days=5)).timestamp()),
        }
        mock_stat.side_effect = lambda: mock_stat_results[mock_stat.call_args.self]

        # Mock rationale: We need to control Path.iterdir() to simulate directory contents.
        # Ensure sub_dir.is_file() returns False and old_file.is_file() returns True
        mock_old_file = MagicMock(spec=Path, name=str(old_file))
        mock_old_file.is_file.return_value = True
        mock_old_file.stat.return_value = mock_stat_results[old_file]
        mock_old_file.unlink.return_value = None

        mock_sub_dir = MagicMock(spec=Path, name=str(sub_dir))
        mock_sub_dir.is_file.return_value = False
        mock_sub_dir.is_dir.return_value = True

        with patch('pathlib.Path.iterdir', return_value=[mock_old_file, mock_sub_dir]):
            collect_dust(self.temp_dir, age_days=3)

        mock_old_file.unlink.assert_called_once_with()
        mock_unlink.assert_not_called() # The mock_old_file.unlink is called, not the global patch

    @patch('logging.error')
    def test_invalid_directory_path(self, mock_log_error):
        invalid_dir = Path("/non/existent/path/12345")
        collect_dust(invalid_dir, age_days=1)
        mock_log_error.assert_called_once()
        self.assertIn("does not exist or is not a directory", mock_log_error.call_args[0][0])

    @patch('datetime.datetime')
    @patch('pathlib.Path.unlink')
    @patch('pathlib.Path.stat')
    def test_zero_day_threshold_deletes_all_files(self, mock_stat, mock_unlink, mock_dt):
        # Mock rationale: We need to control the current time to deterministically test file age.
        mock_dt.now.return_value = self.mock_now
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Create multiple files, all will be older than 0 days relative to mock_now
        file1 = self._create_test_file("file1.log", self.mock_now - timedelta(hours=1))
        file2 = self._create_test_file("file2.txt", self.mock_now - timedelta(days=1))
        file3 = self._create_test_file("file3.tmp", self.mock_now - timedelta(days=10))

        # Mock rationale: We need to control file modification times to deterministically test file age.
        mock_stat_results = {
            file1: MagicMock(st_mtime=(self.mock_now - timedelta(hours=1)).timestamp()),
            file2: MagicMock(st_mtime=(self.mock_now - timedelta(days=1)).timestamp()),
            file3: MagicMock(st_mtime=(self.mock_now - timedelta(days=10)).timestamp()),
        }
        mock_stat.side_effect = lambda: mock_stat_results[mock_stat.call_args.self]

        # Mock rationale: We need to control Path.iterdir() to simulate directory contents.
        with patch('pathlib.Path.iterdir', return_value=[file1, file2, file3]):
            collect_dust(self.temp_dir, age_days=0) # 0 days means anything not created *exactly* now

        self.assertEqual(mock_unlink.call_count, 3)
        mock_unlink.assert_any_call()
        self.assertIn(mock_unlink.call_args_list[0].self, [file1, file2, file3])
        self.assertIn(mock_unlink.call_args_list[1].self, [file1, file2, file3])
        self.assertIn(mock_unlink.call_args_list[2].self, [file1, file2, file3])

if __name__ == '__main__':
    unittest.main()
