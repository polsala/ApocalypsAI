import unittest
import os
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

# Add the src directory to the path to allow importing duster.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import duster

class TestDuster(unittest.TestCase):

    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize')
    def test_find_empty_files(self, mock_getsize, mock_isfile, mock_walk):
        # Mock rationale: Simulate a directory structure with files of various sizes.
        # os.walk is mocked to control directory traversal.
        # os.path.isfile is mocked to ensure all paths are treated as files for size check.
        # os.path.getsize is mocked to return specific sizes for specific files.

        mock_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['fileA.txt', 'fileB.log']),
            ('/root/dir1', [], ['fileC.txt', 'fileD.py']),
            ('/root/dir2', [], ['fileE.json'])
        ]

        def getsize_side_effect(path):
            if path == '/root/fileA.txt': return 0
            if path == '/root/fileB.log': return 100
            if path == '/root/dir1/fileC.txt': return 0
            if path == '/root/dir1/fileD.py': return 200
            if path == '/root/dir2/fileE.json': return 0
            return 50 # Default for unexpected files

        mock_getsize.side_effect = getsize_side_effect

        empty_files = duster.find_empty_files('/root')
        expected_files = [
            '/root/fileA.txt',
            '/root/dir1/fileC.txt',
            '/root/dir2/fileE.json'
        ]
        self.assertCountEqual(empty_files, expected_files)

    @patch('os.walk')
    def test_find_empty_dirs(self, mock_walk):
        # Mock rationale: Simulate a directory structure with nested empty and non-empty directories.
        # os.walk is mocked with topdown=False to simulate bottom-up traversal, crucial for empty dir detection.

        # Structure (as seen by os.walk topdown=False):
        # /root/empty_dir1 (empty)
        # /root/non_empty_dir (contains file.txt)
        # /root/nested_empty_dir/another_empty_dir (empty)
        # /root/nested_empty_dir (contains only another_empty_dir, which is empty)
        # /root/dir_with_only_empty_subdir/only_empty_subdir (empty)
        # /root/dir_with_only_empty_subdir (contains only only_empty_subdir, which is empty)
        # /root (contains other dirs)

        mock_walk.return_value = [
            ('/root/empty_dir1', [], []),
            ('/root/non_empty_dir', [], ['file.txt']),
            ('/root/nested_empty_dir/another_empty_dir', [], []),
            ('/root/nested_empty_dir', ['another_empty_dir'], []),
            ('/root/dir_with_only_empty_subdir/only_empty_subdir', [], []),
            ('/root/dir_with_only_empty_subdir', ['only_empty_subdir'], []),
            ('/root', ['empty_dir1', 'non_empty_dir', 'nested_empty_dir', 'dir_with_only_empty_subdir'], [])
        ]

        empty_dirs = duster.find_empty_dirs('/root')
        expected_dirs = [
            '/root/empty_dir1',
            '/root/nested_empty_dir/another_empty_dir',
            '/root/dir_with_only_empty_subdir/only_empty_subdir'
        ]
        self.assertCountEqual(empty_dirs, expected_dirs)

    @patch('os.path.abspath', side_effect=lambda x: f'/abs{x}') # Mock rationale: Make abspath deterministic for testing
    def test_generate_report(self, mock_abspath):
        # Mock rationale: Test the formatting of the report string without file system interaction.
        empty_files = ['/path/to/empty_file.txt', '/another/empty.log']
        empty_dirs = ['/path/to/empty_dir', '/another/empty/folder']
        root_dir = '/test/root'

        report = duster.generate_report(root_dir, empty_files, empty_dirs)

        self.assertIn("--- Data Dust Bunny Duster Report ---", report)
        self.assertIn(f"Scanned directory: /abs{root_dir}", report)
        self.assertIn("Empty Files Found:", report)
        self.assertIn("  - /path/to/empty_file.txt", report)
        self.assertIn("  - /another/empty.log", report)
        self.assertIn("Empty Directories Found:", report)
        self.assertIn("  - /path/to/empty_dir", report)
        self.assertIn("  - /another/empty/folder", report)
        self.assertIn("-------------------------------------", report)

        report_no_items = duster.generate_report(root_dir, [], [])
        self.assertIn("No empty files detected.", report_no_items)
        self.assertIn("No empty directories detected.", report_no_items)

    @patch('os.remove')
    @patch('os.rmdir')
    @patch('builtins.print')
    def test_clean_up_dry_run(self, mock_print, mock_rmdir, mock_remove):
        # Mock rationale: Test dry-run behavior. os.remove and os.rmdir should not be called.
        empty_files = ['/file1.txt']
        empty_dirs = ['/dir1']

        duster.clean_up(empty_files, empty_dirs, dry_run=True, verbose=False)

        mock_remove.assert_not_called()
        mock_rmdir.assert_not_called()
        mock_print.assert_called_with("\nDry run mode: No changes will be made.")

    @patch('os.remove')
    @patch('os.rmdir')
    @patch('builtins.print')
    def test_clean_up_actual_delete(self, mock_print, mock_rmdir, mock_remove):
        # Mock rationale: Test actual deletion. os.remove and os.rmdir should be called.
        empty_files = ['/file1.txt', '/file2.log']
        empty_dirs = ['/dir1', '/dir2/nested'] # Ensure nested is deleted first

        duster.clean_up(empty_files, empty_dirs, dry_run=False, verbose=True)

        mock_remove.assert_any_call('/file1.txt')
        mock_remove.assert_any_call('/file2.log')
        self.assertEqual(mock_remove.call_count, 2)

        mock_rmdir.assert_any_call('/dir2/nested') # Deepest first
        mock_rmdir.assert_any_call('/dir1')
        self.assertEqual(mock_rmdir.call_count, 2)

        mock_print.assert_any_call('  Deleted empty file: /file1.txt')
        mock_print.assert_any_call('  Deleted empty directory: /dir2/nested')
        mock_print.assert_any_call('  Deleted empty directory: /dir1')
        self.assertIn('Cleanup complete. Total items deleted: 4', [call.args[0] for call in mock_print.call_args_list])

    @patch('os.remove', side_effect=OSError('Permission denied'))
    @patch('os.rmdir', side_effect=OSError('Directory not empty'))
    @patch('builtins.print')
    def test_clean_up_with_errors(self, mock_print, mock_rmdir, mock_remove):
        # Mock rationale: Test error handling during deletion.
        empty_files = ['/file_error.txt']
        empty_dirs = ['/dir_error']

        duster.clean_up(empty_files, empty_dirs, dry_run=False, verbose=False)

        mock_remove.assert_called_once_with('/file_error.txt')
        mock_rmdir.assert_called_once_with('/dir_error')
        mock_print.assert_any_call("  Error deleting file /file_error.txt: Permission denied")
        mock_print.assert_any_call("  Error deleting directory /dir_error: Directory not empty")
        self.assertIn('Cleanup complete. Total items deleted: 0', [call.args[0] for call in mock_print.call_args_list])

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=True)
    @patch('duster.find_empty_files', return_value=['/mock/file.txt'])
    @patch('duster.find_empty_dirs', return_value=['/mock/dir'])
    @patch('duster.generate_report', return_value='Mock Report')
    @patch('builtins.input', return_value='yes')
    @patch('duster.clean_up')
    @patch('builtins.print')
    def test_main_delete_yes(self, mock_print, mock_clean_up, mock_input, mock_generate_report, mock_find_empty_dirs, mock_find_empty_files, mock_isdir, mock_parse_args):
        # Mock rationale: Test the main function's flow when --delete is used and user confirms.
        # All external interactions (arg parsing, file system checks, core logic, user input, cleanup) are mocked.
        mock_parse_args.return_value = MagicMock(path='/test_path', delete=True, verbose=False)

        duster.main()

        mock_isdir.assert_called_once_with('/test_path')
        mock_find_empty_files.assert_called_once_with('/test_path')
        mock_find_empty_dirs.assert_called_once_with('/test_path')
        mock_generate_report.assert_called_once_with('/test_path', ['/mock/file.txt'], ['/mock/dir'])
        mock_print.assert_any_call('Mock Report')
        mock_input.assert_called_once_with('\nAre you sure you want to delete these items? (yes/no): ')
        mock_clean_up.assert_called_once_with(['/mock/file.txt'], ['/mock/dir'], dry_run=False, verbose=False)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=True)
    @patch('duster.find_empty_files', return_value=['/mock/file.txt'])
    @patch('duster.find_empty_dirs', return_value=['/mock/dir'])
    @patch('duster.generate_report', return_value='Mock Report')
    @patch('builtins.input', return_value='no')
    @patch('duster.clean_up')
    @patch('builtins.print')
    def test_main_delete_no(self, mock_print, mock_clean_up, mock_input, mock_generate_report, mock_find_empty_dirs, mock_find_empty_files, mock_isdir, mock_parse_args):
        # Mock rationale: Test the main function's flow when --delete is used and user declines.
        mock_parse_args.return_value = MagicMock(path='/test_path', delete=True, verbose=False)

        duster.main()

        mock_input.assert_called_once()
        mock_clean_up.assert_not_called()
        mock_print.assert_any_call('Cleanup cancelled.')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=True)
    @patch('duster.find_empty_files', return_value=[])
    @patch('duster.find_empty_dirs', return_value=[])
    @patch('duster.generate_report', return_value='Mock Report')
    @patch('builtins.input')
    @patch('duster.clean_up')
    @patch('builtins.print')
    def test_main_no_items_to_delete(self, mock_print, mock_clean_up, mock_input, mock_generate_report, mock_find_empty_dirs, mock_find_empty_files, mock_isdir, mock_parse_args):
        # Mock rationale: Test the main function's flow when no empty items are found, even with --delete.
        mock_parse_args.return_value = MagicMock(path='/test_path', delete=True, verbose=False)

        duster.main()

        mock_input.assert_not_called()
        mock_clean_up.assert_not_called()
        mock_print.assert_any_call('No empty files or directories to delete.')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=True)
    @patch('duster.find_empty_files', return_value=['/mock/file.txt'])
    @patch('duster.find_empty_dirs', return_value=['/mock/dir'])
    @patch('duster.generate_report', return_value='Mock Report')
    @patch('duster.clean_up')
    @patch('builtins.print')
    def test_main_no_delete_flag(self, mock_print, mock_clean_up, mock_generate_report, mock_find_empty_dirs, mock_find_empty_files, mock_isdir, mock_parse_args):
        # Mock rationale: Test the main function's flow when --delete flag is not present (dry run implicitly).
        mock_parse_args.return_value = MagicMock(path='/test_path', delete=False, verbose=False)

        duster.main()

        mock_clean_up.assert_not_called()
        mock_print.assert_any_call("\nTo delete these items, run the utility again with the '--delete' flag.")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_print, mock_isdir, mock_parse_args):
        # Mock rationale: Test error handling for an invalid path.
        mock_parse_args.return_value = MagicMock(path='/nonexistent', delete=False, verbose=False)

        duster.main()

        mock_isdir.assert_called_once_with('/nonexistent')
        mock_print.assert_called_once_with("Error: The specified path '/nonexistent' is not a valid directory.")
        mock_exit.assert_called_once_with(1)
