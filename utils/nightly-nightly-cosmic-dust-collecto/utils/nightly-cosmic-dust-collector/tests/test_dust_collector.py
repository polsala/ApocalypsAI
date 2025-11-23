import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from datetime import datetime, timedelta

# Mock rationale: We need to simulate file system interactions (listing files, getting sizes, modification times, moving files)
# without actually touching the disk. This ensures tests are fast, deterministic, and isolated from the host file system.

# Patch datetime.now to ensure consistent 'current time' for age calculations.
# Mock rationale: File age calculations depend on the current time. Patching `datetime.now` makes these calculations deterministic
# across different test runs and environments.
FIXED_NOW = datetime(2023, 10, 26, 10, 0, 0)

class TestDustCollector(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('builtins.print') # Mock rationale: Suppress print output during tests for cleaner console.
    @patch('dust_collector.datetime') # Mock rationale: Control datetime.now() for consistent age calculations.
    def test_collect_dust_dry_run_empty_and_small_files(self, mock_datetime, mock_print, mock_makedirs, mock_move, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        from src.dust_collector import collect_dust

        mock_datetime.now.return_value = FIXED_NOW
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.timedelta = timedelta # Ensure timedelta works as expected

        target_dir = '/mock/project'
        dustbin_dir = '/mock/dustbin'

        mock_isdir.return_value = True # Mock rationale: Assume target_dir exists.

        # Mock rationale: Simulate a directory structure with various file types and sizes.
        mock_walk.return_value = [
            (target_dir, [], ['empty.txt', 'small.log', 'large.py', 'temp.tmp', 'recent.tmp']),
            (os.path.join(target_dir, 'subdir'), [], ['another_empty.txt', 'config.ini'])
        ]

        # Mock rationale: Control file sizes for `is_empty_file` and `is_small_file` logic.
        mock_getsize.side_effect = lambda p:
            0 if 'empty' in p else \
            500 if 'small' in p else \
            2000 if 'large' in p else \
            100 if 'temp' in p else \
            1000 if 'config' in p else \
            0 # Default for unexpected paths

        # Mock rationale: Control file modification times for `is_old_temp_file` logic.
        # Fixed_now - 40 days for old temp, Fixed_now - 5 days for recent temp
        mock_getmtime.side_effect = lambda p:
            (FIXED_NOW - timedelta(days=40)).timestamp() if 'temp.tmp' in p else \
            (FIXED_NOW - timedelta(days=5)).timestamp() if 'recent.tmp' in p else \
            (FIXED_NOW - timedelta(days=10)).timestamp() # Default for others

        # Test with default max_size_kb=1 (1024 bytes), max_age_days=30
        collected = collect_dust(target_dir, dustbin_dir, dry_run=True)

        self.assertEqual(len(collected), 4)
        self.assertIn((os.path.join(target_dir, 'empty.txt'), 'empty'), collected)
        self.assertIn((os.path.join(target_dir, 'small.log'), 'small (<1KB)'), collected)
        self.assertIn((os.path.join(target_dir, 'temp.tmp'), 'old temp (>30 days)'), collected)
        self.assertIn((os.path.join(target_dir, 'subdir', 'another_empty.txt'), 'empty'), collected)

        self.assertNotIn((os.path.join(target_dir, 'large.py'), 'small (<1KB)'), collected) # Too large
        self.assertNotIn((os.path.join(target_dir, 'recent.tmp'), 'old temp (>30 days)'), collected) # Too recent
        self.assertNotIn((os.path.join(target_dir, 'config.ini'), 'small (<1KB)'), collected) # Not small enough and not temp

        mock_move.assert_not_called() # Mock rationale: In dry-run mode, no files should be moved.
        mock_makedirs.assert_not_called() # Mock rationale: In dry-run mode, dustbin should not be created.

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('builtins.print')
    @patch('dust_collector.datetime')
    def test_collect_dust_move_mode(self, mock_datetime, mock_print, mock_makedirs, mock_move, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        from src.dust_collector import collect_dust

        mock_datetime.now.return_value = FIXED_NOW
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.timedelta = timedelta

        target_dir = '/mock/project'
        dustbin_dir = '/mock/dustbin'

        mock_isdir.return_value = True

        mock_walk.return_value = [
            (target_dir, [], ['empty.txt', 'small.log']),
            (os.path.join(target_dir, 'subdir'), [], ['temp.tmp'])
        ]

        mock_getsize.side_effect = lambda p:
            0 if 'empty' in p else \
            500 if 'small' in p else \
            100 if 'temp' in p else \
            0

        mock_getmtime.side_effect = lambda p:
            (FIXED_NOW - timedelta(days=40)).timestamp() if 'temp.tmp' in p else \
            (FIXED_NOW - timedelta(days=10)).timestamp()

        collected = collect_dust(target_dir, dustbin_dir, dry_run=False, max_size_kb=1, max_age_days=30)

        self.assertEqual(len(collected), 3)
        self.assertIn((os.path.join(target_dir, 'empty.txt'), 'empty'), collected)
        self.assertIn((os.path.join(target_dir, 'small.log'), 'small (<1KB)'), collected)
        self.assertIn((os.path.join(target_dir, 'subdir', 'temp.tmp'), 'old temp (>30 days)'), collected)

        # Mock rationale: Verify that files are moved to the correct destination paths.
        mock_move.assert_any_call(os.path.join(target_dir, 'empty.txt'), os.path.join(dustbin_dir, 'empty.txt'))
        mock_move.assert_any_call(os.path.join(target_dir, 'small.log'), os.path.join(dustbin_dir, 'small.log'))
        mock_move.assert_any_call(os.path.join(target_dir, 'subdir', 'temp.tmp'), os.path.join(dustbin_dir, 'subdir', 'temp.tmp'))
        self.assertEqual(mock_move.call_count, 3)

        # Mock rationale: Ensure the dustbin directory and its subdirectories are created.
        mock_makedirs.assert_any_call(dustbin_dir, exist_ok=True)
        mock_makedirs.assert_any_call(os.path.join(dustbin_dir, 'subdir'), exist_ok=True)
        self.assertEqual(mock_makedirs.call_count, 2) # Once for dustbin_dir, once for dustbin_dir/subdir

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('builtins.print')
    @patch('dust_collector.datetime')
    def test_collect_dust_no_dust_found(self, mock_datetime, mock_print, mock_makedirs, mock_move, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        from src.dust_collector import collect_dust

        mock_datetime.now.return_value = FIXED_NOW
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.timedelta = timedelta

        target_dir = '/mock/project'
        dustbin_dir = '/mock/dustbin'

        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory with only large, recent, non-temp files.
        mock_walk.return_value = [
            (target_dir, [], ['important.txt', 'code.py'])
        ]

        mock_getsize.side_effect = lambda p:
            5000 if 'important' in p else \
            10000 if 'code' in p else \
            0

        mock_getmtime.side_effect = lambda p:
            (FIXED_NOW - timedelta(days=1)).timestamp() # All files are recent

        collected = collect_dust(target_dir, dustbin_dir, dry_run=True)

        self.assertEqual(len(collected), 0)
        mock_move.assert_not_called()
        mock_makedirs.assert_not_called()
        # Mock rationale: Verify that the 'no dust found' message is printed.
        mock_print.assert_any_call('No cosmic dust found. Your space is pristine!')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('builtins.print')
    @patch('dust_collector.datetime')
    def test_collect_dust_custom_parameters(self, mock_datetime, mock_print, mock_makedirs, mock_move, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        from src.dust_collector import collect_dust

        mock_datetime.now.return_value = FIXED_NOW
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.timedelta = timedelta

        target_dir = '/mock/project'
        dustbin_dir = '/mock/dustbin'

        mock_isdir.return_value = True

        mock_walk.return_value = [
            (target_dir, [], ['medium.txt', 'old.log', 'custom.temp'])
        ]

        mock_getsize.side_effect = lambda p:
            3000 if 'medium' in p else \
            1500 if 'old.log' in p else \
            200 if 'custom.temp' in p else \
            0

        mock_getmtime.side_effect = lambda p:
            (FIXED_NOW - timedelta(days=60)).timestamp() if 'old.log' in p else \
            (FIXED_NOW - timedelta(days=100)).timestamp() if 'custom.temp' in p else \
            (FIXED_NOW - timedelta(days=10)).timestamp()

        # Test with custom max_size_kb=2 (2048 bytes), max_age_days=90, temp_patterns=['.temp']
        collected = collect_dust(
            target_dir, dustbin_dir, dry_run=True,
            max_size_kb=2, max_age_days=90, temp_patterns=['.temp']
        )

        self.assertEqual(len(collected), 1)
        self.assertIn((os.path.join(target_dir, 'custom.temp'), 'old temp (>90 days)'), collected)

        self.assertNotIn((os.path.join(target_dir, 'medium.txt'), 'small (<2KB)'), collected) # Too large
        self.assertNotIn((os.path.join(target_dir, 'old.log'), 'old temp (>90 days)'), collected) # Not a custom temp pattern

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('builtins.print')
    @patch('dust_collector.datetime')
    def test_collect_dust_target_dir_not_found(self, mock_datetime, mock_print, mock_makedirs, mock_move, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        from src.dust_collector import collect_dust

        mock_isdir.return_value = False # Mock rationale: Simulate target directory not existing.

        target_dir = '/nonexistent/project'
        dustbin_dir = '/mock/dustbin'

        collected = collect_dust(target_dir, dustbin_dir, dry_run=True)

        self.assertEqual(len(collected), 0)
        mock_print.assert_any_call(f"Error: Target directory '{target_dir}' does not exist.")
        mock_walk.assert_not_called()
        mock_move.assert_not_called()
        mock_makedirs.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('builtins.print')
    @patch('dust_collector.datetime')
    def test_collect_dust_os_error_during_processing(self, mock_datetime, mock_print, mock_makedirs, mock_move, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        from src.dust_collector import collect_dust

        mock_datetime.now.return_value = FIXED_NOW
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)
        mock_datetime.timedelta = timedelta

        target_dir = '/mock/project'
        dustbin_dir = '/mock/dustbin'

        mock_isdir.return_value = True

        mock_walk.return_value = [
            (target_dir, [], ['problem_file.txt', 'normal_file.txt'])
        ]

        # Mock rationale: Simulate an OSError when trying to get size of 'problem_file.txt'.
        def mock_getsize_side_effect(path):
            if 'problem_file.txt' in path:
                raise OSError("Permission denied")
            return 0 # normal_file.txt is empty

        mock_getsize.side_effect = mock_getsize_side_effect
        mock_getmtime.return_value = (FIXED_NOW - timedelta(days=10)).timestamp()

        collected = collect_dust(target_dir, dustbin_dir, dry_run=True)

        self.assertEqual(len(collected), 1)
        self.assertIn((os.path.join(target_dir, 'normal_file.txt'), 'empty'), collected)
        # Mock rationale: Verify that the warning message for the problematic file is printed.
        mock_print.assert_any_call(f"  Warning: Could not process '{os.path.join(target_dir, 'problem_file.txt')}': Permission denied")
        mock_move.assert_not_called()

if __name__ == '__main__':
    unittest.main()
