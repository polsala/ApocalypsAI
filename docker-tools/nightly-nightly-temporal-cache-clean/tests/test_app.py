import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from datetime import datetime, timedelta
import time

# Mock rationale: os.walk, os.path.isdir, os.path.isfile, os.path.getmtime, os.path.getsize, os.remove
# These functions interact with the actual file system, which makes tests non-deterministic
# and dependent on the test environment. Mocking them allows us to simulate various file
# system states and behaviors (e.g., files existing, not existing, different modification times)
# without touching the real disk. This ensures tests are fast, isolated, and repeatable.

# Add the src directory to the Python path to import app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import clean_temporal_cache, get_env_var

class TestTemporalCacheCleaner(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.remove')
    def test_dry_run_identifies_old_files(self, mock_remove, mock_getsize, mock_getmtime, mock_isfile, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        # Simulate a directory with one old file and one new file
        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.txt', 'new_file.txt'])
        ]

        # Mock modification times
        now = datetime.now()
        old_time = (now - timedelta(days=40)).timestamp() # Older than 30 days
        new_time = (now - timedelta(days=10)).timestamp() # Newer than 30 days

        def mock_getmtime_side_effect(path):
            if 'old_file.txt' in path:
                return old_time
            elif 'new_file.txt' in path:
                return new_time
            return now.timestamp() # Default for other paths

        mock_getmtime.side_effect = mock_getmtime_side_effect
        mock_getsize.return_value = 100 # Arbitrary size
        mock_isfile.return_value = True # All paths are files

        # Capture print output
        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            clean_temporal_cache('/test_dir', 30, True) # Dry run

            # Assertions
            mock_remove.assert_not_called() # No deletion in dry run
            # Check for specific output lines
            output_calls = [call_arg.args[0] for call_arg in mock_stdout.write.call_args_list]
            self.assertTrue(any('Found ancient artifact: /test_dir/old_file.txt' in s for s in output_calls))
            self.assertTrue(any('(Dry run: Would have swept old_file.txt)' in s for s in output_calls))
            self.assertTrue(any('Identified 1 artifacts totaling 100 bytes for sweeping.' in s for s in output_calls))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.remove')
    def test_live_run_deletes_old_files(self, mock_remove, mock_getsize, mock_getmtime, mock_isfile, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.txt', 'new_file.txt'])
        ]

        now = datetime.now()
        old_time = (now - timedelta(days=40)).timestamp()
        new_time = (now - timedelta(days=10)).timestamp()

        def mock_getmtime_side_effect(path):
            if 'old_file.txt' in path:
                return old_time
            elif 'new_file.txt' in path:
                return new_time
            return now.timestamp()

        mock_getmtime.side_effect = mock_getmtime_side_effect
        mock_getsize.return_value = 100
        mock_isfile.return_value = True

        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            clean_temporal_cache('/test_dir', 30, False) # Live run

            # Assertions
            mock_remove.assert_called_once_with('/test_dir/old_file.txt')
            output_calls = [call_arg.args[0] for call_arg in mock_stdout.write.call_args_list]
            self.assertTrue(any('Found ancient artifact: /test_dir/old_file.txt' in s for s in output_calls))
            self.assertTrue(any('*Poof!* old_file.txt vanished into the temporal void.' in s for s in output_calls))
            self.assertTrue(any('Swept away 1 artifacts totaling 100 bytes.' in s for s in output_calls))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.remove')
    def test_multiple_target_directories(self, mock_remove, mock_getsize, mock_getmtime, mock_isfile, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        mock_walk.side_effect = [
            [('/dir1', [], ['file1_old.txt'])], # First call for /dir1
            [('/dir2', [], ['file2_new.txt', 'file2_old.txt'])] # Second call for /dir2
        ]

        now = datetime.now()
        old_time = (now - timedelta(days=40)).timestamp()
        new_time = (now - timedelta(days=10)).timestamp()

        def mock_getmtime_side_effect(path):
            if 'file1_old.txt' in path or 'file2_old.txt' in path:
                return old_time
            elif 'file2_new.txt' in path:
                return new_time
            return now.timestamp()

        mock_getmtime.side_effect = mock_getmtime_side_effect
        mock_getsize.return_value = 50
        mock_isfile.return_value = True

        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            clean_temporal_cache('/dir1,/dir2', 30, False)

            self.assertEqual(mock_remove.call_count, 2)
            mock_remove.assert_any_call('/dir1/file1_old.txt')
            mock_remove.assert_any_call('/dir2/file2_old.txt')
            output_calls = [call_arg.args[0] for call_arg in mock_stdout.write.call_args_list]
            self.assertTrue(any('Swept away 2 artifacts totaling 100 bytes.' in s for s in output_calls))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.remove')
    def test_non_existent_directory_is_skipped(self, mock_remove, mock_getsize, mock_getmtime, mock_isfile, mock_walk, mock_isdir):
        mock_isdir.side_effect = lambda x: x == '/existing_dir' # Only one dir exists
        mock_walk.return_value = [
            ('/existing_dir', [], ['old_file.txt'])
        ]

        now = datetime.now()
        old_time = (now - timedelta(days=40)).timestamp()
        mock_getmtime.return_value = old_time
        mock_getsize.return_value = 100
        mock_isfile.return_value = True

        with patch('sys.stdout', new=MagicMock()) as mock_stdout, \
             patch('sys.stderr', new=MagicMock()) as mock_stderr:
            clean_temporal_cache('/non_existent_dir,/existing_dir', 30, False)

            mock_remove.assert_called_once_with('/existing_dir/old_file.txt')
            stderr_calls = [call_arg.args[0] for call_arg in mock_stderr.write.call_args_list]
            self.assertTrue(any("Warning: Target directory '/non_existent_dir' does not exist or is not a directory. Skipping." in s for s in stderr_calls))
            stdout_calls = [call_arg.args[0] for call_arg in mock_stdout.write.call_args_list]
            self.assertTrue(any('Swept away 1 artifacts totaling 100 bytes.' in s for s in stdout_calls))

    def test_get_env_var_defaults(self):
        with patch.dict(os.environ, {}, clear=True): # Ensure no env vars are set
            self.assertEqual(get_env_var("TEST_VAR", "default_val"), "default_val")
            self.assertEqual(get_env_var("TEST_INT", 123, int), 123)
            self.assertEqual(get_env_var("TEST_BOOL", True, lambda x: x.lower() == 'true'), True)
            self.assertEqual(get_env_var("TEST_BOOL", False, lambda x: x.lower() == 'true'), False)

    def test_get_env_var_from_env(self):
        with patch.dict(os.environ, {"TEST_VAR": "env_val", "TEST_INT": "456", "TEST_BOOL": "TRUE"}):
            self.assertEqual(get_env_var("TEST_VAR", "default_val"), "env_val")
            self.assertEqual(get_env_var("TEST_INT", 123, int), 456)
            self.assertEqual(get_env_var("TEST_BOOL", False, lambda x: x.lower() == 'true'), True)

    def test_get_env_var_invalid_type(self):
        with patch.dict(os.environ, {"TEST_INT": "not_an_int"}), \
             patch('sys.stderr', new=MagicMock()) as mock_stderr:
            self.assertEqual(get_env_var("TEST_INT", 123, int), 123)
            stderr_calls = [call_arg.args[0] for call_arg in mock_stderr.write.call_args_list]
            self.assertTrue(any("Warning: Environment variable TEST_INT has invalid format ('not_an_int'). Using default: 123" in s for s in stderr_calls))

    @patch('sys.stdout', new=MagicMock())
    @patch('sys.stderr', new=MagicMock())
    def test_no_target_dirs(self):
        clean_temporal_cache('', 30, True)
        sys.stderr.write.assert_called_with("No target directories specified. Nothing to sweep!\n")

if __name__ == '__main__':
    unittest.main()
