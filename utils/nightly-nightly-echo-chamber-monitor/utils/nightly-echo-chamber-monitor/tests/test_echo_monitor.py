import unittest
from unittest.mock import patch, mock_open
import os
import hashlib
from collections import defaultdict

# Import the functions to be tested
from src.echo_monitor import calculate_file_hash, find_duplicates, CHUNK_SIZE

class TestEchoMonitor(unittest.TestCase):

    def mock_hash_content(self, content: bytes) -> str:
        """Helper to mock hash calculation for specific content."""
        return hashlib.sha256(content).hexdigest()

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_success(self, mock_file):
        # Mock rationale: We need to simulate reading file content without actual disk I/O.
        # `mock_open` allows us to control what `open()` returns and what `read()` yields.
        mock_file.return_value.read.side_effect = [b'hello world', b'']
        expected_hash = hashlib.sha256(b'hello world').hexdigest()
        self.assertEqual(calculate_file_hash('/fake/path/file.txt'), expected_hash)
        mock_file.assert_called_once_with('/fake/path/file.txt', 'rb')

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_empty_file(self, mock_file):
        # Mock rationale: Test handling of empty files without creating one on disk.
        mock_file.return_value.read.side_effect = [b'']
        expected_hash = hashlib.sha256(b'').hexdigest()
        self.assertEqual(calculate_file_hash('/fake/path/empty.txt'), expected_hash)

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_io_error(self, mock_file):
        # Mock rationale: Simulate a file read error (e.g., permissions) without actual error handling setup.
        mock_file.side_effect = IOError("Permission denied")
        self.assertEqual(calculate_file_hash('/fake/path/unreadable.txt'), "")

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_duplicates_no_duplicates(self, mock_file, mock_walk, mock_isfile, mock_isdir):
        # Mock rationale: Simulate a directory structure and file contents without actual files.
        # `os.walk` is mocked to control directory traversal.
        # `os.path.isfile` ensures our mocked files are treated as files.
        # `builtins.open` is mocked to provide specific content for each file.
        mock_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt'])
        ]
        
        # Map file paths to their content for mock_open
        file_contents = {
            '/root/file1.txt': b'content A',
            '/root/file2.txt': b'content B'
        }

        def mock_open_side_effect(filepath, mode):
            if mode == 'rb' and filepath in file_contents:
                m = mock_open(read_data=file_contents[filepath])
                return m.return_value
            raise FileNotFoundError(f"Mock file not found: {filepath}")

        mock_file.side_effect = mock_open_side_effect

        duplicates = find_duplicates('/root')
        self.assertEqual(duplicates, {})

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_duplicates_two_identical_files(self, mock_file, mock_walk, mock_isfile, mock_isdir):
        # Mock rationale: Simulate two files with identical content in different locations.
        mock_walk.return_value = [
            ('/root', ['subdir'], ['fileA.txt']),
            ('/root/subdir', [], ['fileB.txt'])
        ]

        common_content = b'identical content'
        hash_common = self.mock_hash_content(common_content)

        file_contents = {
            '/root/fileA.txt': common_content,
            '/root/subdir/fileB.txt': common_content
        }

        def mock_open_side_effect(filepath, mode):
            if mode == 'rb' and filepath in file_contents:
                m = mock_open(read_data=file_contents[filepath])
                return m.return_value
            raise FileNotFoundError(f"Mock file not found: {filepath}")

        mock_file.side_effect = mock_open_side_effect

        duplicates = find_duplicates('/root')
        expected_duplicates = {
            hash_common: ['/root/fileA.txt', '/root/subdir/fileB.txt']
        }
        self.assertEqual(duplicates, expected_duplicates)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_duplicates_multiple_groups(self, mock_file, mock_walk, mock_isfile, mock_isdir):
        # Mock rationale: Simulate multiple sets of duplicate files.
        mock_walk.return_value = [
            ('/root', [], ['f1.txt', 'f2.txt', 'f3.txt', 'f4.txt'])
        ]

        content_a = b'content A'
        content_b = b'content B'
        hash_a = self.mock_hash_content(content_a)
        hash_b = self.mock_hash_content(content_b)

        file_contents = {
            '/root/f1.txt': content_a,
            '/root/f2.txt': content_b,
            '/root/f3.txt': content_a,
            '/root/f4.txt': content_b
        }

        def mock_open_side_effect(filepath, mode):
            if mode == 'rb' and filepath in file_contents:
                m = mock_open(read_data=file_contents[filepath])
                return m.return_value
            raise FileNotFoundError(f"Mock file not found: {filepath}")

        mock_file.side_effect = mock_open_side_effect

        duplicates = find_duplicates('/root')
        expected_duplicates = {
            hash_a: ['/root/f1.txt', '/root/f3.txt'],
            hash_b: ['/root/f2.txt', '/root/f4.txt']
        }
        # Use assertDictEqual for dictionaries, order of lists might vary but content should be same
        for h, paths in duplicates.items():
            self.assertIn(h, expected_duplicates)
            self.assertCountEqual(paths, expected_duplicates[h])
        self.assertEqual(len(duplicates), len(expected_duplicates))

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_duplicates_different_content_same_size(self, mock_file, mock_walk, mock_isfile, mock_isdir):
        # Mock rationale: Ensure files with same size but different content are not flagged as duplicates.
        mock_walk.return_value = [
            ('/root', [], ['fileX.txt', 'fileY.txt'])
        ]

        file_contents = {
            '/root/fileX.txt': b'AAAAA',
            '/root/fileY.txt': b'BBBBB'
        }

        def mock_open_side_effect(filepath, mode):
            if mode == 'rb' and filepath in file_contents:
                m = mock_open(read_data=file_contents[filepath])
                return m.return_value
            raise FileNotFoundError(f"Mock file not found: {filepath}")

        mock_file.side_effect = mock_open_side_effect

        duplicates = find_duplicates('/root')
        self.assertEqual(duplicates, {})

    @patch('os.path.isdir', return_value=False)
    def test_find_duplicates_invalid_directory(self, mock_isdir):
        # Mock rationale: Test the error handling for non-existent or invalid directories.
        with self.assertRaisesRegex(ValueError, "Directory not found or is not a directory"):
            find_duplicates('/nonexistent')

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_duplicates_empty_files(self, mock_file, mock_walk, mock_isfile, mock_isdir):
        # Mock rationale: Test that multiple empty files are correctly identified as duplicates.
        mock_walk.return_value = [
            ('/root', [], ['empty1.txt', 'empty2.txt', 'non_empty.txt'])
        ]

        empty_content = b''
        non_empty_content = b'some content'
        hash_empty = self.mock_hash_content(empty_content)

        file_contents = {
            '/root/empty1.txt': empty_content,
            '/root/empty2.txt': empty_content,
            '/root/non_empty.txt': non_empty_content
        }

        def mock_open_side_effect(filepath, mode):
            if mode == 'rb' and filepath in file_contents:
                m = mock_open(read_data=file_contents[filepath])
                return m.return_value
            raise FileNotFoundError(f"Mock file not found: {filepath}")

        mock_file.side_effect = mock_open_side_effect

        duplicates = find_duplicates('/root')
        expected_duplicates = {
            hash_empty: ['/root/empty1.txt', '/root/empty2.txt']
        }
        self.assertIn(hash_empty, duplicates)
        self.assertCountEqual(duplicates[hash_empty], expected_duplicates[hash_empty])
        self.assertEqual(len(duplicates), 1)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_duplicates_io_error_on_file(self, mock_file, mock_walk, mock_isfile, mock_isdir):
        # Mock rationale: Simulate a scenario where one file cannot be read, but others can.
        # This ensures the utility continues processing other files.
        mock_walk.return_value = [
            ('/root', [], ['good_file.txt', 'bad_file.txt', 'another_good.txt'])
        ]

        content_good = b'good content'
        hash_good = self.mock_hash_content(content_good)

        file_contents = {
            '/root/good_file.txt': content_good,
            '/root/another_good.txt': content_good
        }

        def mock_open_side_effect(filepath, mode):
            if mode == 'rb':
                if filepath == '/root/bad_file.txt':
                    raise IOError("Permission denied")
                elif filepath in file_contents:
                    m = mock_open(read_data=file_contents[filepath])
                    return m.return_value
            raise FileNotFoundError(f"Mock file not found: {filepath}")

        mock_file.side_effect = mock_open_side_effect

        duplicates = find_duplicates('/root')
        expected_duplicates = {
            hash_good: ['/root/good_file.txt', '/root/another_good.txt']
        }
        self.assertIn(hash_good, duplicates)
        self.assertCountEqual(duplicates[hash_good], expected_duplicates[hash_good])
        self.assertEqual(len(duplicates), 1)

if __name__ == '__main__':
    unittest.main()
