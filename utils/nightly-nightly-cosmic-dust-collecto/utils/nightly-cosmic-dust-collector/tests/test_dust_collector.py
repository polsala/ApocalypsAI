import unittest
from unittest.mock import patch, MagicMock
import os
import re
from datetime import datetime, timedelta
import sys
from io import StringIO

# Add the src directory to the path to import dust_collector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dust_collector import collect_dust, main

class TestDustCollector(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.remove')
    def test_collect_dust_removes_old_files(self, mock_remove, mock_getsize, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale:
        # os.path.isdir: To simulate directory existence without actual filesystem checks.
        # os.walk: To simulate directory traversal and file discovery.
        # os.path.getmtime: To control file modification times for age-based filtering.
        # os.path.getsize: To provide file sizes for reporting.
        # os.remove: To prevent actual file deletion during tests.

        mock_isdir.return_value = True
        
        # Simulate files:
        # - old_log.log: matches pattern, is old
        # - new_log.log: matches pattern, is new
        # - other.txt: does not match pattern
        # - another_old.log: matches pattern, is old, in a subdirectory
        
        # Set current time for consistent age calculation
        now = datetime(2023, 10, 26, 10, 0, 0)
        
        # Mock os.walk to return specific files
        mock_walk.return_value = [
            ('/test_dir', [], ['old_log.log', 'new_log.log', 'other.txt']),
            ('/test_dir/subdir', [], ['another_old.log'])
        ]

        # Mock os.path.getmtime for each file
        def getmtime_side_effect(filepath):
            if 'old_log.log' in filepath:
                return (now - timedelta(days=10)).timestamp() # 10 days old, > 7 days threshold
            elif 'new_log.log' in filepath:
                return (now - timedelta(days=3)).timestamp()  # 3 days old, < 7 days threshold
            elif 'other.txt' in filepath:
                return (now - timedelta(days=10)).timestamp() # 10 days old, but wrong pattern
            elif 'another_old.log' in filepath:
                return (now - timedelta(days=15)).timestamp() # 15 days old, > 7 days threshold
            return now.timestamp() # Default for any unexpected files

        mock_getmtime.side_effect = getmtime_side_effect
        mock_getsize.return_value = 1024 * 1024 # 1 MB for all files

        directories_patterns_ages = [
            ('/test_dir', r'.*\\.log$', 7)
        ]

        # Patch datetime.now() to return a fixed time
        with patch('dust_collector.datetime') as mock_dt:
            mock_dt.now.return_value = now
            mock_dt.fromtimestamp = datetime.fromtimestamp # Keep original fromtimestamp
            mock_dt.timedelta = timedelta # Keep original timedelta
            collect_dust(directories_patterns_ages, dry_run=False)

        # Assertions
        self.assertEqual(mock_remove.call_count, 2) # old_log.log and another_old.log should be removed
        mock_remove.assert_any_call(os.path.join('/test_dir', 'old_log.log'))
        mock_remove.assert_any_call(os.path.join('/test_dir/subdir', 'another_old.log'))
        
        output = self.mock_stdout.getvalue()
        self.assertIn("REMOVED", output)
        self.assertIn("old_log.log", output)
        self.assertIn("another_old.log", output)
        self.assertNotIn("new_log.log", output)
        self.assertNotIn("other.txt", output)
        self.assertIn("Total files removed: 2", output)
        self.assertIn("Total space freed: 2.00 MB", output)


    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.remove')
    def test_collect_dust_dry_run_mode(self, mock_remove, mock_getsize, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Same as above, but specifically testing dry-run behavior.
        mock_isdir.return_value = True
        now = datetime(2023, 10, 26, 10, 0, 0)
        
        mock_walk.return_value = [
            ('/test_dir', [], ['old_log.log', 'new_log.log'])
        ]

        def getmtime_side_effect(filepath):
            if 'old_log.log' in filepath:
                return (now - timedelta(days=10)).timestamp()
            elif 'new_log.log' in filepath:
                return (now - timedelta(days=3)).timestamp()
            return now.timestamp()

        mock_getmtime.side_effect = getmtime_side_effect
        mock_getsize.return_value = 1024 * 1024 # 1 MB

        directories_patterns_ages = [
            ('/test_dir', r'.*\\.log$', 7)
        ]

        with patch('dust_collector.datetime') as mock_dt:
            mock_dt.now.return_value = now
            mock_dt.fromtimestamp = datetime.fromtimestamp
            mock_dt.timedelta = timedelta
            collect_dust(directories_patterns_ages, dry_run=True)

        mock_remove.assert_not_called() # No files should be removed in dry-run
        
        output = self.mock_stdout.getvalue()
        self.assertIn("(Dry Run) Would remove.", output)
        self.assertIn("old_log.log", output)
        self.assertNotIn("new_log.log", output)
        self.assertIn("Total files would be removed: 1", output)
        self.assertIn("Total space would be freed: 1.00 MB", output)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.remove')
    def test_collect_dust_no_matching_files(self, mock_remove, mock_getsize, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Testing scenario where no files match criteria.
        mock_isdir.return_value = True
        now = datetime(2023, 10, 26, 10, 0, 0)
        
        mock_walk.return_value = [
            ('/test_dir', [], ['new_log.log', 'other.txt'])
        ]

        def getmtime_side_effect(filepath):
            return (now - timedelta(days=3)).timestamp() # All files are new

        mock_getmtime.side_effect = getmtime_side_effect
        mock_getsize.return_value = 1024 * 1024

        directories_patterns_ages = [
            ('/test_dir', r'.*\\.log$', 7)
        ]

        with patch('dust_collector.datetime') as mock_dt:
            mock_dt.now.return_value = now
            mock_dt.fromtimestamp = datetime.fromtimestamp
            mock_dt.timedelta = timedelta
            collect_dust(directories_patterns_ages, dry_run=False)

        mock_remove.assert_not_called()
        
        output = self.mock_stdout.getvalue()
        self.assertNotIn("REMOVED", output)
        self.assertIn("Total files removed: 0", output)
        self.assertIn("Total space freed: 0.00 MB", output)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.remove')
    def test_collect_dust_non_existent_directory(self, mock_remove, mock_getsize, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Testing behavior when a specified directory does not exist.
        mock_isdir.return_value = False # Simulate directory not existing
        
        directories_patterns_ages = [
            ('/non_existent_dir', r'.*\\.log$', 7)
        ]

        collect_dust(directories_patterns_ages, dry_run=False)

        mock_walk.assert_not_called()
        mock_remove.assert_not_called()
        
        output = self.mock_stdout.getvalue()
        self.assertIn("Warning: Directory '/non_existent_dir' does not exist or is not a directory. Skipping.", output)
        self.assertIn("Total files removed: 0", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_collector.collect_dust')
    def test_main_function_calls_collect_dust(self, mock_collect_dust, mock_parse_args):
        # Mock rationale:
        # argparse.ArgumentParser.parse_args: To simulate command-line arguments without actually parsing sys.argv.
        # dust_collector.collect_dust: To ensure the main function correctly calls the core logic with parsed arguments.

        # Simulate command-line arguments
        mock_parse_args.return_value = MagicMock(
            dirs=['/test_dir_a', '/test_dir_b'],
            patterns=[r'.*\\.log$', r'.*\\.tmp$'],
            ages=[10, 5],
            dry_run=True,
            verbose=False
        )

        main()

        mock_collect_dust.assert_called_once_with(
            [('/test_dir_a', r'.*\\.log$', 10), ('/test_dir_b', r'.*\\.tmp$', 5)],
            True,
            False
        )
    
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_function_argument_validation(self, mock_exit, mock_stderr, mock_parse_args):
        # Mock rationale:
        # argparse.ArgumentParser.parse_args: To simulate argument parsing.
        # sys.stderr: To capture error messages printed by argparse.
        # sys.exit: To prevent the test from actually exiting, allowing assertion on exit code.

        # Test case 1: Missing --dir
        mock_parse_args.return_value = MagicMock(dirs=None, patterns=[r'.*\\.log$'], ages=[10])
        main()
        mock_exit.assert_called_with(2) # argparse exits with 2 for argument errors
        self.assertIn("error: at least one --dir, --pattern, and --age must be provided", mock_stderr.getvalue())
        mock_exit.reset_mock()
        mock_stderr.truncate(0)
        mock_stderr.seek(0)

        # Test case 2: Mismatched argument counts
        mock_parse_args.return_value = MagicMock(dirs=['/a', '/b'], patterns=[r'.*\\.log$'], ages=[10]) # 2 dirs, 1 pattern, 1 age
        main()
        mock_exit.assert_called_with(2)
        self.assertIn("error: The number of --dir, --pattern, and --age arguments must match.", mock_stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
