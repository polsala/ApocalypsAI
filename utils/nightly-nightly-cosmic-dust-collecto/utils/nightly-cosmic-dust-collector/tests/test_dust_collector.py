import unittest
from unittest.mock import patch, MagicMock
import os
import time
import shutil
import sys
from io import StringIO

# Mock current time for deterministic age calculation
MOCK_CURRENT_TIME = time.time()

# Mock rationale: We need to control the file system state and time for deterministic tests.
# os.walk: Simulates directory structure and files.
# os.path.getmtime: Simulates file modification times.
# os.path.isdir: Simulates directory existence.
# os.remove: Verifies deletion calls without actual file system changes.
# shutil.move: Verifies archiving calls without actual file system changes.
# os.makedirs: Verifies archive directory creation.
# os.path.exists: Simulates existence checks for archive path uniqueness.
# sys.stdout: Captures print output for verification.

class TestDustCollector(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_dust_files(self, mock_stdout, mock_time, mock_getmtime, mock_walk, mock_isdir):
        from src.dust_collector import collect_dust

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['old_log.log', 'new_file.txt', 'temp_data.tmp'])
        ]
        # old_log.log: 40 days old (dust)
        # new_file.txt: 10 days old (not dust, wrong pattern)
        # temp_data.tmp: 40 days old (dust)
        mock_getmtime.side_effect = lambda f: {
            '/test_dir/old_log.log': MOCK_CURRENT_TIME - (40 * 24 * 60 * 60),
            '/test_dir/new_file.txt': MOCK_CURRENT_TIME - (10 * 24 * 60 * 60),
            '/test_dir/temp_data.tmp': MOCK_CURRENT_TIME - (40 * 24 * 60 * 60),
        }.get(f, MOCK_CURRENT_TIME)

        collect_dust(path='/test_dir', age_days=30, patterns=['*.log', '*.tmp'], action='list')

        output = mock_stdout.getvalue()
        self.assertIn("Found 2 cosmic dust files", output)
        self.assertIn("  - /test_dir/old_log.log", output)
        self.assertIn("  - /test_dir/temp_data.tmp", output)
        self.assertNotIn("new_file.txt", output)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.remove')
    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_dust_files(self, mock_stdout, mock_remove, mock_time, mock_getmtime, mock_walk, mock_isdir):
        from src.dust_collector import collect_dust

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['old_log.log', 'another_old.tmp'])
        ]
        mock_getmtime.side_effect = lambda f: {
            '/test_dir/old_log.log': MOCK_CURRENT_TIME - (35 * 24 * 60 * 60),
            '/test_dir/another_old.tmp': MOCK_CURRENT_TIME - (45 * 24 * 60 * 60),
        }.get(f, MOCK_CURRENT_TIME)

        collect_dust(path='/test_dir', age_days=30, patterns=['*.log', '*.tmp'], action='delete')

        output = mock_stdout.getvalue()
        self.assertIn("Found 2 cosmic dust files", output)
        self.assertIn("Initiating cosmic dust deletion...", output)
        self.assertIn("  Deleted: /test_dir/old_log.log", output)
        self.assertIn("  Deleted: /test_dir/another_old.tmp", output)
        mock_remove.assert_any_call('/test_dir/old_log.log')
        mock_remove.assert_any_call('/test_dir/another_old.tmp')
        self.assertEqual(mock_remove.call_count, 2)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('os.path.exists', side_effect=[False, False]) # For archive path uniqueness, no conflict initially
    @patch('sys.stdout', new_callable=StringIO)
    def test_archive_dust_files(self, mock_stdout, mock_exists, mock_makedirs, mock_move, mock_time, mock_getmtime, mock_walk, mock_isdir):
        from src.dust_collector import collect_dust

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['old_log.log', 'temp_file.tmp'])
        ]
        mock_getmtime.side_effect = lambda f: {
            '/test_dir/old_log.log': MOCK_CURRENT_TIME - (50 * 24 * 60 * 60),
            '/test_dir/temp_file.tmp': MOCK_CURRENT_TIME - (60 * 24 * 60 * 60),
        }.get(f, MOCK_CURRENT_TIME)

        collect_dust(path='/test_dir', age_days=40, patterns=['*.log', '*.tmp'], action='archive')

        output = mock_stdout.getvalue()
        self.assertIn("Found 2 cosmic dust files", output)
        self.assertIn("Initiating cosmic dust archiving...", output)
        self.assertIn("  Archived: /test_dir/old_log.log -> /test_dir/.dust_archive/old_log.log", output)
        self.assertIn("  Archived: /test_dir/temp_file.tmp -> /test_dir/.dust_archive/temp_file.tmp", output)
        mock_makedirs.assert_called_once_with('/test_dir/.dust_archive', exist_ok=True)
        mock_move.assert_any_call('/test_dir/old_log.log', '/test_dir/.dust_archive/old_log.log')
        mock_move.assert_any_call('/test_dir/temp_file.tmp', '/test_dir/.dust_archive/temp_file.tmp')
        self.assertEqual(mock_move.call_count, 2)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/test_dir', [], ['recent.log', 'recent.tmp'])])
    @patch('os.path.getmtime', return_value=MOCK_CURRENT_TIME - (10 * 24 * 60 * 60)) # All files 10 days old
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('sys.stdout', new_callable=StringIO)
    def test_no_dust_found(self, mock_stdout, *args):
        from src.dust_collector import collect_dust

        collect_dust(path='/test_dir', age_days=30, patterns=['*.log', '*.tmp'], action='list')

        output = mock_stdout.getvalue()
        self.assertIn("No cosmic dust found in '/test_dir' older than 30 days", output)

    @patch('os.path.isdir', return_value=False)
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_path(self, mock_stdout, mock_isdir):
        from src.dust_collector import collect_dust

        collect_dust(path='/non_existent', action='list')

        output = mock_stdout.getvalue()
        self.assertIn("Error: Directory not found: /non_existent", output)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/test_dir', [], ['file.log'])])
    @patch('os.path.getmtime', return_value=MOCK_CURRENT_TIME - (40 * 24 * 60 * 60))
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('sys.stdout', new_callable=StringIO)
    def test_unknown_action(self, mock_stdout, *args):
        from src.dust_collector import collect_dust

        collect_dust(path='/test_dir', action='unknown_action')

        output = mock_stdout.getvalue()
        self.assertIn("Error: Unknown action 'unknown_action'", output)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('os.path.exists', side_effect=[True, False]) # Simulate a conflict for old_log.log: first check returns True, second False
    @patch('sys.stdout', new_callable=StringIO)
    def test_archive_with_name_conflict(self, mock_stdout, mock_exists, mock_makedirs, mock_move, mock_time, mock_getmtime, mock_walk, mock_isdir):
        from src.dust_collector import collect_dust

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['old_log.log'])
        ]
        mock_getmtime.side_effect = lambda f: {
            '/test_dir/old_log.log': MOCK_CURRENT_TIME - (50 * 24 * 60 * 60),
        }.get(f, MOCK_CURRENT_TIME)

        collect_dust(path='/test_dir', age_days=40, patterns=['*.log'], action='archive')

        output = mock_stdout.getvalue()
        self.assertIn("Found 1 cosmic dust files", output)
        self.assertIn("  Archived: /test_dir/old_log.log -> /test_dir/.dust_archive/old_log_1.log", output)
        mock_move.assert_called_once_with('/test_dir/old_log.log', '/test_dir/.dust_archive/old_log_1.log')


if __name__ == '__main__':
    unittest.main()
