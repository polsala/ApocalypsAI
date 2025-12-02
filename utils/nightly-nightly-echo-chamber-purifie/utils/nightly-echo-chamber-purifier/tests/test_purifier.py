import unittest
import os
import hashlib
from unittest.mock import patch, mock_open, MagicMock
import sys

# Mock rationale: We need to simulate file system operations (walking directories, reading files, deleting files)
# without actually touching the disk. This ensures tests are fast, deterministic, and don't have side effects.
# `os.walk`, `os.path.isfile`, `os.path.islink`, `os.remove` are mocked to control the file system state.
# `open` is mocked to provide specific file contents for hash calculation.
# `sys.exit` is mocked to prevent the test runner from terminating when `main` calls it.
# `builtins.print` is mocked to capture console output for verification.

# Import the functions to be tested
from src.purifier import calculate_file_hash, find_duplicate_files, main

class TestPurifier(unittest.TestCase):

    def setUp(self):
        # Define some mock file contents and their SHA256 hashes
        self.file_contents = {
            'file_a.txt': b'content_a',
            'file_b.txt': b'content_b',
            'file_c.txt': b'content_a', # Duplicate of file_a.txt
            'file_d.txt': b'content_d',
            'empty.txt': b'',
            'link_target.txt': b'link_content'
        }
        self.file_hashes = {
            name: hashlib.sha256(content).hexdigest()
            for name, content in self.file_contents.items()
        }

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash(self, mock_file_open):
        # Mock rationale: Simulate reading file content without actual disk I/O.
        # `mock_file_open` is configured to return specific content when `read` is called.
        mock_file_open.return_value.read.side_effect = [self.file_contents['file_a.txt'], b'']
        self.assertEqual(calculate_file_hash('path/to/file_a.txt'), self.file_hashes['file_a.txt'])
        mock_file_open.assert_called_with('path/to/file_a.txt', 'rb')

        mock_file_open.reset_mock()
        mock_file_open.return_value.read.side_effect = [self.file_contents['empty.txt'], b'']
        self.assertEqual(calculate_file_hash('path/to/empty.txt'), self.file_hashes['empty.txt'])

        # Test for IOError (e.g., permission denied)
        mock_file_open.reset_mock()
        mock_file_open.side_effect = IOError("Permission denied")
        self.assertIsNone(calculate_file_hash('path/to/unreadable.txt'))

    @patch('os.path.islink', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    @patch('src.purifier.calculate_file_hash') # Mock rationale: Isolate `find_duplicate_files` from hash calculation details.
    def test_find_duplicate_files(self, mock_calculate_hash, mock_os_walk, mock_os_isfile, mock_os_islink):
        # Mock rationale: Simulate directory structure and file existence without actual disk I/O.
        # `mock_os_walk` provides the directory traversal.
        # `mock_os_isfile` ensures all reported files are treated as files.
        # `mock_os_islink` ensures symbolic links are ignored.
        # `mock_calculate_hash` provides deterministic hashes for specific file paths.

        # Setup mock_os_walk to simulate a directory structure
        mock_os_walk.return_value = [
            ('/root', ['dir1'], ['file_a.txt', 'file_b.txt']),
            ('/root/dir1', [], ['file_c.txt', 'file_d.txt'])
        ]

        # Setup mock_calculate_hash to return specific hashes for specific files
        mock_calculate_hash.side_effect = lambda f: {
            '/root/file_a.txt': self.file_hashes['file_a.txt'],
            '/root/file_b.txt': self.file_hashes['file_b.txt'],
            '/root/dir1/file_c.txt': self.file_hashes['file_c.txt'], # Same content as file_a.txt
            '/root/dir1/file_d.txt': self.file_hashes['file_d.txt'],
        }.get(f)

        duplicates = find_duplicate_files('/root')

        expected_duplicates = {
            self.file_hashes['file_a.txt']: ['/root/file_a.txt', '/root/dir1/file_c.txt'],
            self.file_hashes['file_b.txt']: ['/root/file_b.txt'],
            self.file_hashes['file_d.txt']: ['/root/dir1/file_d.txt'],
        }

        self.assertIn(self.file_hashes['file_a.txt'], duplicates)
        self.assertCountEqual(duplicates[self.file_hashes['file_a.txt']], expected_duplicates[self.file_hashes['file_a.txt']])
        self.assertCountEqual(duplicates[self.file_hashes['file_b.txt']], expected_duplicates[self.file_hashes['file_b.txt']])
        self.assertCountEqual(duplicates[self.file_hashes['file_d.txt']], expected_duplicates[self.file_hashes['file_d.txt']])

        # Test with a symbolic link (should be ignored)
        mock_os_islink.return_value = True
        mock_os_walk.return_value = [
            ('/root', [], ['link_to_file.txt'])
        ]
        mock_calculate_hash.side_effect = lambda f: {
            '/root/link_to_file.txt': self.file_hashes['link_target.txt']
        }.get(f)
        duplicates_with_link = find_duplicate_files('/root')
        # No files should be processed if they are links, so no hashes should be found.
        # The `find_duplicate_files` returns a defaultdict, so it will be empty if no files are added.
        self.assertEqual(len(duplicates_with_link), 0)

    @patch('os.remove')
    @patch('os.path.isdir', return_value=True)
    @patch('src.purifier.find_duplicate_files') # Mock rationale: Isolate `main` from file system scanning details.
    @patch('builtins.print') # Mock rationale: Capture print output to verify user feedback.
    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Control command-line arguments programmatically.
    def test_main_dry_run(self, mock_parse_args, mock_print, mock_find_duplicates, mock_os_isdir, mock_os_remove):
        # Mock rationale: Simulate running the main script with specific arguments and file system state.
        # `mock_parse_args` sets the arguments.
        # `mock_find_duplicates` provides the duplicate file structure.
        # `mock_print` captures output for assertions.
        # `mock_os_remove` ensures no deletion happens in dry-run.

        # Simulate arguments for a dry run
        mock_parse_args.return_value = MagicMock(directory='./test_dir', delete=False, dry_run=True)

        # Simulate duplicate files found
        mock_find_duplicates.return_value = {
            self.file_hashes['file_a.txt']: ['test_dir/file_a.txt', 'test_dir/subdir/file_c.txt'],
            self.file_hashes['file_b.txt']: ['test_dir/file_b.txt']
        }

        main()

        # Verify print statements for dry run
        mock_print.assert_any_call("\n--- Duplicates for hash " + self.file_hashes['file_a.txt'] + " ---")
        mock_print.assert_any_call("  Original: test_dir/file_a.txt")
        mock_print.assert_any_call("  Duplicate 1: test_dir/subdir/file_c.txt")
        mock_print.assert_any_call("    -> (Dry Run) Would delete: test_dir/subdir/file_c.txt")
        mock_print.assert_any_call("\nOperation completed in dry-run mode. No files were deleted.")
        mock_os_remove.assert_not_called() # Ensure no deletion happened

    @patch('os.remove')
    @patch('os.path.isdir', return_value=True)
    @patch('src.purifier.find_duplicate_files')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_delete_mode(self, mock_parse_args, mock_print, mock_find_duplicates, mock_os_isdir, mock_os_remove):
        # Mock rationale: Simulate running the main script with specific arguments and file system state.
        # `mock_parse_args` sets the arguments.
        # `mock_find_duplicates` provides the duplicate file structure.
        # `mock_print` captures output for assertions.
        # `mock_os_remove` is checked to ensure correct files are deleted.

        # Simulate arguments for delete mode
        mock_parse_args.return_value = MagicMock(directory='./test_dir', delete=True, dry_run=False)

        # Simulate duplicate files found
        mock_find_duplicates.return_value = {
            self.file_hashes['file_a.txt']: ['test_dir/file_a.txt', 'test_dir/subdir/file_c.txt'],
            self.file_hashes['file_b.txt']: ['test_dir/file_b.txt']
        }

        main()

        # Verify print statements for delete mode
        mock_print.assert_any_call("\n--- Duplicates for hash " + self.file_hashes['file_a.txt'] + " ---")
        mock_print.assert_any_call("  Original: test_dir/file_a.txt")
        mock_print.assert_any_call("  Duplicate 1: test_dir/subdir/file_c.txt")
        mock_print.assert_any_call("    -> Deleted: test_dir/subdir/file_c.txt")
        mock_print.assert_any_call("\nDuplicate files deleted successfully.")

        # Ensure os.remove was called for the duplicate
        mock_os_remove.assert_called_once_with('test_dir/subdir/file_c.txt')

    @patch('os.remove')
    @patch('os.path.isdir', return_value=True)
    @patch('src.purifier.find_duplicate_files')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_duplicates(self, mock_parse_args, mock_print, mock_find_duplicates, mock_os_isdir, mock_os_remove):
        # Mock rationale: Simulate running the main script when no duplicates are found.
        # `mock_parse_args` sets the arguments.
        # `mock_find_duplicates` returns an empty set of duplicates (or only unique files).
        # `mock_print` captures output for assertions.

        mock_parse_args.return_value = MagicMock(directory='./test_dir', delete=False, dry_run=True)
        mock_find_duplicates.return_value = {
            self.file_hashes['file_a.txt']: ['test_dir/file_a.txt'],
            self.file_hashes['file_b.txt']: ['test_dir/file_b.txt']
        }

        main()

        mock_print.assert_any_call("\nNo duplicate files found.")
        mock_os_remove.assert_not_called()

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock rationale: Prevent actual exit during testing.
    def test_main_invalid_directory(self, mock_exit, mock_parse_args, mock_print, mock_os_isdir):
        # Mock rationale: Simulate providing an invalid directory to the script.
        # `mock_parse_args` sets the arguments.
        # `mock_os_isdir` returns False to indicate an invalid directory.
        # `mock_print` captures output for assertions.
        # `mock_exit` is mocked to prevent the test runner from terminating.

        mock_parse_args.return_value = MagicMock(directory='./non_existent_dir', delete=False, dry_run=True)

        main()

        mock_print.assert_any_call("Error: Directory './non_existent_dir' not found.")
        mock_exit.assert_called_once_with(1)

    @patch('os.remove')
    @patch('os.path.isdir', return_value=True)
    @patch('src.purifier.find_duplicate_files')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_delete_io_error(self, mock_parse_args, mock_print, mock_find_duplicates, mock_os_isdir, mock_os_remove):
        # Mock rationale: Simulate an error during file deletion.
        # `mock_parse_args` sets the arguments for delete mode.
        # `mock_find_duplicates` provides duplicate files.
        # `mock_os_remove` is configured to raise an OSError.
        # `mock_print` captures output to verify error reporting.

        mock_parse_args.return_value = MagicMock(directory='./test_dir', delete=True, dry_run=False)
        mock_find_duplicates.return_value = {
            self.file_hashes['file_a.txt']: ['test_dir/file_a.txt', 'test_dir/subdir/file_c.txt']
        }
        mock_os_remove.side_effect = OSError("Permission denied")

        main()

        mock_print.assert_any_call("    -> Error deleting test_dir/subdir/file_c.txt: Permission denied")
        mock_os_remove.assert_called_once_with('test_dir/subdir/file_c.txt')


if __name__ == '__main__':
    unittest.main()
