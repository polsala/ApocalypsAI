import unittest
from unittest.mock import patch, MagicMock, call
import os
import time
from datetime import datetime, timedelta
from src.collector import find_cosmic_dust, clean_cosmic_dust, get_file_age_in_days

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Mock current time for deterministic age calculations
        self.mock_current_time = time.mktime((2023, 10, 26, 10, 0, 0, 0, 0, 0))
        self.patcher_time_time = patch('time.time', return_value=self.mock_current_time)
        self.mock_time_time = self.patcher_time_time.start()

    def tearDown(self):
        self.patcher_time_time.stop()

    @patch('os.path.getmtime')
    def test_get_file_age_in_days(self, mock_getmtime):
        # Mock rationale: `os.path.getmtime` is a system call that depends on file system state.
        # Mocking it allows deterministic testing of age calculation logic.
        
        # File modified 10 days ago
        mock_getmtime.return_value = self.mock_current_time - (10 * 24 * 3600)
        self.assertAlmostEqual(get_file_age_in_days("dummy_file.txt"), 10.0)

        # File modified 40 days ago
        mock_getmtime.return_value = self.mock_current_time - (40 * 24 * 3600)
        self.assertAlmostEqual(get_file_age_in_days("dummy_file.txt"), 40.0)

    @patch('os.path.isfile', return_value=True) # Mock rationale: `os.path.isfile` is a system call. Mocking it ensures paths are treated as files.
    @patch('os.path.isdir', return_value=False) # Mock rationale: `os.path.isdir` is a system call. Mocking it ensures paths are not treated as directories.
    @patch('os.path.getmtime') # Mock rationale: `os.path.getmtime` is a system call. Mocking it allows deterministic age calculation.
    @patch('os.walk') # Mock rationale: `os.walk` traverses the file system. Mocking it allows simulating arbitrary directory structures offline.
    def test_find_cosmic_dust_files_and_empty_dirs(self, mock_os_walk, mock_getmtime, mock_isdir, mock_isfile):
        # Simulate a file system structure
        # root, dirs, files
        mock_os_walk.return_value = [
            ('/test_root', ['subdir1', 'subdir2', 'empty_dir'], ['file.txt', 'old.log', 'recent.tmp']),
            ('/test_root/subdir1', [], ['another.bak', 'important.py']),
            ('/test_root/subdir2', ['nested_empty'], ['config.ini']),
            ('/test_root/subdir2/nested_empty', [], []), # This will be an empty dir
            ('/test_root/empty_dir', [], []), # This will be an empty dir
        ]

        # Set modification times for files
        # old.log: 40 days old (should be collected)
        # recent.tmp: 10 days old (should NOT be collected, too recent)
        # another.bak: 35 days old (should be collected)
        # file.txt, important.py, config.ini: not temp extensions, so ignored
        
        def mock_getmtime_side_effect(path):
            if 'old.log' in path:
                return self.mock_current_time - (40 * 24 * 3600)
            elif 'recent.tmp' in path:
                return self.mock_current_time - (10 * 24 * 3600)
            elif 'another.bak' in path:
                return self.mock_current_time - (35 * 24 * 3600)
            else:
                return self.mock_current_time - (5 * 24 * 3600) # Default recent

        mock_getmtime.side_effect = mock_getmtime_side_effect

        dust_files, empty_dirs = find_cosmic_dust('/test_root', age_threshold_days=30)

        expected_dust_files = [
            os.path.join('/test_root', 'old.log'),
            os.path.join('/test_root', 'subdir1', 'another.bak'),
        ]
        expected_empty_dirs = [
            os.path.join('/test_root', 'subdir2', 'nested_empty'),
            os.path.join('/test_root', 'empty_dir'),
        ]

        self.assertCountEqual(dust_files, expected_dust_files)
        self.assertCountEqual(empty_dirs, expected_empty_dirs)

    @patch('os.path.isfile', return_value=True)
    @patch('os.path.isdir', return_value=False)
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_cosmic_dust_with_exclusions(self, mock_os_walk, mock_getmtime, mock_isdir, mock_isfile):
        mock_os_walk.return_value = [
            ('/test_root', ['node_modules', 'logs'], ['old.log', 'temp.tmp']),
            ('/test_root/node_modules', [], ['cache.tmp']),
            ('/test_root/logs', [], ['app.log']),
        ]

        def mock_getmtime_side_effect(path):
            return self.mock_current_time - (40 * 24 * 3600) # All files are old

        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Exclude 'node_modules' and 'logs'
        dust_files, empty_dirs = find_cosmic_dust(
            '/test_root',
            age_threshold_days=30,
            exclude_patterns=['node_modules', 'logs']
        )

        expected_dust_files = [
            os.path.join('/test_root', 'old.log'),
            os.path.join('/test_root', 'temp.tmp'),
        ]
        
        self.assertCountEqual(dust_files, expected_dust_files)
        self.assertEqual(empty_dirs, []) # No empty dirs in this mock setup

        # Test with a more specific exclusion for files
        dust_files, empty_dirs = find_cosmic_dust(
            '/test_root',
            age_threshold_days=30,
            exclude_patterns=['node_modules', 'app.log'] # Exclude app.log specifically
        )
        expected_dust_files = [
            os.path.join('/test_root', 'old.log'),
            os.path.join('/test_root', 'temp.tmp'),
        ]
        self.assertCountEqual(dust_files, expected_dust_files)


    @patch('builtins.print') # Mock rationale: `print` is an I/O operation. Mocking it allows capturing and asserting console output.
    @patch('os.remove') # Mock rationale: `os.remove` is a system call. Mocking it prevents actual file deletion during tests.
    @patch('os.rmdir') # Mock rationale: `os.rmdir` is a system call. Mocking it prevents actual directory deletion during tests.
    def test_clean_cosmic_dust_dry_run(self, mock_rmdir, mock_remove, mock_print):
        dust_files = ['/path/to/old.log', '/path/to/temp.tmp']
        empty_dirs = ['/path/to/empty_dir']

        clean_cosmic_dust(dust_files, empty_dirs, dry_run=True)

        mock_remove.assert_not_called()
        mock_rmdir.assert_not_called()
        
        # Assert that print was called with expected messages (order might vary for files/dirs sections)
        output_calls = [call.args[0] for call in mock_print.call_args_list]
        self.assertIn("--- Cosmic Dust Collection Report (Dry Run) ---", output_calls)
        self.assertIn("\nFiles to be swept away:", output_calls)
        self.assertIn("  - /path/to/old.log", output_calls)
        self.assertIn("  - /path/to/temp.tmp", output_calls)
        self.assertIn("\nEmpty directories to be collapsed:", output_calls)
        self.assertIn("  - /path/to/empty_dir", output_calls)
        self.assertIn("--- Collection Complete ---", output_calls)

    @patch('builtins.print')
    @patch('os.remove')
    @patch('os.rmdir')
    def test_clean_cosmic_dust_actual_clean(self, mock_rmdir, mock_remove, mock_print):
        dust_files = ['/path/to/old.log', '/path/to/temp.tmp']
        empty_dirs = ['/path/to/empty_dir/nested', '/path/to/empty_dir'] # Test sorting for rmdir

        clean_cosmic_dust(dust_files, empty_dirs, dry_run=False)

        mock_remove.assert_any_call('/path/to/old.log')
        mock_remove.assert_any_call('/path/to/temp.tmp')
        self.assertEqual(mock_remove.call_count, 2)

        # Ensure rmdir is called in correct order (deepest first)
        self.assertEqual(mock_rmdir.call_args_list[0].args[0], '/path/to/empty_dir/nested')
        self.assertEqual(mock_rmdir.call_args_list[1].args[0], '/path/to/empty_dir')
        self.assertEqual(mock_rmdir.call_count, 2)

        output_calls = [call.args[0] for call in mock_print.call_args_list]
        self.assertIn("--- Cosmic Dust Collection Report (Cleaning) ---", output_calls)
        self.assertIn("    [REMOVED] /path/to/old.log", output_calls)
        self.assertIn("    [REMOVED] /path/to/temp.tmp", output_calls)
        self.assertIn("    [REMOVED] /path/to/empty_dir/nested", output_calls)
        self.assertIn("    [REMOVED] /path/to/empty_dir", output_calls)

    @patch('builtins.print')
    @patch('os.remove', side_effect=OSError("Permission denied")) # Mock rationale: Simulate OS errors during deletion.
    @patch('os.rmdir')
    def test_clean_cosmic_dust_error_handling(self, mock_rmdir, mock_remove, mock_print):
        dust_files = ['/path/to/unremovable.log']
        empty_dirs = []

        clean_cosmic_dust(dust_files, empty_dirs, dry_run=False)

        mock_remove.assert_called_once_with('/path/to/unremovable.log')
        mock_rmdir.assert_not_called()

        output_calls = [call.args[0] for call in mock_print.call_args_list]
        self.assertIn("    [ERROR] Could not remove /path/to/unremovable.log: Permission denied", output_calls)

    @patch('builtins.print')
    @patch('os.remove')
    @patch('os.rmdir')
    def test_clean_cosmic_dust_no_dust(self, mock_rmdir, mock_remove, mock_print):
        dust_files = []
        empty_dirs = []

        clean_cosmic_dust(dust_files, empty_dirs, dry_run=True)

        mock_remove.assert_not_called()
        mock_rmdir.assert_not_called()

        output_calls = [call.args[0] for call in mock_print.call_args_list]
        self.assertIn("No cosmic dust detected. Your digital cosmos is pristine!", output_calls)


if __name__ == '__main__':
    unittest.main()
