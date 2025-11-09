import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Mock rationale: We need to simulate file system operations (listing directories, getting file stats, deleting files)
# without actually touching the real file system. This ensures tests are deterministic, fast, and safe.

# Define a consistent current time for mocks to ensure age calculations are stable.
# This time is 2023-10-27 10:00:00 UTC
MOCK_CURRENT_TIME = 1698391200.0

# Helper to create mock stat objects
def create_mock_stat(mtime, size):
    mock_stat = MagicMock()
    mock_stat.st_mtime = mtime
    mock_stat.st_size = size
    return mock_stat

class TestCosmicDustCollector(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('os.remove')
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('builtins.print') # Mock rationale: Mock print to capture output and prevent console spam during tests.
    def test_dry_run_identifies_old_and_large_files(self, mock_print, mock_time, mock_remove, mock_stat, mock_walk, mock_isdir):
        from src.collector import collect_dust

        mock_isdir.return_value = True # Mock rationale: Assume the base path exists for testing purposes.

        # Mock rationale: Simulate a directory structure with files of varying ages and sizes.
        # File 1: Old and large (should be identified)
        # File 2: Old but small (should NOT be identified by size criteria)
        # File 3: New and large (should NOT be identified by age criteria)
        # File 4: New and small (should NOT be identified)
        mock_walk.return_value = [
            ('/mock/path', [], ['file1.log', 'file2.txt', 'file3.data', 'file4.tmp'])
        ]

        # Mock rationale: Provide specific stat data for each file to control age and size.
        # file1.log: mtime = 60 days ago, size = 20MB
        # file2.txt: mtime = 60 days ago, size = 5MB
        # file3.data: mtime = 10 days ago, size = 20MB
        # file4.tmp: mtime = 10 days ago, size = 5MB
        mock_stat.side_effect = [
            create_mock_stat(MOCK_CURRENT_TIME - (60 * 24 * 60 * 60), 20 * 1024 * 1024), # file1.log (old, large)
            create_mock_stat(MOCK_CURRENT_TIME - (60 * 24 * 60 * 60), 5 * 1024 * 1024),  # file2.txt (old, small)
            create_mock_stat(MOCK_CURRENT_TIME - (10 * 24 * 60 * 60), 20 * 1024 * 1024), # file3.data (new, large)
            create_mock_stat(MOCK_CURRENT_TIME - (10 * 24 * 60 * 60), 5 * 1024 * 1024)   # file4.tmp (new, small)
        ]

        # Call the function with default criteria (min_age_days=30, min_size_mb=10, dry_run=True)
        result = collect_dust('/mock/path', dry_run=True)

        self.assertEqual(len(result), 1)
        self.assertIn('/mock/path/file1.log', result)
        mock_remove.assert_not_called() # Mock rationale: In dry run mode, os.remove should never be called.
        mock_print.assert_any_call(unittest.mock.ANY, 'Identified 1 files.') # Mock rationale: Verify the summary output for identified files.

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('os.remove')
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('builtins.print')
    def test_actual_cleanup_deletes_files(self, mock_print, mock_time, mock_remove, mock_stat, mock_walk, mock_isdir):
        from src.collector import collect_dust

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['deleteme.log', 'keepme.txt'])
        ]

        mock_stat.side_effect = [
            create_mock_stat(MOCK_CURRENT_TIME - (40 * 24 * 60 * 60), 15 * 1024 * 1024), # deleteme.log (old, large)
            create_mock_stat(MOCK_CURRENT_TIME - (10 * 24 * 60 * 60), 5 * 1024 * 1024)   # keepme.txt (new, small)
        ]

        result = collect_dust('/mock/path', min_age_days=30, min_size_mb=10, dry_run=False)

        self.assertEqual(len(result), 1)
        self.assertIn('/mock/path/deleteme.log', result)
        mock_remove.assert_called_once_with('/mock/path/deleteme.log') # Mock rationale: Verify os.remove is called exactly once for the target file when not in dry run.
        mock_print.assert_any_call(unittest.mock.ANY, 'Cleaned 1 files.') # Mock rationale: Verify the summary output for cleaned files.

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('os.remove')
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('builtins.print')
    def test_filters_by_extensions(self, mock_print, mock_time, mock_remove, mock_stat, mock_walk, mock_isdir):
        from src.collector import collect_dust

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['file.log', 'file.tmp', 'file.bak', 'file.txt'])
        ]

        # Mock rationale: All files are old and large enough to be considered by age/size criteria.
        # We are specifically testing the extension filtering here.
        mock_stat.side_effect = [
            create_mock_stat(MOCK_CURRENT_TIME - (60 * 24 * 60 * 60), 20 * 1024 * 1024), # file.log
            create_mock_stat(MOCK_CURRENT_TIME - (60 * 24 * 60 * 60), 20 * 1024 * 1024), # file.tmp
            create_mock_stat(MOCK_CURRENT_TIME - (60 * 24 * 60 * 60), 20 * 1024 * 1024), # file.bak
            create_mock_stat(MOCK_CURRENT_TIME - (60 * 24 * 60 * 60), 20 * 1024 * 1024)  # file.txt
        ]

        result = collect_dust('/mock/path', file_extensions=['log', 'bak'], dry_run=True)

        self.assertEqual(len(result), 2)
        self.assertIn('/mock/path/file.log', result)
        self.assertIn('/mock/path/file.bak', result)
        self.assertNotIn('/mock/path/file.tmp', result)
        self.assertNotIn('/mock/path/file.txt', result)
        mock_remove.assert_not_called()

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    def test_invalid_path_handling(self, mock_print, mock_isdir):
        from src.collector import collect_dust

        result = collect_dust('/nonexistent/path', dry_run=True)

        self.assertEqual(result, [])
        mock_print.assert_any_call("Error: Path '/nonexistent/path' is not a valid directory.") # Mock rationale: Verify the specific error message for an invalid path.

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('os.remove')
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('builtins.print')
    def test_os_error_handling(self, mock_print, mock_time, mock_remove, mock_stat, mock_walk, mock_isdir):
        from src.collector import collect_dust

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['unreadable.log'])
        ]

        # Mock rationale: Simulate an OSError (e.g., permission denied) when trying to get file stats.
        mock_stat.side_effect = OSError("Permission denied")

        result = collect_dust('/mock/path', dry_run=True)

        self.assertEqual(result, []) # No files should be identified/cleaned if stat fails.
        mock_print.assert_any_call(unittest.mock.ANY, 'Warning: Could not access /mock/path/unreadable.log - Permission denied') # Mock rationale: Verify the warning message for OS errors.
        mock_remove.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('os.remove')
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('builtins.print')
    def test_no_files_match_criteria(self, mock_print, mock_time, mock_remove, mock_stat, mock_walk, mock_isdir):
        from src.collector import collect_dust

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['recent_small.txt'])
        ]

        # Mock rationale: Provide stat data for a file that is both recent and small, so it shouldn't match criteria.
        mock_stat.return_value = create_mock_stat(MOCK_CURRENT_TIME - (5 * 24 * 60 * 60), 1 * 1024 * 1024) # Recent and small

        result = collect_dust('/mock/path', min_age_days=30, min_size_mb=10, dry_run=True)

        self.assertEqual(result, [])
        mock_print.assert_any_call(unittest.mock.ANY, 'Identified 0 files.') # Mock rationale: Verify that no files are identified.
        mock_remove.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('os.remove')
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('builtins.print')
    def test_case_insensitive_extensions(self, mock_print, mock_time, mock_remove, mock_stat, mock_walk, mock_isdir):
        from src.collector import collect_dust

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['file.LOG', 'file.Tmp', 'file.TXT'])
        ]

        # Mock rationale: All files are old and large enough to be considered by age/size.
        # We are testing case-insensitive extension matching.
        mock_stat.side_effect = [
            create_mock_stat(MOCK_CURRENT_TIME - (60 * 24 * 60 * 60), 20 * 1024 * 1024), # file.LOG
            create_mock_stat(MOCK_CURRENT_TIME - (60 * 24 * 60 * 60), 20 * 1024 * 1024), # file.Tmp
            create_mock_stat(MOCK_CURRENT_TIME - (60 * 24 * 60 * 60), 20 * 1024 * 1024)  # file.TXT
        ]

        result = collect_dust('/mock/path', file_extensions=['log', 'tmp'], dry_run=True)

        self.assertEqual(len(result), 2)
        self.assertIn('/mock/path/file.LOG', result)
        self.assertIn('/mock/path/file.Tmp', result)
        self.assertNotIn('/mock/path/file.TXT', result)
        mock_remove.assert_not_called()

if __name__ == '__main__':
    unittest.main()
