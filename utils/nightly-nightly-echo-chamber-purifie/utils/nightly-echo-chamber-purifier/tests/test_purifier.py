import unittest
import os
import hashlib
from unittest.mock import patch, mock_open
from collections import defaultdict

# Import the functions to be tested
from src.purifier import calculate_file_hash, find_duplicates

class TestPurifier(unittest.TestCase):

    # Mock rationale: We need to simulate file system access (os.walk, open)
    # without actually creating files or directories on the disk. This ensures
    # tests are deterministic, fast, and don't leave artifacts.

    def _mock_os_walk(self, test_files_structure):
        """
        Helper to mock os.walk.
        test_files_structure: A dictionary mapping directory paths to a tuple
                              (dirs_in_root, files_in_root).
        Example:
        {
            '/mock/dir': (['subdir'], ['file1.txt', 'file2.txt']),
            '/mock/dir/subdir': ([], ['subfile.txt'])
        }
        """
        def walk_mock(top):
            if top in test_files_structure:
                dirs, files = test_files_structure[top]
                yield top, dirs, files
                for d in dirs:
                    yield from walk_mock(os.path.join(top, d))
            else:
                yield top, [], [] # Empty directory if not in structure
        return walk_mock

    def _mock_file_content(self, file_contents_map):
        """
        Helper to mock builtins.open.
        file_contents_map: A dictionary mapping file paths to their content.
        Example:
        {
            '/mock/dir/file1.txt': b'content A',
            '/mock/dir/file2.txt': b'content B'
        }
        """
        def mock_open_func(filename, mode='r', **kwargs):
            if 'b' in mode:
                content = file_contents_map.get(filename, b'')
            else:
                content = file_contents_map.get(filename, '').decode('utf-8')
            m = mock_open(read_data=content)
            return m()
        return mock_open_func

    def test_calculate_file_hash(self):
        # Mock rationale: Simulate reading a file's content to get a hash
        # without actual disk I/O.
        mock_file_path = "/mock/path/to/file.txt"
        mock_content = b"This is some test content."
        expected_hash = hashlib.sha256(mock_content).hexdigest()

        with patch('builtins.open', self._mock_file_content({mock_file_path: mock_content})):
            self.assertEqual(calculate_file_hash(mock_file_path), expected_hash)

        # Test with empty content
        mock_empty_path = "/mock/path/to/empty.txt"
        mock_empty_content = b""
        expected_empty_hash = hashlib.sha256(mock_empty_content).hexdigest()
        with patch('builtins.open', self._mock_file_content({mock_empty_path: mock_empty_content})):
            self.assertEqual(calculate_file_hash(mock_empty_path), expected_empty_hash)

        # Test with file not found
        with patch('builtins.open', side_effect=FileNotFoundError):
            # Suppress print output for cleaner test results
            with patch('builtins.print'):
                self.assertEqual(calculate_file_hash("/nonexistent/file.txt"), "")

    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume the base directory exists
    def test_no_duplicates(self, mock_isdir):
        # Mock rationale: Simulate a directory structure where all files have unique content.
        mock_dir = "/mock/repo"
        mock_files_structure = {
            mock_dir: ([], ['file1.txt', 'file2.txt', 'file3.txt'])
        }
        mock_file_contents = {
            os.path.join(mock_dir, 'file1.txt'): b'content A',
            os.path.join(mock_dir, 'file2.txt'): b'content B',
            os.path.join(mock_dir, 'file3.txt'): b'content C',
        }

        with patch('os.walk', self._mock_os_walk(mock_files_structure)), \
             patch('builtins.open', self._mock_file_content(mock_file_contents)):
            duplicates = find_duplicates(mock_dir)
            self.assertEqual(len(duplicates), 0)

    @patch('os.path.isdir', return_value=True)
    def test_simple_duplicates(self, mock_isdir):
        # Mock rationale: Simulate a directory with two files having identical content.
        mock_dir = "/mock/repo"
        mock_files_structure = {
            mock_dir: ([], ['file1.txt', 'file2.txt', 'unique.txt'])
        }
        mock_file_contents = {
            os.path.join(mock_dir, 'file1.txt'): b'duplicate content',
            os.path.join(mock_dir, 'file2.txt'): b'duplicate content',
            os.path.join(mock_dir, 'unique.txt'): b'unique content',
        }

        with patch('os.walk', self._mock_os_walk(mock_files_structure)), \
             patch('builtins.open', self._mock_file_content(mock_file_contents)):
            duplicates = find_duplicates(mock_dir)
            self.assertEqual(len(duplicates), 1)
            duplicate_hash = hashlib.sha256(b'duplicate content').hexdigest()
            self.assertIn(duplicate_hash, duplicates)
            self.assertCountEqual(
                duplicates[duplicate_hash],
                [os.path.join(mock_dir, 'file1.txt'), os.path.join(mock_dir, 'file2.txt')]
            )

    @patch('os.path.isdir', return_value=True)
    def test_duplicates_in_subdirectories(self, mock_isdir):
        # Mock rationale: Simulate a more complex directory structure with duplicates
        # across different subdirectories.
        mock_dir = "/mock/repo"
        mock_files_structure = {
            mock_dir: (['subdir1', 'subdir2'], ['root_file.txt']),
            os.path.join(mock_dir, 'subdir1'): ([], ['sub1_file.txt', 'common.txt']),
            os.path.join(mock_dir, 'subdir2'): ([], ['sub2_file.txt', 'common.txt']),
        }
        mock_file_contents = {
            os.path.join(mock_dir, 'root_file.txt'): b'unique root',
            os.path.join(mock_dir, 'subdir1', 'sub1_file.txt'): b'unique sub1',
            os.path.join(mock_dir, 'subdir2', 'sub2_file.txt'): b'unique sub2',
            os.path.join(mock_dir, 'subdir1', 'common.txt'): b'shared content',
            os.path.join(mock_dir, 'subdir2', 'common.txt'): b'shared content',
        }

        with patch('os.walk', self._mock_os_walk(mock_files_structure)), \
             patch('builtins.open', self._mock_file_content(mock_file_contents)):
            duplicates = find_duplicates(mock_dir)
            self.assertEqual(len(duplicates), 1)
            duplicate_hash = hashlib.sha256(b'shared content').hexdigest()
            self.assertIn(duplicate_hash, duplicates)
            self.assertCountEqual(
                duplicates[duplicate_hash],
                [
                    os.path.join(mock_dir, 'subdir1', 'common.txt'),
                    os.path.join(mock_dir, 'subdir2', 'common.txt')
                ]
            )

    @patch('os.path.isdir', return_value=True)
    def test_empty_files_are_duplicates(self, mock_isdir):
        # Mock rationale: Ensure that multiple empty files are correctly identified as duplicates.
        mock_dir = "/mock/repo"
        mock_files_structure = {
            mock_dir: ([], ['empty1.txt', 'empty2.txt', 'non_empty.txt'])
        }
        mock_file_contents = {
            os.path.join(mock_dir, 'empty1.txt'): b'',
            os.path.join(mock_dir, 'empty2.txt'): b'',
            os.path.join(mock_dir, 'non_empty.txt'): b'some content',
        }

        with patch('os.walk', self._mock_os_walk(mock_files_structure)), \
             patch('builtins.open', self._mock_file_content(mock_file_contents)):
            duplicates = find_duplicates(mock_dir)
            self.assertEqual(len(duplicates), 1)
            empty_hash = hashlib.sha256(b'').hexdigest()
            self.assertIn(empty_hash, duplicates)
            self.assertCountEqual(
                duplicates[empty_hash],
                [os.path.join(mock_dir, 'empty1.txt'), os.path.join(mock_dir, 'empty2.txt')]
            )

    @patch('os.path.isdir', return_value=False) # Mock rationale: Simulate a non-existent directory
    def test_invalid_directory(self, mock_isdir):
        # Suppress print output for cleaner test results
        with patch('builtins.print'):
            duplicates = find_duplicates("/nonexistent/dir")
            self.assertEqual(len(duplicates), 0)
            self.assertEqual(duplicates, {})

    @patch('os.path.isdir', return_value=True)
    def test_empty_directory(self, mock_isdir):
        # Mock rationale: Simulate an empty directory.
        mock_dir = "/mock/empty_repo"
        mock_files_structure = {
            mock_dir: ([], [])
        }
        mock_file_contents = {} # No files to read

        with patch('os.walk', self._mock_os_walk(mock_files_structure)), \
             patch('builtins.open', self._mock_file_content(mock_file_contents)):
            duplicates = find_duplicates(mock_dir)
            self.assertEqual(len(duplicates), 0)

if __name__ == '__main__':
    unittest.main()
