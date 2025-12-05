import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Mock rationale: We need to simulate file system interactions without actually
# creating or deleting files on the disk. This ensures tests are deterministic,
# fast, and do not have side effects on the user's system.
# os.walk: Simulates directory traversal.
# os.path.exists: Controls which paths are considered valid.
# os.path.getmtime: Simulates file modification times for age-based checks.
# os.remove, os.rmdir: Verifies that deletion calls are made without actual deletion.
# os.listdir: Simulates directory contents for empty directory checks.

# Import the class to be tested
from src.collector import CosmicDustCollector

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        self.collector = CosmicDustCollector()
        self.mock_time = time.time()

    @patch('os.path.exists', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    def test_scan_temp_files(self, mock_listdir, mock_getmtime, mock_walk, mock_exists):
        # Mock rationale: Simulate a directory with various temporary files.
        mock_walk.return_value = [
            ('/mock/path', [], ['file.txt', 'temp.tmp', 'backup.bak', '.~hidden', '#temp#'])
        ]
        mock_getmtime.return_value = self.mock_time # Not relevant for temp files, but good practice
        mock_listdir.return_value = ['file.txt', 'temp.tmp'] # Not relevant for file checks

        findings = self.collector.scan(['/mock/path'])

        self.assertIn('/mock/path/temp.tmp', findings['temp_files'])
        self.assertIn('/mock/path/backup.bak', findings['temp_files'])
        self.assertIn('/mock/path/.~hidden', findings['temp_files'])
        self.assertIn('/mock/path/#temp#', findings['temp_files'])
        self.assertNotIn('/mock/path/file.txt', findings['temp_files'])
        self.assertEqual(len(findings['old_logs']), 0)
        self.assertEqual(len(findings['empty_dirs']), 0)

    @patch('os.path.exists', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    def test_scan_old_logs(self, mock_listdir, mock_getmtime, mock_walk, mock_exists):
        # Mock rationale: Simulate a directory with log files, some old, some new.
        old_log_mtime = self.mock_time - (40 * 24 * 3600) # 40 days old
        new_log_mtime = self.mock_time - (10 * 24 * 3600) # 10 days old

        mock_walk.return_value = [
            ('/mock/path', [], ['app.log', 'server.log', 'debug.txt'])
        ]
        # Mock rationale: Control the modification time for specific files.
        def getmtime_side_effect(path):
            if path == '/mock/path/app.log':
                return old_log_mtime
            elif path == '/mock/path/server.log':
                return new_log_mtime
            return self.mock_time # Default for others

        mock_getmtime.side_effect = getmtime_side_effect
        mock_listdir.return_value = ['app.log', 'server.log']

        findings = self.collector.scan(['/mock/path'], age_days=30)

        self.assertIn('/mock/path/app.log', findings['old_logs'])
        self.assertNotIn('/mock/path/server.log', findings['old_logs'])
        self.assertNotIn('/mock/path/debug.txt', findings['old_logs'])
        self.assertEqual(len(findings['temp_files']), 0)
        self.assertEqual(len(findings['empty_dirs']), 0)

    @patch('os.path.exists', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    def test_scan_empty_dirs(self, mock_listdir, mock_getmtime, mock_walk, mock_exists):
        # Mock rationale: Simulate a directory structure with an empty subdirectory.
        mock_walk.return_value = [
            ('/mock/path', ['empty_dir', 'full_dir'], []), # Root dir
            ('/mock/path/full_dir', [], ['file.txt']), # Full dir
            ('/mock/path/empty_dir', [], []) # Empty dir
        ]
        # Mock rationale: Control the return value of os.listdir for specific directories.
        def listdir_side_effect(path):
            if path == '/mock/path/empty_dir':
                return [] # Empty
            elif path == '/mock/path/full_dir':
                return ['file.txt'] # Not empty
            return ['empty_dir', 'full_dir'] # Root dir

        mock_listdir.side_effect = listdir_side_effect
        mock_getmtime.return_value = self.mock_time

        findings = self.collector.scan(['/mock/path'])

        self.assertIn('/mock/path/empty_dir', findings['empty_dirs'])
        self.assertNotIn('/mock/path/full_dir', findings['empty_dirs'])
        self.assertNotIn('/mock/path', findings['empty_dirs']) # Root is not empty
        self.assertEqual(len(findings['temp_files']), 0)
        self.assertEqual(len(findings['old_logs']), 0)

    @patch('os.path.exists', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('builtins.print') # Mock rationale: Suppress print output during tests
    def test_clean_dry_run(self, mock_print, mock_rmdir, mock_remove, mock_listdir, mock_getmtime, mock_walk, mock_exists):
        findings = {
            'temp_files': ['/mock/path/temp.tmp'],
            'old_logs': ['/mock/path/old.log'],
            'empty_dirs': ['/mock/path/empty_dir']
        }

        deleted_files, deleted_dirs = self.collector.clean(findings, dry_run=True)

        mock_remove.assert_not_called()
        mock_rmdir.assert_not_called()
        self.assertEqual(deleted_files, 0)
        self.assertEqual(deleted_dirs, 0)
        mock_print.assert_any_call('--- DRY RUN MODE ---')
        mock_print.assert_any_call('No changes were made. Run without --dry-run to perform actual deletion.')

    @patch('os.path.exists', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('builtins.print') # Mock rationale: Suppress print output during tests
    def test_clean_actual_deletion(self, mock_print, mock_rmdir, mock_remove, mock_listdir, mock_getmtime, mock_walk, mock_exists):
        findings = {
            'temp_files': ['/mock/path/temp.tmp'],
            'old_logs': ['/mock/path/old.log'],
            'empty_dirs': ['/mock/path/empty_dir']
        }

        deleted_files, deleted_dirs = self.collector.clean(findings, dry_run=False)

        mock_remove.assert_any_call('/mock/path/temp.tmp')
        mock_remove.assert_any_call('/mock/path/old.log')
        mock_rmdir.assert_any_call('/mock/path/empty_dir')
        self.assertEqual(deleted_files, 2)
        self.assertEqual(deleted_dirs, 1)
        mock_print.assert_any_call('--- CLEANING MODE ---')
        mock_print.assert_any_call('Cleanup complete. Deleted 2 files and 1 directories.')

    @patch('os.path.exists', return_value=False)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('sys.stderr', new_callable=MagicMock) # Mock rationale: Capture stderr output
    def test_scan_non_existent_path(self, mock_stderr, mock_listdir, mock_getmtime, mock_walk, mock_exists):
        mock_walk.return_value = []
        findings = self.collector.scan(['/non/existent/path'])
        self.assertEqual(len(findings['temp_files']), 0)
        self.assertEqual(len(findings['old_logs']), 0)
        self.assertEqual(len(findings['empty_dirs']), 0)
        mock_stderr.write.assert_any_call('Warning: Path not found - /non/existent/path\n')

    @patch('os.path.exists', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime', side_effect=OSError) # Mock rationale: Simulate permission error
    @patch('os.listdir')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_scan_getmtime_error(self, mock_stderr, mock_listdir, mock_getmtime, mock_walk, mock_exists):
        mock_walk.return_value = [
            ('/mock/path', [], ['error.log'])
        ]
        mock_listdir.return_value = ['error.log']

        findings = self.collector.scan(['/mock/path'], age_days=1)
        self.assertEqual(len(findings['old_logs']), 0) # Should not be added if mtime fails
        # No error message printed for getmtime, just not added to findings

    @patch('os.path.exists', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir', side_effect=OSError) # Mock rationale: Simulate permission error for listdir
    @patch('sys.stderr', new_callable=MagicMock)
    def test_scan_listdir_error(self, mock_stderr, mock_listdir, mock_getmtime, mock_walk, mock_exists):
        mock_walk.return_value = [
            ('/mock/path', ['unreadable_dir'], []), # Root dir
            ('/mock/path/unreadable_dir', [], []) # Unreadable dir
        ]
        mock_getmtime.return_value = self.mock_time

        findings = self.collector.scan(['/mock/path'])
        self.assertEqual(len(findings['empty_dirs']), 0) # Should not be added if listdir fails

    @patch('os.path.exists', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('os.remove', side_effect=OSError('Permission denied')) # Mock rationale: Simulate deletion error
    @patch('os.rmdir', side_effect=OSError('Directory not empty')) # Mock rationale: Simulate deletion error
    @patch('builtins.print')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_clean_deletion_error(self, mock_stderr, mock_print, mock_rmdir, mock_remove, mock_listdir, mock_getmtime, mock_walk, mock_exists):
        findings = {
            'temp_files': ['/mock/path/temp.tmp'],
            'empty_dirs': ['/mock/path/empty_dir']
        }

        deleted_files, deleted_dirs = self.collector.clean(findings, dry_run=False)

        mock_remove.assert_any_call('/mock/path/temp.tmp')
        mock_rmdir.assert_any_call('/mock/path/empty_dir')
        self.assertEqual(deleted_files, 0) # Not deleted due to error
        self.assertEqual(deleted_dirs, 0) # Not deleted due to error
        mock_stderr.write.assert_any_call("    [ERROR] Could not delete /mock/path/temp.tmp: Permission denied\n")
        mock_stderr.write.assert_any_call("    [ERROR] Could not delete /mock/path/empty_dir: Directory not empty\n")

    @patch('os.path.exists', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('builtins.print')
    def test_clean_no_findings(self, mock_print, mock_listdir, mock_getmtime, mock_walk, mock_exists):
        findings = {
            'temp_files': [],
            'old_logs': [],
            'empty_dirs': []
        }
        deleted_files, deleted_dirs = self.collector.clean(findings, dry_run=True)
        self.assertEqual(deleted_files, 0)
        self.assertEqual(deleted_dirs, 0)
        mock_print.assert_any_call('No cosmic dust bunnies found. Your system is pristine!')

if __name__ == '__main__':
    unittest.main()
