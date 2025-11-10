import unittest
from unittest.mock import patch, mock_open
import os
import sys
import hashlib

# Mock rationale: We need to simulate file system interactions (walking directories, reading files)
# without actually touching the disk. This ensures tests are deterministic, fast, and offline.
# `os.walk` is mocked to return a predefined directory structure.
# `builtins.open` is mocked to return predefined file contents when files are 'read'.
# `os.path.isdir` is mocked to control directory existence checks.
# `sys.stdout` and `sys.stderr` are mocked to capture printed output for assertion.
# `sys.exit` is mocked to prevent the program from terminating during tests.

# Import the functions to be tested
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from resonator import calculate_file_hash, find_duplicate_files, main
sys.path.pop(0)

class TestResonator(unittest.TestCase):

    def _mock_os_walk(self, mock_walk_data):
        """Helper to set up os.walk mock."""
        return patch('os.walk', return_value=mock_walk_data)

    def _mock_open_files(self, file_contents):
        """Helper to set up mock_open for specific file paths and contents."""
        mock_file_handles = {}
        for path, content in file_contents.items():
            mock_file_handles[path] = mock_open(read_data=content).return_value
        
        def custom_open(filepath, mode='r', *args, **kwargs):
            if filepath in mock_file_handles:
                return mock_file_handles[filepath]
            # Fallback for files not explicitly mocked, or if the test expects an error
            raise FileNotFoundError(f"Mocked open: File not found or not mocked: {filepath}")

        return patch('builtins.open', side_effect=custom_open)

    def test_calculate_file_hash(self):
        # Mock rationale: Test hash calculation in isolation without actual file I/O.
        mock_file_content = b"test content for hashing"
        expected_hash = hashlib.sha256(mock_file_content).hexdigest()

        with self._mock_open_files({'/mock/path/file.txt': mock_file_content}):
            self.assertEqual(calculate_file_hash('/mock/path/file.txt'), expected_hash)

        # Test with empty content
        mock_empty_content = b""
        expected_empty_hash = hashlib.sha256(mock_empty_content).hexdigest()
        with self._mock_open_files({'/mock/path/empty.txt': mock_empty_content}):
            self.assertEqual(calculate_file_hash('/mock/path/empty.txt'), expected_empty_hash)

        # Test file not found (mocked to raise error, which calculate_file_hash catches as IOError)
        with self._mock_open_files({}): # No files mocked, so any open will fail
            self.assertIsNone(calculate_file_hash('/mock/path/nonexistent.txt'))

    def test_find_duplicate_files_no_duplicates(self):
        # Mock rationale: Simulate a directory with unique files to ensure no duplicates are reported.
        mock_walk_data = [
            ('/mock/dir', [], ['file1.txt', 'file2.txt'])
        ]
        mock_file_contents = {
            '/mock/dir/file1.txt': b'content1',
            '/mock/dir/file2.txt': b'content2'
        }
        with patch('os.path.isdir', return_value=True),
             self._mock_os_walk(mock_walk_data),
             self._mock_open_files(mock_file_contents):
            duplicates = find_duplicate_files('/mock/dir')
            self.assertEqual(duplicates, {})

    def test_find_duplicate_files_simple_duplicates(self):
        # Mock rationale: Simulate a directory with two identical files.
        mock_walk_data = [
            ('/mock/dir', [], ['fileA.txt', 'fileB.txt'])
        ]
        mock_file_contents = {
            '/mock/dir/fileA.txt': b'duplicate content',
            '/mock/dir/fileB.txt': b'duplicate content'
        }
        expected_hash = hashlib.sha256(b'duplicate content').hexdigest()
        with patch('os.path.isdir', return_value=True),
             self._mock_os_walk(mock_walk_data),
             self._mock_open_files(mock_file_contents):
            duplicates = find_duplicate_files('/mock/dir')
            self.assertIn(expected_hash, duplicates)
            self.assertCountEqual(duplicates[expected_hash], ['/mock/dir/fileA.txt', '/mock/dir/fileB.txt'])
            self.assertEqual(len(duplicates), 1)

    def test_find_duplicate_files_multiple_groups_and_unique(self):
        # Mock rationale: Simulate a more complex directory with multiple duplicate groups and unique files.
        mock_walk_data = [
            ('/mock/dir', ['subdir1', 'subdir2'], ['unique.txt', 'dup1_a.txt']),
            ('/mock/dir/subdir1', [], ['dup1_b.txt', 'dup2_x.txt']),
            ('/mock/dir/subdir2', [], ['dup2_y.txt', 'another_unique.txt'])
        ]
        mock_file_contents = {
            '/mock/dir/unique.txt': b'unique content',
            '/mock/dir/dup1_a.txt': b'content for group 1',
            '/mock/dir/subdir1/dup1_b.txt': b'content for group 1',
            '/mock/dir/subdir1/dup2_x.txt': b'content for group 2',
            '/mock/dir/subdir2/dup2_y.txt': b'content for group 2',
            '/mock/dir/subdir2/another_unique.txt': b'another unique content'
        }
        hash_group1 = hashlib.sha256(b'content for group 1').hexdigest()
        hash_group2 = hashlib.sha256(b'content for group 2').hexdigest()

        with patch('os.path.isdir', return_value=True),
             self._mock_os_walk(mock_walk_data),
             self._mock_open_files(mock_file_contents):
            duplicates = find_duplicate_files('/mock/dir')
            self.assertEqual(len(duplicates), 2)
            self.assertIn(hash_group1, duplicates)
            self.assertCountEqual(duplicates[hash_group1], ['/mock/dir/dup1_a.txt', '/mock/dir/subdir1/dup1_b.txt'])
            self.assertIn(hash_group2, duplicates)
            self.assertCountEqual(duplicates[hash_group2], ['/mock/dir/subdir1/dup2_x.txt', '/mock/dir/subdir2/dup2_y.txt'])

    def test_find_duplicate_files_empty_directory(self):
        # Mock rationale: Ensure the utility handles an empty directory gracefully.
        mock_walk_data = [
            ('/mock/empty_dir', [], [])
        ]
        with patch('os.path.isdir', return_value=True),
             self._mock_os_walk(mock_walk_data),
             self._mock_open_files({}):
            duplicates = find_duplicate_files('/mock/empty_dir')
            self.assertEqual(duplicates, {})

    def test_find_duplicate_files_non_existent_directory(self):
        # Mock rationale: Ensure the utility handles a non-existent directory gracefully.
        # `os.path.isdir` is mocked to return False for a non-existent directory.
        with patch('os.path.isdir', return_value=False),
             patch('sys.stderr') as mock_stderr:
            duplicates = find_duplicate_files('/mock/nonexistent_dir')
            self.assertEqual(duplicates, {})
            mock_stderr.write.assert_called_with("Error: Directory '/mock/nonexistent_dir' not found.\n")

    @patch('sys.stdout')
    @patch('sys.argv', ['resonator.py', '/mock/dir'])
    def test_main_with_duplicates(self, mock_stdout):
        # Mock rationale: Test the main function's output when duplicates are found.
        # `sys.stdout` is mocked to capture printed output.
        # `sys.argv` is mocked to simulate command-line arguments.
        mock_walk_data = [
            ('/mock/dir', [], ['fileA.txt', 'fileB.txt'])
        ]
        mock_file_contents = {
            '/mock/dir/fileA.txt': b'duplicate content',
            '/mock/dir/fileB.txt': b'duplicate content'
        }
        expected_hash = hashlib.sha256(b'duplicate content').hexdigest()

        with patch('os.path.isdir', return_value=True),
             self._mock_os_walk(mock_walk_data),
             self._mock_open_files(mock_file_contents):
            main()
            output = mock_stdout.write.call_args_list
            output_str = "".join([call.args[0] for call in output])
            self.assertIn("Found 1 groups of duplicate files:", output_str)
            self.assertIn(f"Hash: {expected_hash}", output_str)
            self.assertIn("  - /mock/dir/fileA.txt", output_str)
            self.assertIn("  - /mock/dir/fileB.txt", output_str)

    @patch('sys.stdout')
    @patch('sys.argv', ['resonator.py', '/mock/dir'])
    def test_main_no_duplicates(self, mock_stdout):
        # Mock rationale: Test the main function's output when no duplicates are found.
        mock_walk_data = [
            ('/mock/dir', [], ['file1.txt', 'file2.txt'])
        ]
        mock_file_contents = {
            '/mock/dir/file1.txt': b'content1',
            '/mock/dir/file2.txt': b'content2'
        }
        with patch('os.path.isdir', return_value=True),
             self._mock_os_walk(mock_walk_data),
             self._mock_open_files(mock_file_contents):
            main()
            output = mock_stdout.write.call_args_list
            output_str = "".join([call.args[0] for call in output])
            self.assertIn("No duplicate files found. The echo chamber is silent.", output_str)

    @patch('sys.stderr')
    @patch('sys.exit')
    @patch('sys.argv', ['resonator.py'])
    def test_main_no_arguments(self, mock_exit, mock_stderr):
        # Mock rationale: Test the main function's error handling for missing arguments.
        # `sys.stderr` is mocked to capture error output.
        # `sys.exit` is mocked to prevent the program from actually exiting during the test.
        main()
        mock_stderr.write.assert_called_with("Usage: python src/resonator.py <directory_path>\n")
        mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
