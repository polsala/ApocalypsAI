import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path to allow importing collector.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import collector

class TestCosmicDustBunnyCollector(unittest.TestCase):

    @patch('os.walk')
    def test_find_empty_dirs_basic(self, mock_os_walk):
        # Mock rationale: os.walk is a filesystem operation. We need to simulate
        # different directory structures without actually creating them on disk
        # to ensure deterministic and offline testing.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file.txt']),
            ('/root/dir1', [], []), # Empty dir
            ('/root/dir2', ['subdir'], []),
            ('/root/dir2/subdir', [], []), # Empty dir
        ]
        
        empty_dirs = collector.find_empty_dirs('/root')
        self.assertIn('/root/dir1', empty_dirs)
        self.assertIn('/root/dir2/subdir', empty_dirs)
        self.assertEqual(len(empty_dirs), 2)

    @patch('os.walk')
    def test_find_empty_dirs_nested_empty(self, mock_os_walk):
        # Mock rationale: Simulate nested empty directories to ensure the topdown=False
        # logic correctly identifies them. The order in os.walk.return_value matters
        # for topdown=False, simulating how it would be yielded.
        mock_os_walk.return_value = [
            ('/root/a/b/c', [], []), # Deeply nested empty
            ('/root/a/b', ['c'], []), # Not empty because it contains 'c' (even if 'c' is empty itself)
            ('/root/a', ['b'], []), # Not empty because it contains 'b'
            ('/root', ['a'], []), # Not empty because it contains 'a'
        ]
        empty_dirs = collector.find_empty_dirs('/root')
        self.assertIn('/root/a/b/c', empty_dirs)
        self.assertEqual(len(empty_dirs), 1)

    @patch('os.walk')
    def test_find_empty_dirs_no_empty(self, mock_os_walk):
        # Mock rationale: Verify behavior when no empty directories are present.
        mock_os_walk.return_value = [
            ('/root', ['dir1'], ['file.txt']),
            ('/root/dir1', [], ['another.txt']),
        ]
        empty_dirs = collector.find_empty_dirs('/root')
        self.assertEqual(len(empty_dirs), 0)

    @patch('os.rmdir')
    @patch('builtins.print')
    def test_remove_empty_dirs_success(self, mock_print, mock_os_rmdir):
        # Mock rationale: os.rmdir performs actual filesystem deletion. We mock it
        # to prevent real deletions during tests and to verify that it was called
        # with the correct arguments. builtins.print is mocked to capture output.
        dirs_to_remove = ['/root/empty1', '/root/empty2']
        removed_count = collector.remove_empty_dirs(dirs_to_remove)
        
        self.assertEqual(removed_count, 2)
        # Assert calls in the order they would be made (deeper first, then sorted by name if same depth)
        mock_os_rmdir.assert_any_call('/root/empty1')
        mock_os_rmdir.assert_any_call('/root/empty2')
        self.assertEqual(mock_os_rmdir.call_count, 2)
        mock_print.assert_any_call('Successfully removed: /root/empty1')
        mock_print.assert_any_call('Successfully removed: /root/empty2')

    @patch('os.rmdir')
    @patch('builtins.print')
    def test_remove_empty_dirs_failure(self, mock_print, mock_os_rmdir):
        # Mock rationale: Simulate an OSError during directory removal to ensure
        # the error handling path is correctly exercised and reported.
        mock_os_rmdir.side_effect = OSError("Permission denied")
        dirs_to_remove = ['/root/protected']
        removed_count = collector.remove_empty_dirs(dirs_to_remove)
        
        self.assertEqual(removed_count, 0)
        mock_os_rmdir.assert_called_once_with('/root/protected')
        mock_print.assert_any_call('Error removing /root/protected: Permission denied', file=sys.stderr)

    @patch('os.path.isdir', return_value=True)
    @patch('collector.find_empty_dirs', return_value=['/root/empty1', '/root/empty2'])
    @patch('collector.remove_empty_dirs', return_value=2)
    @patch('builtins.input', return_value='yes')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_remove_confirmed(self, mock_sys_exit, mock_print, mock_input, mock_remove_empty_dirs, mock_find_empty_dirs, mock_isdir):
        # Mock rationale: Test the main CLI logic. We mock all external interactions
        # (filesystem checks, core logic functions, user input, printing, and system exit)
        # to isolate the main function's control flow and argument parsing.
        with patch('sys.argv', ['collector.py', '--path', '/test', '--remove']):
            collector.main()
            mock_isdir.assert_called_once_with('/test')
            mock_find_empty_dirs.assert_called_once_with('/test')
            mock_input.assert_called_once()
            mock_remove_empty_dirs.assert_called_once_with(['/root/empty1', '/root/empty2'])
            mock_print.assert_any_call('Initiating cleanup...')
            mock_print.assert_any_call('Cleanup complete. Removed 2 directories.')
            mock_sys_exit.assert_called_once_with(0)

    @patch('os.path.isdir', return_value=True)
    @patch('collector.find_empty_dirs', return_value=['/root/empty1'])
    @patch('builtins.input', return_value='no')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_remove_aborted(self, mock_sys_exit, mock_print, mock_input, mock_find_empty_dirs, mock_isdir):
        # Mock rationale: Similar to the above, but testing the 'no' path for confirmation.
        with patch('sys.argv', ['collector.py', '--path', '/test', '--remove']):
            collector.main()
            mock_input.assert_called_once()
            mock_print.assert_any_call('Cleanup aborted.')
            mock_sys_exit.assert_called_once_with(2)

    @patch('os.path.isdir', return_value=True)
    @patch('collector.find_empty_dirs', return_value=['/root/empty1'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_list_only(self, mock_sys_exit, mock_print, mock_find_empty_dirs, mock_isdir):
        # Mock rationale: Test the --list functionality, ensuring no removal is attempted.
        with patch('sys.argv', ['collector.py', '--path', '/test', '--list']):
            collector.main()
            mock_find_empty_dirs.assert_called_once_with('/test')
            mock_print.assert_any_call('Found 1 cosmic dust bunnies:')
            mock_print.assert_any_call('  - /root/empty1')
            mock_print.assert_any_call('Listing complete. Use --remove to sweep them away.')
            mock_sys_exit.assert_called_once_with(0)

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_sys_exit, mock_print, mock_isdir):
        # Mock rationale: Test error handling for an invalid path without touching the filesystem.
        with patch('sys.argv', ['collector.py', '--path', '/nonexistent', '--list']):
            collector.main()
            mock_isdir.assert_called_once_with('/nonexistent')
            mock_print.assert_any_call("Error: Path '/nonexistent' does not exist or is not a directory.", file=sys.stderr)
            mock_sys_exit.assert_called_once_with(1)

    @patch('os.path.isdir', return_value=True)
    @patch('collector.find_empty_dirs', return_value=[])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_dust_bunnies(self, mock_sys_exit, mock_print, mock_find_empty_dirs, mock_isdir):
        # Mock rationale: Test the scenario where no empty directories are found.
        with patch('sys.argv', ['collector.py', '--path', '/test', '--list']):
            collector.main()
            mock_find_empty_dirs.assert_called_once_with('/test')
            mock_print.assert_any_call('No cosmic dust bunnies (empty directories) found. Your space is pristine! ✨')
            mock_sys_exit.assert_called_once_with(0)

    @patch('os.path.isdir', return_value=True)
    @patch('collector.find_empty_dirs', return_value=['/root/empty'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_action_specified(self, mock_sys_exit, mock_print, mock_find_empty_dirs, mock_isdir):
        # Mock rationale: Test the default behavior when neither --list nor --remove is provided.
        with patch('sys.argv', ['collector.py', '--path', '/test']):
            collector.main()
            mock_find_empty_dirs.assert_called_once_with('/test')
            mock_print.assert_any_call('No action specified. Use --list to see them or --remove to sweep them away.')
            mock_sys_exit.assert_called_once_with(2)
