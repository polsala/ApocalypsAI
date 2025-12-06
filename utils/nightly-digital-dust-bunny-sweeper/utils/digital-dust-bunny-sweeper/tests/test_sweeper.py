import unittest
from unittest.mock import patch, MagicMock
import os
import datetime
import sys

# Adjust sys.path to allow importing sweeper from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import sweeper
sys.path.pop(0)

class TestDigitalDustBunnySweeper(unittest.TestCase):

    @patch('os.path.getmtime')
    def test_get_file_age_in_days(self, mock_getmtime):
        # Mock rationale: os.path.getmtime returns a timestamp, which is non-deterministic.
        # We need to control the file's modification time to test age calculation reliably.
        
        # Simulate a file modified 10 days ago
        ten_days_ago = (datetime.datetime.now() - datetime.timedelta(days=10)).timestamp()
        mock_getmtime.return_value = ten_days_ago
        self.assertEqual(sweeper.get_file_age_in_days('/fake/path/file.txt'), 10)

        # Simulate a file modified 0 days ago (today)
        today = datetime.datetime.now().timestamp()
        mock_getmtime.return_value = today
        self.assertEqual(sweeper.get_file_age_in_days('/fake/path/file.txt'), 0)

        # Simulate OSError (file not found/permissions)
        mock_getmtime.side_effect = OSError
        self.assertEqual(sweeper.get_file_age_in_days('/nonexistent/file.txt'), -1)

    @patch('os.listdir')
    def test_is_directory_empty(self, mock_listdir):
        # Mock rationale: os.listdir interacts with the actual file system, making tests non-deterministic.
        # We need to simulate directory contents to test the 'empty' logic.

        # Simulate an empty directory
        mock_listdir.return_value = []
        self.assertTrue(sweeper.is_directory_empty('/fake/empty/dir'))

        # Simulate a non-empty directory
        mock_listdir.return_value = ['file.txt', 'subdir']
        self.assertFalse(sweeper.is_directory_empty('/fake/nonempty/dir'))

        # Simulate OSError (directory not found/permissions)
        mock_listdir.side_effect = OSError
        self.assertFalse(sweeper.is_directory_empty('/nonexistent/dir'))

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir') # For is_directory_empty
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('builtins.print') # To capture output
    def test_find_dust_bunnies_dry_run(self,
                                       mock_print,
                                       mock_rmdir,
                                       mock_remove,
                                       mock_listdir,
                                       mock_getmtime,
                                       mock_walk,
                                       mock_isdir):
        # Mock rationale: All os.* functions interact with the file system. Mocking them ensures
        # the test is deterministic, offline, and doesn't modify the actual file system.
        # builtins.print is mocked to capture output for assertion without affecting console.

        root_path = '/test_root'
        
        # Simulate file system structure:
        # /test_root/
        #   subdir1/
        #     old_log.log (40 days old)
        #     recent_file.txt (5 days old)
        #   subdir2/ (empty)
        #   another_file.tmp (60 days old)
        #   empty_dir_at_root/ (empty)

        # Mock os.walk to simulate directory structure
        mock_walk.return_value = [
            (root_path, ['subdir1', 'subdir2', 'empty_dir_at_root'], ['another_file.tmp']),
            (os.path.join(root_path, 'subdir1'), [], ['old_log.log', 'recent_file.txt']),
            (os.path.join(root_path, 'subdir2'), [], []),
            (os.path.join(root_path, 'empty_dir_at_root'), [], []),
        ]

        # Mock os.path.getmtime for specific files
        now = datetime.datetime.now()
        mock_getmtime.side_effect = lambda p: {
            os.path.join(root_path, 'subdir1', 'old_log.log'): (now - datetime.timedelta(days=40)).timestamp(),
            os.path.join(root_path, 'subdir1', 'recent_file.txt'): (now - datetime.timedelta(days=5)).timestamp(),
            os.path.join(root_path, 'another_file.tmp'): (now - datetime.timedelta(days=60)).timestamp(),
        }.get(p, now.timestamp()) # Default to now for unexpected paths

        # Mock os.listdir for is_directory_empty checks
        mock_listdir.side_effect = lambda p: {
            os.path.join(root_path, 'subdir1'): ['old_log.log', 'recent_file.txt'],
            os.path.join(root_path, 'subdir2'): [],
            os.path.join(root_path, 'empty_dir_at_root'): [],
            root_path: ['subdir1', 'subdir2', 'empty_dir_at_root', 'another_file.tmp']
        }.get(p, [])

        # Run in dry-run mode
        sweeper.find_dust_bunnies(
            root_path=root_path,
            age_days=30,
            extensions=['.log', '.tmp'],
            delete_empty_dirs=True,
            dry_run=True,
            verbose=False
        )

        # Assertions for dry run
        mock_remove.assert_not_called() # Should not delete in dry run
        mock_rmdir.assert_not_called()   # Should not delete in dry run

        # Check if the correct files and directories were identified and printed
        output_calls = [call.args[0] for call in mock_print.call_args_list if call.args and isinstance(call.args[0], str)]

        self.assertIn(f"  [FILE] {os.path.join(root_path, 'subdir1', 'old_log.log')} (Age: 40 days)", output_calls)
        self.assertIn(f"  [FILE] {os.path.join(root_path, 'another_file.tmp')} (Age: 60 days)", output_calls)
        self.assertNotIn(f"  [FILE] {os.path.join(root_path, 'subdir1', 'recent_file.txt')} (Age: 5 days)", output_calls) # Too recent

        self.assertIn(f"  [DIR] {os.path.join(root_path, 'subdir2')}", output_calls)
        self.assertIn(f"  [DIR] {os.path.join(root_path, 'empty_dir_at_root')}", output_calls)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir') # For is_directory_empty
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('builtins.print') # To capture output
    def test_find_dust_bunnies_actual_run(self,
                                         mock_print,
                                         mock_rmdir,
                                         mock_remove,
                                         mock_listdir,
                                         mock_getmtime,
                                         mock_walk,
                                         mock_isdir):
        # Mock rationale: Same as dry-run, ensuring isolation and determinism.

        root_path = '/test_root'

        # Simulate file system structure (same as dry run for consistency)
        mock_walk.return_value = [
            (root_path, ['subdir1', 'subdir2', 'empty_dir_at_root'], ['another_file.tmp']),
            (os.path.join(root_path, 'subdir1'), [], ['old_log.log', 'recent_file.txt']),
            (os.path.join(root_path, 'subdir2'), [], []),
            (os.path.join(root_path, 'empty_dir_at_root'), [], []),
        ]

        now = datetime.datetime.now()
        mock_getmtime.side_effect = lambda p: {
            os.path.join(root_path, 'subdir1', 'old_log.log'): (now - datetime.timedelta(days=40)).timestamp(),
            os.path.join(root_path, 'subdir1', 'recent_file.txt'): (now - datetime.timedelta(days=5)).timestamp(),
            os.path.join(root_path, 'another_file.tmp'): (now - datetime.timedelta(days=60)).timestamp(),
        }.get(p, now.timestamp())

        mock_listdir.side_effect = lambda p: {
            os.path.join(root_path, 'subdir1'): ['old_log.log', 'recent_file.txt'],
            os.path.join(root_path, 'subdir2'): [],
            os.path.join(root_path, 'empty_dir_at_root'): [],
            root_path: ['subdir1', 'subdir2', 'empty_dir_at_root', 'another_file.tmp']
        }.get(p, [])

        # Run without dry-run mode
        sweeper.find_dust_bunnies(
            root_path=root_path,
            age_days=30,
            extensions=['.log', '.tmp'],
            delete_empty_dirs=True,
            dry_run=False,
            verbose=False
        )

        # Assertions for actual run
        # Check if os.remove was called for the old files
        mock_remove.assert_any_call(os.path.join(root_path, 'subdir1', 'old_log.log'))
        mock_remove.assert_any_call(os.path.join(root_path, 'another_file.tmp'))
        self.assertEqual(mock_remove.call_count, 2)

        # Check if os.rmdir was called for the empty directories
        mock_rmdir.assert_any_call(os.path.join(root_path, 'subdir2'))
        mock_rmdir.assert_any_call(os.path.join(root_path, 'empty_dir_at_root'))
        self.assertEqual(mock_rmdir.call_count, 2)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.listdir')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('builtins.print')
    def test_find_dust_bunnies_no_extensions(self,
                                             mock_print,
                                             mock_rmdir,
                                             mock_remove,
                                             mock_listdir,
                                             mock_getmtime,
                                             mock_walk,
                                             mock_isdir):
        # Mock rationale: Testing the behavior when no specific extensions are provided.

        root_path = '/test_root'
        mock_walk.return_value = [
            (root_path, [], ['old_file.txt', 'old_file.json', 'recent_file.py']),
        ]

        now = datetime.datetime.now()
        mock_getmtime.side_effect = lambda p: {
            os.path.join(root_path, 'old_file.txt'): (now - datetime.timedelta(days=40)).timestamp(),
            os.path.join(root_path, 'old_file.json'): (now - datetime.timedelta(days=40)).timestamp(),
            os.path.join(root_path, 'recent_file.py'): (now - datetime.timedelta(days=5)).timestamp(),
        }.get(p, now.timestamp())

        sweeper.find_dust_bunnies(
            root_path=root_path,
            age_days=30,
            extensions=[], # No extensions specified
            delete_empty_dirs=False,
            dry_run=True,
            verbose=False
        )

        output_calls = [call.args[0] for call in mock_print.call_args_list if call.args and isinstance(call.args[0], str)]
        self.assertIn(f"  [FILE] {os.path.join(root_path, 'old_file.txt')} (Age: 40 days)", output_calls)
        self.assertIn(f"  [FILE] {os.path.join(root_path, 'old_file.json')} (Age: 40 days)", output_calls)
        self.assertNotIn(f"  [FILE] {os.path.join(root_path, 'recent_file.py')} (Age: 5 days)", output_calls)

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_find_dust_bunnies_invalid_path(self, mock_stderr, mock_print, mock_isdir):
        # Mock rationale: Test error handling for invalid root path without actual file system interaction.
        sweeper.find_dust_bunnies(
            root_path='/nonexistent/path',
            age_days=30,
            extensions=[],
            delete_empty_dirs=False,
            dry_run=True,
            verbose=False
        )
        mock_print.assert_any_call("Error: Path '/nonexistent/path' is not a valid directory.", file=mock_stderr)

if __name__ == '__main__':
    unittest.main()
