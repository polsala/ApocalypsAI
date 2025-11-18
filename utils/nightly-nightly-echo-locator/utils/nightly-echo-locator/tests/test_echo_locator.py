import unittest
import os
import hashlib
from unittest.mock import patch, mock_open, MagicMock
from collections import defaultdict
import sys

# Add the src directory to the path to allow importing echo_locator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import echo_locator

class TestEchoLocator(unittest.TestCase):

    def setUp(self):
        # Mock os.path.isdir for all tests
        self.mock_isdir_patcher = patch('os.path.isdir')
        self.mock_isdir = self.mock_isdir_patcher.start()
        self.mock_isdir.return_value = True # Assume the root directory exists by default

    def tearDown(self):
        self.mock_isdir_patcher.stop()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True) # Mock rationale: Ensure file existence for open
    def test_calculate_file_hash(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate file content without actual disk I/O.
        # This ensures deterministic results and isolation from the filesystem.
        mock_file_open.return_value.read.side_effect = [b"test content", b""]
        expected_hash = hashlib.sha256(b"test content").hexdigest()
        self.assertEqual(echo_locator.calculate_file_hash("dummy_path.txt"), expected_hash)

        mock_file_open.return_value.read.side_effect = [b"another content", b""]
        expected_hash = hashlib.sha256(b"another content").hexdigest()
        self.assertEqual(echo_locator.calculate_file_hash("another_dummy.txt"), expected_hash)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True) # Mock rationale: Ensure file existence for open
    def test_calculate_file_hash_io_error(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate a file that cannot be read (e.g., permissions issue).
        # This tests error handling without needing to create an actual unreadable file.
        mock_file_open.side_effect = IOError("Permission denied")
        self.assertIsNone(echo_locator.calculate_file_hash("unreadable.txt"))

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True) # Mock rationale: Ensure file existence for open
    def test_find_duplicate_files_no_duplicates(self, mock_exists, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory structure with unique files.
        # This avoids actual filesystem interaction and provides a controlled environment.
        self.mock_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt']),
            ('/root/subdir', [], ['file3.txt'])
        ]
        
        # Mock rationale: Provide specific content for each file to ensure unique hashes.
        # This makes the hash calculation deterministic and testable.
        file_contents = {
            os.path.join('/root', 'file1.txt'): b"content1",
            os.path.join('/root', 'file2.txt'): b"content2",
            os.path.join('/root/subdir', 'file3.txt'): b"content3",
        }

        def mock_open_side_effect(filepath, mode='r'):
            if mode == 'rb':
                mock_file_open.return_value.read.side_effect = [file_contents[filepath], b""]
                return mock_file_open.return_value
            raise ValueError("Unexpected open mode")

        mock_file_open.side_effect = mock_open_side_effect

        duplicates = echo_locator.find_duplicate_files('/root')
        self.assertEqual(duplicates, {})

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True) # Mock rationale: Ensure file existence for open
    def test_find_duplicate_files_with_duplicates(self, mock_exists, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory structure with duplicate files.
        # This allows testing the core logic of finding duplicates without real files.
        self.mock_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/root', [], ['fileA.txt', 'fileB.txt']),
            ('/root/subdir', [], ['fileC.txt', 'fileD.txt'])
        ]

        # Mock rationale: Assign identical content to fileA.txt and fileC.txt to create a duplicate.
        # This ensures a predictable hash for the duplicate pair.
        content_duplicate = b"duplicate content"
        content_unique1 = b"unique content 1"
        content_unique2 = b"unique content 2"

        file_contents = {
            os.path.join('/root', 'fileA.txt'): content_duplicate,
            os.path.join('/root', 'fileB.txt'): content_unique1,
            os.path.join('/root/subdir', 'fileC.txt'): content_duplicate,
            os.path.join('/root/subdir', 'fileD.txt'): content_unique2,
        }

        def mock_open_side_effect(filepath, mode='r'):
            if mode == 'rb':
                mock_file_open.return_value.read.side_effect = [file_contents[filepath], b""]
                return mock_file_open.return_value
            raise ValueError("Unexpected open mode")

        mock_file_open.side_effect = mock_open_side_effect

        expected_hash = hashlib.sha256(content_duplicate).hexdigest()
        expected_duplicates = {
            expected_hash: [
                os.path.join('/root', 'fileA.txt'),
                os.path.join('/root/subdir', 'fileC.txt')
            ]
        }

        duplicates = echo_locator.find_duplicate_files('/root')
        # Sort paths for consistent comparison, as order from os.walk might vary
        for h in expected_duplicates:
            expected_duplicates[h].sort()
        for h in duplicates:
            duplicates[h].sort()

        self.assertEqual(duplicates, expected_duplicates)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True) # Mock rationale: Ensure file existence for open
    def test_find_duplicate_files_multiple_duplicate_sets(self, mock_exists, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate multiple sets of duplicate files.
        # This verifies the tool can identify and group different sets of duplicates.
        self.mock_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/root', [], ['f1.txt', 'f2.txt', 'f3.txt']),
            ('/root/sub1', [], ['f4.txt']),
            ('/root/sub2', [], ['f5.txt'])
        ]

        content_dup1 = b"dup content 1"
        content_dup2 = b"dup content 2"
        content_unique = b"unique content"

        file_contents = {
            os.path.join('/root', 'f1.txt'): content_dup1,
            os.path.join('/root', 'f2.txt'): content_dup2,
            os.path.join('/root', 'f3.txt'): content_unique,
            os.path.join('/root/sub1', 'f4.txt'): content_dup1,
            os.path.join('/root/sub2', 'f5.txt'): content_dup2,
        }

        def mock_open_side_effect(filepath, mode='r'):
            if mode == 'rb':
                mock_file_open.return_value.read.side_effect = [file_contents[filepath], b""]
                return mock_file_open.return_value
            raise ValueError("Unexpected open mode")

        mock_file_open.side_effect = mock_open_side_effect

        hash_dup1 = hashlib.sha256(content_dup1).hexdigest()
        hash_dup2 = hashlib.sha256(content_dup2).hexdigest()

        expected_duplicates = {
            hash_dup1: [os.path.join('/root', 'f1.txt'), os.path.join('/root/sub1', 'f4.txt')],
            hash_dup2: [os.path.join('/root', 'f2.txt'), os.path.join('/root/sub2', 'f5.txt')],
        }

        duplicates = echo_locator.find_duplicate_files('/root')
        for h in expected_duplicates:
            expected_duplicates[h].sort()
        for h in duplicates:
            duplicates[h].sort()

        self.assertEqual(duplicates, expected_duplicates)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True) # Mock rationale: Ensure file existence for open
    def test_find_duplicate_files_empty_directory(self, mock_exists, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate an empty directory.
        # This tests the edge case where no files are present.
        self.mock_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/root', [], []) # No files
        ]
        duplicates = echo_locator.find_duplicate_files('/root')
        self.assertEqual(duplicates, {})

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True) # Mock rationale: Ensure file existence for open
    def test_find_duplicate_files_single_file(self, mock_exists, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory with only one file.
        # This tests that a single file is not reported as a duplicate.
        self.mock_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/root', [], ['single.txt'])
        ]
        file_contents = {os.path.join('/root', 'single.txt'): b"unique content"}
        def mock_open_side_effect(filepath, mode='r'):
            if mode == 'rb':
                mock_file_open.return_value.read.side_effect = [file_contents[filepath], b""]
                return mock_file_open.return_value
            raise ValueError("Unexpected open mode")
        mock_file_open.side_effect = mock_open_side_effect

        duplicates = echo_locator.find_duplicate_files('/root')
        self.assertEqual(duplicates, {})

    def test_find_duplicate_files_non_existent_directory(self):
        # Mock rationale: Simulate a non-existent root directory.
        # This tests the initial directory validation.
        self.mock_isdir.return_value = False # Explicitly set to False for this test
        with patch('sys.stderr', new_callable=MagicMock) as mock_stderr:
            duplicates = echo_locator.find_duplicate_files('/non_existent')
            self.assertEqual(duplicates, {})
            mock_stderr.write.assert_called_with("Error: Directory '/non_existent' not found.\n")

    @patch('sys.argv', ['echo_locator.py', '/test_dir'])
    @patch('echo_locator.find_duplicate_files')
    @patch('builtins.print')
    def test_main_no_duplicates(self, mock_print, mock_find_duplicates):
        # Mock rationale: Test the main function's output when no duplicates are found.
        # This isolates the main function's logic from the file scanning.
        mock_find_duplicates.return_value = {}
        echo_locator.main()
        mock_print.assert_called_with("No duplicate files found in '/test_dir'. Your digital hoard is pristine!")

    @patch('sys.argv', ['echo_locator.py', '/test_dir'])
    @patch('echo_locator.find_duplicate_files')
    @patch('builtins.print')
    def test_main_with_duplicates(self, mock_print, mock_find_duplicates):
        # Mock rationale: Test the main function's output when duplicates are found.
        # This verifies the correct formatting of the duplicate report.
        test_hash = hashlib.sha256(b"content").hexdigest()
        mock_find_duplicates.return_value = {
            test_hash: ['/test_dir/file1.txt', '/test_dir/subdir/file2.txt']
        }
        echo_locator.main()
        mock_print.assert_any_call("Duplicate files found in '/test_dir':")
        mock_print.assert_any_call(f"\nHash: {test_hash}")
        mock_print.assert_any_call("  - /test_dir/file1.txt")
        mock_print.assert_any_call("  - /test_dir/subdir/file2.txt")

    @patch('sys.argv', ['echo_locator.py'])
    @patch('sys.exit')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_main_no_args(self, mock_stderr, mock_exit):
        # Mock rationale: Test the main function's behavior when no arguments are provided.
        # This checks for correct usage message and exit code.
        echo_locator.main()
        mock_stderr.write.assert_called_with("Usage: python src/echo_locator.py <directory_path>\n")
        mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
