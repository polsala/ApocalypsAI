import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import hashlib

# Add the src directory to the path to allow importing purifier
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from purifier import calculate_file_hash, find_duplicate_files, report_and_remove_duplicates, main

class TestPurifier(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    def test_calculate_file_hash(self, mock_file):
        # Mock rationale: We don't want to read actual files during unit tests.
        # `mock_open` simulates file content, ensuring deterministic hashing.
        filepath = "/fake/path/to/file.txt"
        expected_hash = hashlib.md5(b'test content').hexdigest()
        self.assertEqual(calculate_file_hash(filepath), expected_hash)
        mock_file.assert_called_once_with(filepath, 'rb')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    def test_find_duplicate_files_no_duplicates(self, mock_walk, mock_isfile, mock_open_func):
        # Mock rationale: Simulate file system traversal without actual disk I/O.
        # `os.walk` is mocked to return a predefined structure.
        # `os.path.isfile` ensures our mock files are treated as files.
        # `builtins.open` is mocked to provide unique content for each file.

        # Setup mock_walk to simulate a directory structure
        mock_walk.return_value = [
            ('/dir1', [], ['fileA.txt', 'fileB.txt']),
            ('/dir1/subdir', [], ['fileC.txt'])
        ]

        # Setup mock_open to return different content for each file
        file_contents = {
            '/dir1/fileA.txt': b'content A',
            '/dir1/fileB.txt': b'content B',
            '/dir1/subdir/fileC.txt': b'content C',
        }
        
        def mock_open_side_effect(filepath, mode='r'):
            if mode == 'rb':
                m = mock_open(read_data=file_contents.get(filepath, b''))
                return m() # Return the mock file object
            return mock_open_func(filepath, mode) # Fallback for other modes if needed

        mock_open_func.side_effect = mock_open_side_effect

        directories = ['/dir1']
        duplicates = find_duplicate_files(directories)

        self.assertEqual(len(duplicates), 3) # 3 unique files
        self.assertIn(hashlib.md5(b'content A').hexdigest(), duplicates)
        self.assertIn(hashlib.md5(b'content B').hexdigest(), duplicates)
        self.assertIn(hashlib.md5(b'content C').hexdigest(), duplicates)
        self.assertEqual(len(duplicates[hashlib.md5(b'content A').hexdigest()]), 1)
        self.assertEqual(len(duplicates[hashlib.md5(b'content B').hexdigest()]), 1)
        self.assertEqual(len(duplicates[hashlib.md5(b'content C').hexdigest()]), 1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    def test_find_duplicate_files_with_duplicates(self, mock_walk, mock_isfile, mock_open_func):
        # Mock rationale: Simulate file system traversal with duplicate files.
        # `os.walk` and `os.path.isfile` are mocked as before.
        # `builtins.open` is mocked to provide identical content for duplicate files.

        mock_walk.return_value = [
            ('/dir1', [], ['file1.txt', 'file2.txt']),
            ('/dir2', [], ['file3.txt'])
        ]

        file_contents = {
            '/dir1/file1.txt': b'duplicate content',
            '/dir1/file2.txt': b'unique content',
            '/dir2/file3.txt': b'duplicate content',
        }
        
        def mock_open_side_effect(filepath, mode='r'):
            if mode == 'rb':
                m = mock_open(read_data=file_contents.get(filepath, b''))
                return m()
            return mock_open_func(filepath, mode)

        mock_open_func.side_effect = mock_open_side_effect

        directories = ['/dir1', '/dir2']
        duplicates = find_duplicate_files(directories)

        duplicate_hash = hashlib.md5(b'duplicate content').hexdigest()
        unique_hash = hashlib.md5(b'unique content').hexdigest()

        self.assertEqual(len(duplicates), 2) # One duplicate group, one unique file
        self.assertIn(duplicate_hash, duplicates)
        self.assertIn(unique_hash, duplicates)
        self.assertEqual(len(duplicates[duplicate_hash]), 2)
        self.assertIn('/dir1/file1.txt', duplicates[duplicate_hash])
        self.assertIn('/dir2/file3.txt', duplicates[duplicate_hash])
        self.assertEqual(len(duplicates[unique_hash]), 1)
        self.assertIn('/dir1/file2.txt', duplicates[unique_hash])

    @patch('os.remove')
    @patch('builtins.print')
    def test_report_and_remove_duplicates_dry_run(self, mock_print, mock_remove):
        # Mock rationale: `os.remove` is mocked to prevent actual file deletion.
        # `builtins.print` is mocked to capture output and verify reporting.
        duplicate_groups = {
            'hash1': ['/path/to/original.txt', '/path/to/duplicate1.txt', '/path/to/duplicate2.txt'],
            'hash2': ['/path/to/another_original.txt', '/path/to/another_duplicate.txt']
        }
        
        files_found, files_removed = report_and_remove_duplicates(duplicate_groups, remove=False)

        self.assertEqual(files_found, 5) # 3 in first group + 2 in second group
        self.assertEqual(files_removed, 0) # Dry run, no removals
        mock_remove.assert_not_called()
        mock_print.assert_any_call(unittest.mock.ANY) # Check if print was called at all
        mock_print.assert_any_call('    [DRY RUN] Would remove /path/to/duplicate1.txt')
        mock_print.assert_any_call('    [DRY RUN] Would remove /path/to/duplicate2.txt')
        mock_print.assert_any_call('    [DRY RUN] Would remove /path/to/another_duplicate.txt')

    @patch('os.remove')
    @patch('builtins.print')
    def test_report_and_remove_duplicates_with_removal(self, mock_print, mock_remove):
        # Mock rationale: `os.remove` is mocked to prevent actual file deletion.
        # `builtins.print` is mocked to capture output and verify reporting.
        duplicate_groups = {
            'hash1': ['/path/to/original.txt', '/path/to/duplicate1.txt', '/path/to/duplicate2.txt'],
            'hash2': ['/path/to/another_original.txt', '/path/to/another_duplicate.txt']
        }
        
        files_found, files_removed = report_and_remove_duplicates(duplicate_groups, remove=True)

        self.assertEqual(files_found, 5)
        self.assertEqual(files_removed, 3) # 2 from first group, 1 from second group
        mock_remove.assert_any_call('/path/to/duplicate1.txt')
        mock_remove.assert_any_call('/path/to/duplicate2.txt')
        mock_remove.assert_any_call('/path/to/another_duplicate.txt')
        self.assertEqual(mock_remove.call_count, 3)
        mock_print.assert_any_call('    [REMOVED] /path/to/duplicate1.txt')
        mock_print.assert_any_call('    [REMOVED] /path/to/duplicate2.txt')
        mock_print.assert_any_call('    [REMOVED] /path/to/another_duplicate.txt')

    @patch('os.remove')
    @patch('builtins.print')
    def test_report_and_remove_duplicates_removal_error(self, mock_print, mock_remove):
        # Mock rationale: Simulate an OSError during file removal.
        # `os.remove` is mocked to raise an exception.
        # `builtins.print` is mocked to capture error messages.
        mock_remove.side_effect = OSError("Permission denied")
        duplicate_groups = {
            'hash1': ['/path/to/original.txt', '/path/to/duplicate1.txt']
        }
        
        files_found, files_removed = report_and_remove_duplicates(duplicate_groups, remove=True)

        self.assertEqual(files_found, 2)
        self.assertEqual(files_removed, 0) # Error occurred, so no files were successfully removed
        mock_remove.assert_called_once_with('/path/to/duplicate1.txt')
        mock_print.assert_any_call('    [ERROR] Could not remove /path/to/duplicate1.txt: Permission denied')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('purifier.find_duplicate_files')
    @patch('purifier.report_and_remove_duplicates')
    @patch('builtins.print')
    def test_main_no_duplicates(self, mock_print, mock_report, mock_find, mock_parse_args):
        # Mock rationale: Isolate the `main` function logic.
        # `argparse` is mocked to control CLI arguments.
        # `find_duplicate_files` is mocked to return no duplicates.
        # `report_and_remove_duplicates` is mocked as it won't be called if no duplicates.
        # `builtins.print` is mocked to check output.

        mock_parse_args.return_value = MagicMock(directories=['/test_dir'], remove=False, verbose=False)
        mock_find.return_value = {
            'hash_unique_1': ['/test_dir/file1.txt'],
            'hash_unique_2': ['/test_dir/file2.txt']
        } # Only unique files

        main()

        mock_find.assert_called_once_with(['/test_dir'], False)
        mock_report.assert_not_called() # Should not be called if no actual duplicates
        mock_print.assert_any_call('\nNo duplicate files found. Your echo chamber is pure!')
        mock_print.assert_any_call('Purification complete!')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('purifier.find_duplicate_files')
    @patch('purifier.report_and_remove_duplicates')
    @patch('builtins.print')
    def test_main_with_duplicates_dry_run(self, mock_print, mock_report, mock_find, mock_parse_args):
        # Mock rationale: Isolate the `main` function logic.
        # `argparse` is mocked to control CLI arguments.
        # `find_duplicate_files` is mocked to return duplicates.
        # `report_and_remove_duplicates` is mocked to check its call.
        # `builtins.print` is mocked to check output.

        mock_parse_args.return_value = MagicMock(directories=['/test_dir'], remove=False, verbose=True)
        mock_find.return_value = {
            'hash_dup': ['/test_dir/file1.txt', '/test_dir/file2.txt'],
            'hash_unique': ['/test_dir/file3.txt']
        }
        mock_report.return_value = (3, 2) # 3 files found (including original), 2 would be removed

        main()

        mock_find.assert_called_once_with(['/test_dir'], True)
        # Ensure only actual duplicates are passed to report_and_remove_duplicates
        expected_actual_duplicates = {'hash_dup': ['/test_dir/file1.txt', '/test_dir/file2.txt']}
        mock_report.assert_called_once_with(expected_actual_duplicates, False, True)
        mock_print.assert_any_call('Mode: DRY RUN (no files will be deleted)')
        mock_print.assert_any_call('Total duplicate files identified (including originals): 3')
        mock_print.assert_any_call('Total files that would be removed: 2')
        mock_print.assert_any_call('Purification complete!')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('purifier.find_duplicate_files')
    @patch('purifier.report_and_remove_duplicates')
    @patch('builtins.print')
    def test_main_with_duplicates_remove(self, mock_print, mock_report, mock_find, mock_parse_args):
        # Mock rationale: Isolate the `main` function logic.
        # `argparse` is mocked to control CLI arguments.
        # `find_duplicate_files` is mocked to return duplicates.
        # `report_and_remove_duplicates` is mocked to check its call.
        # `builtins.print` is mocked to check output.

        mock_parse_args.return_value = MagicMock(directories=['/test_dir'], remove=True, verbose=False)
        mock_find.return_value = {
            'hash_dup': ['/test_dir/file1.txt', '/test_dir/file2.txt']
        }
        mock_report.return_value = (2, 1) # 2 files found, 1 removed

        main()

        mock_find.assert_called_once_with(['/test_dir'], False)
        expected_actual_duplicates = {'hash_dup': ['/test_dir/file1.txt', '/test_dir/file2.txt']}
        mock_report.assert_called_once_with(expected_actual_duplicates, True, False)
        mock_print.assert_any_call('Mode: REMOVE duplicates')
        mock_print.assert_any_call('Total files that were removed: 1')
        mock_print.assert_any_call('Purification complete!')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_no_directories_provided(self, mock_print, mock_parse_args):
        # Mock rationale: Test the case where no directories are provided to the CLI.
        # `argparse` is mocked to simulate no directory arguments.
        # `builtins.print` is mocked to check error output.
        mock_parse_args.return_value = MagicMock(directories=[], remove=False, verbose=False)
        
        with patch('argparse.ArgumentParser.print_help') as mock_print_help:
            main()
            mock_print.assert_any_call('Error: At least one directory path must be provided.')
            mock_print_help.assert_called_once()

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    def test_find_duplicate_files_invalid_directory(self, mock_print, mock_isdir):
        # Mock rationale: Simulate an invalid directory path.
        # `os.path.isdir` is mocked to return False.
        # `builtins.print` is mocked to check warning output.
        directories = ['/non/existent/dir']
        duplicates = find_duplicate_files(directories)
        self.assertEqual(duplicates, {})
        mock_print.assert_any_call('Warning: Directory not found or not accessible: /non/existent/dir')


if __name__ == '__main__':
    unittest.main()
