import unittest
import os
import tempfile
import shutil
import hashlib
from unittest.mock import patch, mock_open

# Mock rationale: We need to test the core logic of file hashing and file system traversal.
# For `calculate_file_hash`, `mock_open` allows us to simulate file content without actual disk I/O,
# ensuring the hash calculation logic is tested deterministically. For `find_duplicates` and `main`,
# we use `tempfile` to create actual temporary files and directories. This provides a realistic
# and deterministic environment for `os.walk` and `os.path.getsize` without relying on external
# system state or actual user files. It ensures isolation and cleanup for each test.
# `sys.stdout`, `sys.stderr`, and `sys.exit` are patched to capture CLI output and prevent program termination.

# Import the functions to be tested
from src.duster import calculate_file_hash, find_duplicates, main

class TestDuster(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for tests that need actual files
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory after each test
        shutil.rmtree(self.test_dir)

    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    def test_calculate_file_hash_mocked_content(self, mock_file):
        expected_hash = hashlib.sha256(b'test content').hexdigest()
        self.assertEqual(calculate_file_hash('/fake/path/file.txt'), expected_hash)
        mock_file.assert_called_once_with('/fake/path/file.txt', 'rb')

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_io_error(self, mock_file):
        mock_file.side_effect = IOError("Permission denied")
        with patch('sys.stderr') as mock_stderr:
            result = calculate_file_hash('/fake/path/file.txt')
            self.assertEqual(result, "")
            mock_stderr.write.assert_called_once_with('Error reading file /fake/path/file.txt: Permission denied\n')

    def test_find_duplicates_no_duplicates(self):
        # Create unique files
        os.makedirs(os.path.join(self.test_dir, 'subdir'), exist_ok=True)
        with open(os.path.join(self.test_dir, 'file1.txt'), 'w') as f: f.write('content A')
        with open(os.path.join(self.test_dir, 'file2.txt'), 'w') as f: f.write('content B')
        with open(os.path.join(self.test_dir, 'subdir', 'file3.txt'), 'w') as f: f.write('content C')

        duplicates = find_duplicates([self.test_dir])
        self.assertEqual(duplicates, {})

    def test_find_duplicates_with_duplicates(self):
        # Create files with duplicates
        subdir = os.path.join(self.test_dir, 'subdir')
        os.makedirs(subdir, exist_ok=True)

        content_a = b'duplicate content A'
        content_b = b'unique content B'

        with open(os.path.join(self.test_dir, 'dup1.txt'), 'wb') as f: f.write(content_a)
        with open(os.path.join(subdir, 'dup2.txt'), 'wb') as f: f.write(content_a)
        with open(os.path.join(self.test_dir, 'unique.txt'), 'wb') as f: f.write(content_b)
        with open(os.path.join(self.test_dir, 'another_dup1.txt'), 'wb') as f: f.write(content_a)

        expected_hash_a = hashlib.sha256(content_a).hexdigest()

        duplicates = find_duplicates([self.test_dir])

        self.assertIn(expected_hash_a, duplicates)
        self.assertEqual(len(duplicates[expected_hash_a]), 3)
        self.assertIn(os.path.join(self.test_dir, 'dup1.txt'), duplicates[expected_hash_a])
        self.assertIn(os.path.join(subdir, 'dup2.txt'), duplicates[expected_hash_a])
        self.assertIn(os.path.join(self.test_dir, 'another_dup1.txt'), duplicates[expected_hash_a])
        self.assertEqual(len(duplicates), 1) # Only one group of duplicates

    def test_find_duplicates_multiple_directories(self):
        dir1 = os.path.join(self.test_dir, 'dir1')
        dir2 = os.path.join(self.test_dir, 'dir2')
        os.makedirs(dir1, exist_ok=True)
        os.makedirs(dir2, exist_ok=True)

        content_c = b'shared content C'
        with open(os.path.join(dir1, 'file_c1.txt'), 'wb') as f: f.write(content_c)
        with open(os.path.join(dir2, 'file_c2.txt'), 'wb') as f: f.write(content_c)

        expected_hash_c = hashlib.sha256(content_c).hexdigest()

        duplicates = find_duplicates([dir1, dir2])

        self.assertIn(expected_hash_c, duplicates)
        self.assertEqual(len(duplicates[expected_hash_c]), 2)
        self.assertIn(os.path.join(dir1, 'file_c1.txt'), duplicates[expected_hash_c])
        self.assertIn(os.path.join(dir2, 'file_c2.txt'), duplicates[expected_hash_c])

    def test_find_duplicates_empty_directory(self):
        empty_dir = os.path.join(self.test_dir, 'empty')
        os.makedirs(empty_dir, exist_ok=True)
        duplicates = find_duplicates([empty_dir])
        self.assertEqual(duplicates, {})

    @patch('sys.stderr')
    def test_find_duplicates_non_existent_directory(self, mock_stderr):
        non_existent_dir = os.path.join(self.test_dir, 'non_existent')
        duplicates = find_duplicates([non_existent_dir])
        self.assertEqual(duplicates, {})
        mock_stderr.write.assert_called_once_with(f"Warning: Path '{non_existent_dir}' is not a directory and will be skipped.\n")

    @patch('sys.stdout')
    @patch('sys.stderr')
    @patch('sys.exit')
    def test_main_no_args(self, mock_exit, mock_stderr, mock_stdout):
        with patch('sys.argv', ['src/duster.py']):
            main()
            mock_stderr.write.assert_called_with('Usage: python src/duster.py <directory1> [directory2] ...\n')
            mock_exit.assert_called_once_with(1)

    @patch('sys.stdout')
    @patch('sys.stderr')
    @patch('sys.exit')
    def test_main_no_duplicates_found(self, mock_exit, mock_stderr, mock_stdout):
        with patch('sys.argv', ['src/duster.py', self.test_dir]):
            # Ensure the test_dir has unique files
            with open(os.path.join(self.test_dir, 'unique_file.txt'), 'w') as f: f.write('unique content')
            main()
            mock_stdout.write.assert_called_with('No duplicate files found. Your digital wasteland is surprisingly clean!\n')
            mock_exit.assert_called_once_with(0)

    @patch('sys.stdout')
    @patch('sys.stderr')
    @patch('sys.exit')
    def test_main_duplicates_found(self, mock_exit, mock_stderr, mock_stdout):
        subdir = os.path.join(self.test_dir, 'subdir')
        os.makedirs(subdir, exist_ok=True)
        content_a = b'duplicate content A'
        with open(os.path.join(self.test_dir, 'dup1.txt'), 'wb') as f: f.write(content_a)
        with open(os.path.join(subdir, 'dup2.txt'), 'wb') as f: f.write(content_a)

        expected_hash_a = hashlib.sha256(content_a).hexdigest()

        with patch('sys.argv', ['src/duster.py', self.test_dir]):
            main()
            # Check that the output contains the expected hash and file paths
            output_calls = [call_arg[0][0] for call_arg in mock_stdout.write.call_args_list]
            self.assertIn(f'Hash: {expected_hash_a}\n', output_calls)
            self.assertIn(f'  - {os.path.join(self.test_dir, 'dup1.txt')}\n', output_calls)
            self.assertIn(f'  - {os.path.join(subdir, 'dup2.txt')}\n', output_calls)
            mock_exit.assert_called_once_with(0)

if __name__ == '__main__':
    unittest.main()
