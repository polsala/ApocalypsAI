import unittest
from unittest.mock import patch, MagicMock
import os
import datetime
import time

# Import the function to be tested
from src.dust_collector import collect_dust, _is_dusty, _is_temp_file

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Define a fixed current time for deterministic age calculations
        self.fixed_current_time = datetime.datetime(2023, 10, 26, 10, 0, 0)
        self.fixed_current_timestamp = self.fixed_current_time.timestamp()

        # Define some mock file paths and their properties
        self.mock_files = {
            # Empty file
            '/test_dir/empty.txt': {'size': 0, 'mtime': (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()},
            # Old and small file (dust)
            '/test_dir/old_small.log': {'size': 500, 'mtime': (self.fixed_current_time - datetime.timedelta(days=100)).timestamp()},
            # Old but large file (not dust)
            '/test_dir/old_large.data': {'size': 20000, 'mtime': (self.fixed_current_time - datetime.timedelta(days=100)).timestamp()},
            # New and small file (not dust)
            '/test_dir/new_small.txt': {'size': 100, 'mtime': (self.fixed_current_time - datetime.timedelta(days=5)).timestamp()},
            # Temporary pattern files (dust)
            '/test_dir/temp_file.tmp': {'size': 100, 'mtime': (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()},
            '/test_dir/backup_file.bak': {'size': 200, 'mtime': (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()},
            '/test_dir/vim_swap.txt.swp': {'size': 300, 'mtime': (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()},
            '/test_dir/emacs_backup~': {'size': 50, 'mtime': (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()},
            '/test_dir/sub/another_temp#': {'size': 70, 'mtime': (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()},
            '/test_dir/sub/#hidden_temp': {'size': 80, 'mtime': (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()},
            # Regular file (not dust)
            '/test_dir/important.py': {'size': 1500, 'mtime': (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()},
            # File in quarantine dir (should be ignored by os.walk mock)
            '/quarantine_zone/quarantined_file.txt': {'size': 100, 'mtime': (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()}
        }

        # Mock os.stat for _is_dusty helper
        self.mock_stat_obj = MagicMock()
        self.mock_stat_obj.st_size = 0
        self.mock_stat_obj.st_mtime = 0

    @patch('time.time')
    @patch('os.stat')
    def test_is_dusty_empty_file(self, mock_os_stat, mock_time_time):
        # Mock rationale: Ensure _is_dusty correctly identifies empty files.
        mock_time_time.return_value = self.fixed_current_timestamp
        self.mock_stat_obj.st_size = 0
        mock_os_stat.return_value = self.mock_stat_obj
        is_dust, reason = _is_dusty('/path/to/empty.txt', 90, 1, self.fixed_current_timestamp)
        self.assertTrue(is_dust)
        self.assertEqual(reason, 'empty file')

    @patch('time.time')
    @patch('os.stat')
    def test_is_dusty_old_small_file(self, mock_os_stat, mock_time_time):
        # Mock rationale: Ensure _is_dusty correctly identifies old and small files.
        mock_time_time.return_value = self.fixed_current_timestamp
        self.mock_stat_obj.st_size = 500  # 0.5 KB
        self.mock_stat_obj.st_mtime = (self.fixed_current_time - datetime.timedelta(days=100)).timestamp()
        mock_os_stat.return_value = self.mock_stat_obj
        is_dust, reason = _is_dusty('/path/to/old_small.log', 90, 1, self.fixed_current_timestamp)
        self.assertTrue(is_dust)
        self.assertIn('old (100 days) and small (500 bytes)', reason)

    @patch('time.time')
    @patch('os.stat')
    def test_is_dusty_new_small_file(self, mock_os_stat, mock_time_time):
        # Mock rationale: Ensure _is_dusty does not flag new small files as dust.
        mock_time_time.return_value = self.fixed_current_timestamp
        self.mock_stat_obj.st_size = 500
        self.mock_stat_obj.st_mtime = (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()
        mock_os_stat.return_value = self.mock_stat_obj
        is_dust, _ = _is_dusty('/path/to/new_small.txt', 90, 1, self.fixed_current_timestamp)
        self.assertFalse(is_dust)

    @patch('time.time')
    @patch('os.stat')
    def test_is_dusty_old_large_file(self, mock_os_stat, mock_time_time):
        # Mock rationale: Ensure _is_dusty does not flag old large files as dust.
        mock_time_time.return_value = self.fixed_current_timestamp
        self.mock_stat_obj.st_size = 20000  # 20 KB
        self.mock_stat_obj.st_mtime = (self.fixed_current_time - datetime.timedelta(days=100)).timestamp()
        mock_os_stat.return_value = self.mock_stat_obj
        is_dust, _ = _is_dusty('/path/to/old_large.data', 90, 1, self.fixed_current_timestamp)
        self.assertFalse(is_dust)

    def test_is_temp_file(self):
        # Mock rationale: Test the helper for temporary file pattern matching.
        self.assertTrue(_is_temp_file('file.tmp'))
        self.assertTrue(_is_temp_file('document~'))
        self.assertTrue(_is_temp_file('config.bak'))
        self.assertTrue(_is_temp_file('main.py.swp'))
        self.assertTrue(_is_temp_file('#my_file.txt#'))
        self.assertTrue(_is_temp_file('._resource_fork'))
        self.assertFalse(_is_temp_file('regular_file.txt'))
        self.assertFalse(_is_temp_file('tempest.py')) # 'temp' is substring but not a pattern

    @patch('time.time')
    @patch('os.stat')
    def test_is_dusty_temp_file(self, mock_os_stat, mock_time_time):
        # Mock rationale: Ensure _is_dusty correctly identifies temporary pattern files.
        mock_time_time.return_value = self.fixed_current_timestamp
        self.mock_stat_obj.st_size = 100
        self.mock_stat_obj.st_mtime = (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()
        mock_os_stat.return_value = self.mock_stat_obj
        is_dust, reason = _is_dusty('/path/to/temp_file.tmp', 90, 1, self.fixed_current_timestamp)
        self.assertTrue(is_dust)
        self.assertEqual(reason, 'temporary pattern file')

    @patch('builtins.print')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('os.path.isdir', side_effect=lambda p: p in ['/test_dir', '/quarantine_zone', '/test_dir/sub'])
    @patch('os.path.exists', side_effect=lambda p: p in ['/test_dir', '/quarantine_zone', '/test_dir/sub'] or p in self.mock_files)
    @patch('os.stat', side_effect=lambda p: type('Stat', (object,), self.mock_files.get(p, {'size': 1, 'mtime': 0}))())
    @patch('os.walk')
    @patch('time.time')
    def test_collect_dust_dry_run(self, mock_time_time, mock_os_walk, mock_os_stat, mock_os_path_exists, mock_os_path_isdir, mock_os_makedirs, mock_shutil_move, mock_print):
        # Mock rationale: Test dry-run mode. No files should be moved, but dust should be reported.
        mock_time_time.return_value = self.fixed_current_timestamp

        # Configure os.walk to simulate a directory structure with various files
        mock_os_walk.return_value = [
            ('/test_dir', ['sub'], ['empty.txt', 'old_small.log', 'old_large.data', 'new_small.txt', 'temp_file.tmp', 'important.py']),
            ('/test_dir/sub', [], ['another_temp#', '#hidden_temp'])
        ]

        collect_dust(
            target_dir='/test_dir',
            quarantine_dir='/quarantine_zone',
            age_threshold_days=90,
            size_threshold_kb=1,
            dry_run=True
        )

        # Assert that shutil.move was NOT called
        mock_shutil_move.assert_not_called()
        mock_os_makedirs.assert_called_with('/quarantine_zone') # Quarantine dir should be created if not exists

        # Assert that relevant dust files were reported
        mock_print.assert_any_call('  [DUST] /test_dir/empty.txt (empty file)')
        mock_print.assert_any_call('  [DUST] /test_dir/old_small.log (old (100 days) and small (500 bytes))')
        mock_print.assert_any_call('  [DUST] /test_dir/temp_file.tmp (temporary pattern file)')
        mock_print.assert_any_call('  [DUST] /test_dir/sub/another_temp# (temporary pattern file)')
        mock_print.assert_any_call('  [DUST] /test_dir/sub/#hidden_temp (temporary pattern file)')

        # Assert that non-dust files were not reported as dust
        self.assertNotIn('  [DUST] /test_dir/old_large.data', [call.args[0] for call in mock_print.call_args_list])
        self.assertNotIn('  [DUST] /test_dir/new_small.txt', [call.args[0] for call in mock_print.call_args_list])
        self.assertNotIn('  [DUST] /test_dir/important.py', [call.args[0] for call in mock_print.call_args_list])

        # Check summary message
        mock_print.assert_any_call('\nSummary: 5 cosmic dust files reported.')

    @patch('builtins.print')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('os.path.isdir', side_effect=lambda p: p in ['/test_dir', '/quarantine_zone', '/test_dir/sub'])
    @patch('os.path.exists', side_effect=lambda p: p in ['/test_dir', '/quarantine_zone', '/test_dir/sub'] or p in self.mock_files)
    @patch('os.stat', side_effect=lambda p: type('Stat', (object,), self.mock_files.get(p, {'size': 1, 'mtime': 0}))())
    @patch('os.walk')
    @patch('time.time')
    def test_collect_dust_quarantine_mode(self, mock_time_time, mock_os_walk, mock_os_stat, mock_os_path_exists, mock_os_path_isdir, mock_os_makedirs, mock_shutil_move, mock_print):
        # Mock rationale: Test quarantine mode. Files should be moved, and relevant messages printed.
        mock_time_time.return_value = self.fixed_current_timestamp

        mock_os_walk.return_value = [
            ('/test_dir', ['sub'], ['empty.txt', 'old_small.log', 'temp_file.tmp']),
            ('/test_dir/sub', [], ['another_temp#'])
        ]

        collect_dust(
            target_dir='/test_dir',
            quarantine_dir='/quarantine_zone',
            age_threshold_days=90,
            size_threshold_kb=1,
            dry_run=False
        )

        # Assert that shutil.move was called for each dust file
        mock_shutil_move.assert_any_call('/test_dir/empty.txt', '/quarantine_zone/empty.txt')
        mock_shutil_move.assert_any_call('/test_dir/old_small.log', '/quarantine_zone/old_small.log')
        mock_shutil_move.assert_any_call('/test_dir/temp_file.tmp', '/quarantine_zone/temp_file.tmp')
        mock_shutil_move.assert_any_call('/test_dir/sub/another_temp#', '/quarantine_zone/sub/another_temp#')
        self.assertEqual(mock_shutil_move.call_count, 4)

        # Assert that quarantine directory creation was handled
        mock_os_makedirs.assert_any_call('/quarantine_zone')
        mock_os_makedirs.assert_any_call('/quarantine_zone/sub', exist_ok=True)

        # Check summary message
        mock_print.assert_any_call('\nSummary: 4 cosmic dust files quarantined.')

    @patch('builtins.print')
    @patch('os.path.isdir', return_value=False)
    def test_collect_dust_invalid_target_dir(self, mock_os_path_isdir, mock_print):
        # Mock rationale: Ensure the utility handles non-existent target directories gracefully.
        collect_dust('/non_existent_dir', '/quarantine_zone')
        mock_print.assert_any_call("Error: Target directory '/non_existent_dir' does not exist or is not a directory.")

    @patch('builtins.print')
    @patch('os.path.isdir', side_effect=lambda p: p == '/test_dir')
    @patch('os.path.exists', side_effect=lambda p: p == '/test_dir' or p == '/quarantine_zone_file')
    def test_collect_dust_invalid_quarantine_dir(self, mock_os_path_exists, mock_os_path_isdir, mock_print):
        # Mock rationale: Ensure the utility handles quarantine path being a file, not a directory.
        collect_dust('/test_dir', '/quarantine_zone_file')
        mock_print.assert_any_call("Error: Quarantine path '/quarantine_zone_file' exists but is not a directory.")

    @patch('builtins.print')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('os.path.isdir', side_effect=lambda p: p in ['/test_dir', '/quarantine_zone'])
    @patch('os.path.exists', side_effect=lambda p: p in ['/test_dir', '/quarantine_zone'])
    @patch('os.stat', side_effect=lambda p: type('Stat', (object,), {'size': 100, 'mtime': (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()})())
    @patch('os.walk')
    @patch('time.time')
    def test_collect_dust_no_dust_found(self, mock_time_time, mock_os_walk, mock_os_stat, mock_os_path_exists, mock_os_path_isdir, mock_os_makedirs, mock_shutil_move, mock_print):
        # Mock rationale: Test scenario where no dust is found.
        mock_time_time.return_value = self.fixed_current_timestamp
        mock_os_walk.return_value = [
            ('/test_dir', [], ['clean_file.txt', 'another_clean.py'])
        ]

        collect_dust(
            target_dir='/test_dir',
            quarantine_dir='/quarantine_zone',
            age_threshold_days=1,
            size_threshold_kb=1000,
            dry_run=True
        )

        mock_shutil_move.assert_not_called()
        mock_print.assert_any_call('No cosmic dust found. Your directories are sparkling clean!')

    @patch('builtins.print')
    @patch('shutil.move', side_effect=OSError("Permission denied"))
    @patch('os.makedirs')
    @patch('os.path.isdir', side_effect=lambda p: p in ['/test_dir', '/quarantine_zone'])
    @patch('os.path.exists', side_effect=lambda p: p in ['/test_dir', '/quarantine_zone'] or p == '/test_dir/empty.txt')
    @patch('os.stat', side_effect=lambda p: type('Stat', (object,), {'size': 0, 'mtime': (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()})())
    @patch('os.walk')
    @patch('time.time')
    def test_collect_dust_quarantine_failure(self, mock_time_time, mock_os_walk, mock_os_stat, mock_os_path_exists, mock_os_path_isdir, mock_os_makedirs, mock_shutil_move, mock_print):
        # Mock rationale: Test error handling during file quarantine.
        mock_time_time.return_value = self.fixed_current_timestamp
        mock_os_walk.return_value = [
            ('/test_dir', [], ['empty.txt'])
        ]

        collect_dust(
            target_dir='/test_dir',
            quarantine_dir='/quarantine_zone',
            dry_run=False
        )

        mock_print.assert_any_call('  [DUST] /test_dir/empty.txt (empty file)')
        mock_print.assert_any_call('    -> Failed to quarantine /test_dir/empty.txt: Permission denied')
        mock_shutil_move.assert_called_once_with('/test_dir/empty.txt', '/quarantine_zone/empty.txt')

if __name__ == '__main__':
    unittest.main()
