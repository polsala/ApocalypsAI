import unittest
import os
import time
import argparse
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Import the script to be tested
import src.cleaner as cleaner_script

class TestTemporalCacheCleaner(unittest.TestCase):

    # Mock rationale: To fix the 'current time' for age calculations, making tests deterministic.
    @patch('datetime.datetime')
    def test_find_old_files_dry_run(self, mock_datetime):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

        # Mock rationale: Simulate a directory structure without creating actual files.
        mock_os_walk = [
            ('/test_dir', [], ['file1.txt', 'file2.log']),
            ('/test_dir/subdir', [], ['file3.tmp'])
        ]
        # Mock rationale: Control modification times for simulated files.
        # file1.txt: 60 days old (older than 30 days cutoff)
        # file2.log: 10 days old (newer than 30 days cutoff)
        # file3.tmp: 40 days old (older than 30 days cutoff)
        mock_os_path_getmtime = {
            '/test_dir/file1.txt': (datetime(2023, 8, 27, 9, 0, 0)).timestamp(), # ~60 days old
            '/test_dir/file2.log': (datetime(2023, 10, 16, 9, 0, 0)).timestamp(), # ~10 days old
            '/test_dir/subdir/file3.tmp': (datetime(2023, 9, 16, 9, 0, 0)).timestamp() # ~40 days old
        }

        # Mock rationale: Ensure os.path.isdir returns true for the base path.
        mock_os_path_isdir = lambda p: p == '/test_dir'

        with patch('os.walk', return_value=mock_os_walk),
             patch('os.path.getmtime', side_effect=lambda p: mock_os_path_getmtime[p]),
             patch('os.path.isdir', side_effect=mock_os_path_isdir),
             patch('os.remove') as mock_os_remove,
             patch('builtins.print') as mock_print:

            # Test dry run (default behavior)
            cleaner_script.main.__globals__['argparse'].ArgumentParser.parse_args.return_value = MagicMock(
                path='/test_dir', age=30, dry_run=True, delete=False
            )
            cleaner_script.main()

            expected_old_files = [
                '/test_dir/file1.txt',
                '/test_dir/subdir/file3.tmp'
            ]
            self.assertIn(f"Found {len(expected_old_files)} old files:", mock_print.call_args_list[1].args[0])
            self.assertIn(f"  - {expected_old_files[0]}", mock_print.call_args_list[2].args[0])
            self.assertIn(f"  - {expected_old_files[1]}", mock_print.call_args_list[3].args[0])
            self.assertIn("This was a DRY RUN. No files were deleted.", mock_print.call_args_list[4].args[0])
            mock_os_remove.assert_not_called()

    # Mock rationale: To fix the 'current time' for age calculations, making tests deterministic.
    @patch('datetime.datetime')
    def test_find_old_files_delete(self, mock_datetime):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

        # Mock rationale: Simulate a directory structure without creating actual files.
        mock_os_walk = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]
        # Mock rationale: Control modification times for simulated files.
        # file1.txt: 60 days old (older than 30 days cutoff)
        # file2.log: 10 days old (newer than 30 days cutoff)
        mock_os_path_getmtime = {
            '/test_dir/file1.txt': (datetime(2023, 8, 27, 9, 0, 0)).timestamp(), # ~60 days old
            '/test_dir/file2.log': (datetime(2023, 10, 16, 9, 0, 0)).timestamp() # ~10 days old
        }

        # Mock rationale: Ensure os.path.isdir returns true for the base path.
        mock_os_path_isdir = lambda p: p == '/test_dir'

        with patch('os.walk', return_value=mock_os_walk),
             patch('os.path.getmtime', side_effect=lambda p: mock_os_path_getmtime[p]),
             patch('os.path.isdir', side_effect=mock_os_path_isdir),
             patch('os.remove') as mock_os_remove,
             patch('builtins.print') as mock_print:

            # Test delete mode
            cleaner_script.main.__globals__['argparse'].ArgumentParser.parse_args.return_value = MagicMock(
                path='/test_dir', age=30, dry_run=False, delete=True
            )
            cleaner_script.main()

            expected_old_files = ['/test_dir/file1.txt']
            self.assertIn(f"Found {len(expected_old_files)} old files:", mock_print.call_args_list[1].args[0])
            self.assertIn(f"  - {expected_old_files[0]}", mock_print.call_args_list[2].args[0])
            self.assertIn("Initiating temporal stabilization (deletion)...", mock_print.call_args_list[3].args[0])
            mock_os_remove.assert_called_once_with('/test_dir/file1.txt')
            self.assertIn("Temporal stabilization complete. 1 files removed.", mock_print.call_args_list[5].args[0])

    # Mock rationale: To fix the 'current time' for age calculations, making tests deterministic.
    @patch('datetime.datetime')
    def test_no_old_files(self, mock_datetime):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

        # Mock rationale: Simulate a directory structure without creating actual files.
        mock_os_walk = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]
        # Mock rationale: Control modification times for simulated files (all newer than cutoff).
        mock_os_path_getmtime = {
            '/test_dir/file1.txt': (datetime(2023, 10, 20, 9, 0, 0)).timestamp(), # ~6 days old
            '/test_dir/file2.log': (datetime(2023, 10, 16, 9, 0, 0)).timestamp() # ~10 days old
        }

        # Mock rationale: Ensure os.path.isdir returns true for the base path.
        mock_os_path_isdir = lambda p: p == '/test_dir'

        with patch('os.walk', return_value=mock_os_walk),
             patch('os.path.getmtime', side_effect=lambda p: mock_os_path_getmtime[p]),
             patch('os.path.isdir', side_effect=mock_os_path_isdir),
             patch('os.remove') as mock_os_remove,
             patch('builtins.print') as mock_print:

            cleaner_script.main.__globals__['argparse'].ArgumentParser.parse_args.return_value = MagicMock(
                path='/test_dir', age=5, dry_run=True, delete=False
            )
            cleaner_script.main()

            self.assertIn("No old files found. Your temporal cache is pristine!", mock_print.call_args_list[1].args[0])
            mock_os_remove.assert_not_called()

    # Mock rationale: To fix the 'current time' for age calculations, making tests deterministic.
    @patch('datetime.datetime')
    def test_empty_directory(self, mock_datetime):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

        # Mock rationale: Simulate an empty directory.
        mock_os_walk = [
            ('/test_dir', [], [])
        ]

        # Mock rationale: Ensure os.path.isdir returns true for the base path.
        mock_os_path_isdir = lambda p: p == '/test_dir'

        with patch('os.walk', return_value=mock_os_walk),
             patch('os.path.getmtime'), # Not called if no files
             patch('os.path.isdir', side_effect=mock_os_path_isdir),
             patch('os.remove') as mock_os_remove,
             patch('builtins.print') as mock_print:

            cleaner_script.main.__globals__['argparse'].ArgumentParser.parse_args.return_value = MagicMock(
                path='/test_dir', age=30, dry_run=True, delete=False
            )
            cleaner_script.main()

            self.assertIn("No old files found. Your temporal cache is pristine!", mock_print.call_args_list[1].args[0])
            mock_os_remove.assert_not_called()

    # Mock rationale: To fix the 'current time' for age calculations, making tests deterministic.
    @patch('datetime.datetime')
    def test_path_not_directory(self, mock_datetime):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

        # Mock rationale: Simulate that the path is not a directory.
        mock_os_path_isdir = lambda p: p != '/not_a_dir'

        with patch('os.walk') as mock_os_walk,
             patch('os.path.getmtime'),
             patch('os.path.isdir', side_effect=mock_os_path_isdir),
             patch('os.remove') as mock_os_remove,
             patch('builtins.print') as mock_print:

            cleaner_script.main.__globals__['argparse'].ArgumentParser.parse_args.return_value = MagicMock(
                path='/not_a_dir', age=30, dry_run=True, delete=False
            )
            cleaner_script.main()

            self.assertIn("Error: Path '/not_a_dir' is not a valid directory.", mock_print.call_args_list[0].args[0])
            mock_os_walk.assert_not_called()
            mock_os_remove.assert_not_called()

    # Mock rationale: To fix the 'current time' for age calculations, making tests deterministic.
    @patch('datetime.datetime')
    def test_deletion_error_handling(self, mock_datetime):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

        # Mock rationale: Simulate a directory structure with one old file.
        mock_os_walk = [
            ('/test_dir', [], ['unreachable_file.txt'])
        ]
        # Mock rationale: Control modification times for simulated files.
        mock_os_path_getmtime = {
            '/test_dir/unreachable_file.txt': (datetime(2023, 8, 27, 9, 0, 0)).timestamp() # ~60 days old
        }

        # Mock rationale: Ensure os.path.isdir returns true for the base path.
        mock_os_path_isdir = lambda p: p == '/test_dir'

        with patch('os.walk', return_value=mock_os_walk),
             patch('os.path.getmtime', side_effect=lambda p: mock_os_path_getmtime[p]),
             patch('os.path.isdir', side_effect=mock_os_path_isdir),
             patch('os.remove', side_effect=OSError("Permission denied")) as mock_os_remove,
             patch('builtins.print') as mock_print:

            cleaner_script.main.__globals__['argparse'].ArgumentParser.parse_args.return_value = MagicMock(
                path='/test_dir', age=30, dry_run=False, delete=True
            )
            cleaner_script.main()

            self.assertIn("Error deleting '/test_dir/unreachable_file.txt': Permission denied", mock_print.call_args_list[4].args[0])
            mock_os_remove.assert_called_once_with('/test_dir/unreachable_file.txt')
            self.assertIn("Temporal stabilization complete. 0 files removed.", mock_print.call_args_list[5].args[0])

if __name__ == '__main__':
    unittest.main()
