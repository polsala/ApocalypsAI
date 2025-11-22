import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path to import sweeper.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sweeper

class TestSweeper(unittest.TestCase):

    @patch('os.walk')
    @patch('os.path.islink')
    @patch('os.path.exists')
    def test_find_empty_dirs(self, mock_exists, mock_islink, mock_walk):
        # Mock rationale: os.walk is a generator that traverses the file system. We need to control its output
        # to simulate different directory structures for testing empty directory detection.
        # os.path.islink and os.path.exists are not directly relevant for find_empty_dirs but are patched
        # because they are used by other functions in sweeper.py and might be called during os.walk's internal checks.

        mock_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file1.txt']),
            ('/root/dir1', [], []), # Empty directory
            ('/root/dir2', ['subdir'], []), # Not empty (has subdir)
            ('/root/dir2/subdir', [], ['subfile.txt']), # Not empty (has file)
            ('/root/empty_but_has_file', [], ['file.txt']), # Not empty (has file)
            ('/root/empty_dir_nested', [], []) # Another empty directory
        ]

        expected_empty_dirs = ['/root/dir1', '/root/empty_dir_nested']
        found_empty_dirs = sweeper.find_empty_dirs('/root')
        self.assertCountEqual(found_empty_dirs, expected_empty_dirs)

    @patch('os.walk')
    @patch('os.path.islink')
    @patch('os.path.exists')
    def test_find_broken_symlinks(self, mock_exists, mock_islink, mock_walk):
        # Mock rationale: os.walk is used to traverse the file system. os.path.islink determines if an entry is a symlink.
        # os.path.exists checks if the target of a symlink exists. We need to control these to simulate broken links.

        # Simulate a directory structure with various links
        mock_walk.return_value = [
            ('/root', [], ['file.txt', 'link_to_existing', 'link_to_broken']),
            ('/root/subdir', [], ['another_link'])
        ]

        # Configure mocks for specific paths
        def islink_side_effect(path):
            return path in ['/root/link_to_existing', '/root/link_to_broken', '/root/subdir/another_link']

        def exists_side_effect(path):
            # For symlinks, os.path.exists(link_path) checks the *target*, not the link itself.
            # So, if we mock os.path.exists('/root/link_to_broken') to be False, it's a broken link.
            return path not in ['/root/link_to_broken', '/root/subdir/another_link']

        mock_islink.side_effect = islink_side_effect
        mock_exists.side_effect = exists_side_effect

        expected_broken_links = ['/root/link_to_broken', '/root/subdir/another_link']
        found_broken_links = sweeper.find_broken_symlinks('/root')
        self.assertCountEqual(found_broken_links, expected_broken_links)

    @patch('builtins.print')
    @patch('os.rmdir')
    @patch('os.remove')
    @patch('os.path.isdir')
    def test_sweep_items_dry_run(self, mock_isdir, mock_remove, mock_rmdir, mock_print):
        # Mock rationale: builtins.print is mocked to capture output without affecting the console.
        # os.rmdir and os.remove are mocked to prevent actual file system modifications during a dry run test.
        # os.path.isdir is mocked to simulate whether an item is a directory or a file (symlink).

        items_to_sweep = ['/path/to/empty_dir', '/path/to/broken_link']
        mock_isdir.side_effect = lambda x: x == '/path/to/empty_dir'

        sweeper.sweep_items(items_to_sweep, dry_run=True, item_type="test item")

        mock_rmdir.assert_not_called()
        mock_remove.assert_not_called()
        mock_print.assert_any_call('\n(Dry run complete. No changes were made.)')
        mock_print.assert_any_call('  - /path/to/empty_dir')
        mock_print.assert_any_call('  - /path/to/broken_link')

    @patch('builtins.print')
    @patch('os.rmdir')
    @patch('os.remove')
    @patch('os.path.isdir')
    def test_sweep_items_actual_run(self, mock_isdir, mock_remove, mock_rmdir, mock_print):
        # Mock rationale: builtins.print is mocked to capture output. os.rmdir and os.remove are mocked
        # to simulate successful deletion without actual file system changes. os.path.isdir is mocked
        # to direct calls to either rmdir or remove based on item type.

        items_to_sweep = ['/path/to/empty_dir', '/path/to/broken_link']
        mock_isdir.side_effect = lambda x: x == '/path/to/empty_dir'

        sweeper.sweep_items(items_to_sweep, dry_run=False, item_type="test item")

        mock_rmdir.assert_called_once_with('/path/to/empty_dir')
        mock_remove.assert_called_once_with('/path/to/broken_link')
        mock_print.assert_any_call('  [SWEPT] Removed empty directory: /path/to/empty_dir')
        mock_print.assert_any_call('  [SWEPT] Removed broken symlink: /path/to/broken_link')
        mock_print.assert_any_call('Sweeping complete.')

    @patch('builtins.print')
    @patch('os.rmdir', side_effect=OSError("Permission denied"))
    @patch('os.remove', side_effect=OSError("File not found"))
    @patch('os.path.isdir')
    def test_sweep_items_error_handling(self, mock_isdir, mock_remove, mock_rmdir, mock_print):
        # Mock rationale: Simulate OSError during deletion to ensure error handling is robust.
        # os.path.isdir is mocked to ensure both rmdir and remove paths are tested.

        items_to_sweep = ['/path/to/empty_dir', '/path/to/broken_link']
        mock_isdir.side_effect = lambda x: x == '/path/to/empty_dir'

        sweeper.sweep_items(items_to_sweep, dry_run=False, item_type="test item")

        mock_rmdir.assert_called_once_with('/path/to/empty_dir')
        mock_remove.assert_called_once_with('/path/to/broken_link')
        mock_print.assert_any_call('  [ERROR] Could not remove test item /path/to/empty_dir: Permission denied')
        mock_print.assert_any_call('  [ERROR] Could not remove test item /path/to/broken_link: File not found')

    @patch('sys.exit')
    @patch('builtins.print')
    @patch('os.path.isdir', return_value=False)
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/nonexistent', dry_run=False))
    def test_main_invalid_path(self, mock_parse_args, mock_isdir, mock_print, mock_exit):
        # Mock rationale: sys.exit is mocked to prevent the test runner from exiting. builtins.print
        # is mocked to capture error messages. os.path.isdir is mocked to simulate an invalid path.
        # argparse.ArgumentParser.parse_args is mocked to provide specific CLI arguments.

        sweeper.main()
        mock_print.assert_any_call("Error: The provided path '/nonexistent' is not a valid directory.", file=sys.stderr)
        mock_exit.assert_called_once_with(1)

    @patch('sys.exit')
    @patch('builtins.print')
    @patch('os.path.isdir', return_value=True)
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/test_root', dry_run=True))
    @patch('sweeper.find_empty_dirs', return_value=['/test_root/empty_dir'])
    @patch('sweeper.find_broken_symlinks', return_value=['/test_root/broken_link'])
    @patch('sweeper.sweep_items')
    def test_main_workflow(self, mock_sweep_items, mock_find_broken_symlinks, mock_find_empty_dirs, mock_isdir, mock_print, mock_exit):
        # Mock rationale: This tests the main execution flow. All internal functions (find_empty_dirs, find_broken_symlinks,
        # sweep_items) are mocked to control their behavior and verify they are called correctly. os.path.isdir and
        # argparse.ArgumentParser.parse_args are mocked for setup. sys.exit and builtins.print are mocked for output control.

        sweeper.main()

        mock_find_empty_dirs.assert_called_once_with('/test_root')
        mock_find_broken_symlinks.assert_called_once_with('/test_root')
        self.assertEqual(mock_sweep_items.call_count, 2)
        mock_sweep_items.assert_any_call(['/test_root/empty_dir'], True, item_type='empty directory')
        mock_sweep_items.assert_any_call(['/test_root/broken_link'], True, item_type='broken symbolic link')
        mock_print.assert_any_call("Scanning '/test_root' for digital dust bunnies...")

    @patch('sys.exit')
    @patch('builtins.print')
    @patch('os.path.isdir', return_value=True)
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/test_root', dry_run=True))
    @patch('sweeper.find_empty_dirs', return_value=[])
    @patch('sweeper.find_broken_symlinks', return_value=[])
    @patch('sweeper.sweep_items')
    def test_main_no_dust_bunnies(self, mock_sweep_items, mock_find_broken_symlinks, mock_find_empty_dirs, mock_isdir, mock_print, mock_exit):
        # Mock rationale: Similar to test_main_workflow, but specifically tests the scenario where no items are found.

        sweeper.main()

        mock_find_empty_dirs.assert_called_once_with('/test_root')
        mock_find_broken_symlinks.assert_called_once_with('/test_root')
        self.assertEqual(mock_sweep_items.call_count, 2) # Still called, but with empty lists
        mock_print.assert_any_call('\nNo digital dust bunnies found. Your directory is pristine!')
