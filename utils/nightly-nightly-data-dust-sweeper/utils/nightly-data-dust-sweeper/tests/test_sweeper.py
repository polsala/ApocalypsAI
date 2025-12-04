import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import hashlib
from src.sweeper import find_duplicate_files, calculate_file_hash

# Mock rationale: We need to simulate file system operations (existence, size, content, directory traversal)
# without actually touching the disk, ensuring deterministic and offline tests.

class TestDataDustSweeper(unittest.TestCase):

    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('os.path.isfile', MagicMock(return_value=True))
    def test_calculate_file_hash_md5(self):
        # Mock rationale: Simulate file content for hashing without actual file I/O.
        mock_file_content = b"test content"
        expected_hash = hashlib.md5(mock_file_content).hexdigest()
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            self.assertEqual(calculate_file_hash("dummy_path.txt", 'md5'), expected_hash)

    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('os.path.isfile', MagicMock(return_value=True))
    def test_calculate_file_hash_sha256(self):
        # Mock rationale: Simulate file content for hashing without actual file I/O.
        mock_file_content = b"another test content"
        expected_hash = hashlib.sha256(mock_file_content).hexdigest()
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            self.assertEqual(calculate_file_hash("dummy_path.txt", 'sha256'), expected_hash)

    @patch('os.path.exists', MagicMock(return_value=False))
    @patch('os.path.isfile', MagicMock(return_value=False))
    def test_calculate_file_hash_non_existent_file(self):
        # Mock rationale: Test behavior when file does not exist.
        self.assertIsNone(calculate_file_hash("non_existent.txt"))

    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('os.path.isfile', MagicMock(return_value=True))
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    def test_find_duplicate_files_no_duplicates(self, mock_walk, mock_open_func, mock_getsize):
        # Mock rationale: Simulate a file system with unique files.
        # os.walk will return a single directory with unique files.
        mock_walk.return_value = [
            ('/dir1', [], ['fileA.txt', 'fileB.txt', 'fileC.txt'])
        ]
        # os.path.getsize will return unique sizes.
        mock_getsize.side_effect = lambda x: {
            '/dir1/fileA.txt': 100,
            '/dir1/fileB.txt': 200,
            '/dir1/fileC.txt': 300,
        }.get(x, 0)
        # builtins.open will return unique content for each file.
        file_contents = {
            '/dir1/fileA.txt': b'contentA',
            '/dir1/fileB.txt': b'contentB',
            '/dir1/fileC.txt': b'contentC',
        }
        mock_open_func.side_effect = lambda f, mode: mock_open(read_data=file_contents.get(f, b'')).return_value

        # os.path.isfile and os.path.exists need to be mocked for each path
        with patch('os.path.isfile', side_effect=lambda x: x in ['/dir1/fileA.txt', '/dir1/fileB.txt', '/dir1/fileC.txt']), \
             patch('os.path.exists', side_effect=lambda x: x in ['/dir1', '/dir1/fileA.txt', '/dir1/fileB.txt', '/dir1/fileC.txt']):
            duplicates = find_duplicate_files(['/dir1'])
            self.assertEqual(duplicates, {})

    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('os.path.isfile', MagicMock(return_value=True))
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    def test_find_duplicate_files_with_duplicates(self, mock_walk, mock_open_func, mock_getsize):
        # Mock rationale: Simulate a file system with duplicate files.
        # os.walk will return a single directory with some duplicate files.
        mock_walk.return_value = [
            ('/dir1', [], ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt'])
        ]
        # os.path.getsize will return sizes, with file1 and file2 having the same size.
        mock_getsize.side_effect = lambda x: {
            '/dir1/file1.txt': 100,
            '/dir1/file2.txt': 100,
            '/dir1/file3.txt': 200,
            '/dir1/file4.txt': 100, # Another file with size 100
        }.get(x, 0)

        # Mock file content: file1 and file2 have the same content, file4 has different content.
        file_contents = {
            '/dir1/file1.txt': b"duplicate content A",
            '/dir1/file2.txt': b"duplicate content A",
            '/dir1/file3.txt': b"unique content B",
            '/dir1/file4.txt': b"unique content C",
        }
        mock_open_func.side_effect = lambda f, mode: mock_open(read_data=file_contents.get(f, b'')).return_value

        # os.path.isfile and os.path.exists need to be mocked for each path
        all_paths = ['/dir1', '/dir1/file1.txt', '/dir1/file2.txt', '/dir1/file3.txt', '/dir1/file4.txt']
        with patch('os.path.isfile', side_effect=lambda x: x in all_paths and x != '/dir1'), \
             patch('os.path.exists', side_effect=lambda x: x in all_paths):
            duplicates = find_duplicate_files(['/dir1'])

            expected_hash = hashlib.md5(b"duplicate content A").hexdigest()
            self.assertIn(expected_hash, duplicates)
            self.assertCountEqual(duplicates[expected_hash], ['/dir1/file1.txt', '/dir1/file2.txt'])
            self.assertEqual(len(duplicates), 1) # Only one set of duplicates

    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('os.path.isfile', MagicMock(return_value=True))
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    def test_find_duplicate_files_empty_files(self, mock_walk, mock_open_func, mock_getsize):
        # Mock rationale: Simulate a file system with empty files.
        mock_walk.return_value = [
            ('/dir1', [], ['empty1.txt', 'empty2.txt', 'non_empty.txt'])
        ]
        mock_getsize.side_effect = lambda x: {
            '/dir1/empty1.txt': 0,
            '/dir1/empty2.txt': 0,
            '/dir1/non_empty.txt': 50,
        }.get(x, 0)
        file_contents = {
            '/dir1/empty1.txt': b"",
            '/dir1/empty2.txt': b"",
            '/dir1/non_empty.txt': b"some content",
        }
        mock_open_func.side_effect = lambda f, mode: mock_open(read_data=file_contents.get(f, b'')).return_value

        all_paths = ['/dir1', '/dir1/empty1.txt', '/dir1/empty2.txt', '/dir1/non_empty.txt']
        with patch('os.path.isfile', side_effect=lambda x: x in all_paths and x != '/dir1'), \
             patch('os.path.exists', side_effect=lambda x: x in all_paths):
            duplicates = find_duplicate_files(['/dir1'])
            
            # For 0-byte files, the hash is consistent (md5 of empty string is d41d8cd98f00b204e9800998ecf8427e)
            expected_hash_empty = hashlib.md5(b"").hexdigest()
            self.assertIn(expected_hash_empty, duplicates)
            self.assertCountEqual(duplicates[expected_hash_empty], ['/dir1/empty1.txt', '/dir1/empty2.txt'])
            self.assertEqual(len(duplicates), 1)

    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('os.path.isfile', MagicMock(return_value=True))
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    def test_find_duplicate_files_multiple_directories(self, mock_walk, mock_open_func, mock_getsize):
        # Mock rationale: Simulate scanning multiple root directories.
        mock_walk.side_effect = [
            [('/dirA', [], ['file1.txt', 'file2.txt'])],
            [('/dirB', [], ['file3.txt', 'file4.txt'])]
        ]
        mock_getsize.side_effect = lambda x: {
            '/dirA/file1.txt': 100,
            '/dirA/file2.txt': 200,
            '/dirB/file3.txt': 100, # Duplicate of file1.txt
            '/dirB/file4.txt': 300,
        }.get(x, 0)
        file_contents = {
            '/dirA/file1.txt': b"content X",
            '/dirA/file2.txt': b"content Y",
            '/dirB/file3.txt': b"content X", # Same content as file1.txt
            '/dirB/file4.txt': b"content Z",
        }
        mock_open_func.side_effect = lambda f, mode: mock_open(read_data=file_contents.get(f, b'')).return_value

        all_paths = [
            '/dirA', '/dirA/file1.txt', '/dirA/file2.txt',
            '/dirB', '/dirB/file3.txt', '/dirB/file4.txt'
        ]
        with patch('os.path.isfile', side_effect=lambda x: x in all_paths and x not in ['/dirA', '/dirB']), \
             patch('os.path.exists', side_effect=lambda x: x in all_paths):
            duplicates = find_duplicate_files(['/dirA', '/dirB'])

            expected_hash = hashlib.md5(b"content X").hexdigest()
            self.assertIn(expected_hash, duplicates)
            self.assertCountEqual(duplicates[expected_hash], ['/dirA/file1.txt', '/dirB/file3.txt'])
            self.assertEqual(len(duplicates), 1)

    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('os.path.isfile', MagicMock(return_value=True))
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    def test_find_duplicate_files_with_single_file_path(self, mock_walk, mock_open_func, mock_getsize):
        # Mock rationale: Test scanning a single file path directly.
        # os.walk should not be called if only file paths are provided.
        mock_walk.return_value = [] # Ensure os.walk is not used for file paths
        mock_getsize.side_effect = lambda x: {
            '/file1.txt': 100,
            '/file2.txt': 100,
        }.get(x, 0)
        file_contents = {
            '/file1.txt': b"content A",
            '/file2.txt': b"content A",
        }
        mock_open_func.side_effect = lambda f, mode: mock_open(read_data=file_contents.get(f, b'')).return_value

        all_paths = ['/file1.txt', '/file2.txt']
        with patch('os.path.isfile', side_effect=lambda x: x in all_paths), \
             patch('os.path.exists', side_effect=lambda x: x in all_paths):
            duplicates = find_duplicate_files(['/file1.txt', '/file2.txt'])

            expected_hash = hashlib.md5(b"content A").hexdigest()
            self.assertIn(expected_hash, duplicates)
            self.assertCountEqual(duplicates[expected_hash], ['/file1.txt', '/file2.txt'])
            self.assertEqual(len(duplicates), 1)
            mock_walk.assert_not_called() # Verify os.walk was not used for file paths

    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('os.path.isfile', MagicMock(return_value=True))
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    def test_find_duplicate_files_mixed_paths(self, mock_walk, mock_open_func, mock_getsize):
        # Mock rationale: Test scanning a mix of directory and file paths.
        mock_walk.return_value = [
            ('/dir1', [], ['dir_file1.txt'])
        ]
        mock_getsize.side_effect = lambda x: {
            '/dir1/dir_file1.txt': 100,
            '/standalone_file.txt': 100,
        }.get(x, 0)
        file_contents = {
            '/dir1/dir_file1.txt': b"mixed content",
            '/standalone_file.txt': b"mixed content",
        }
        mock_open_func.side_effect = lambda f, mode: mock_open(read_data=file_contents.get(f, b'')).return_value

        all_paths = ['/dir1', '/dir1/dir_file1.txt', '/standalone_file.txt']
        with patch('os.path.isfile', side_effect=lambda x: x in all_paths and x != '/dir1'), \
             patch('os.path.exists', side_effect=lambda x: x in all_paths):
            duplicates = find_duplicate_files(['/dir1', '/standalone_file.txt'])

            expected_hash = hashlib.md5(b"mixed content").hexdigest()
            self.assertIn(expected_hash, duplicates)
            self.assertCountEqual(duplicates[expected_hash], ['/dir1/dir_file1.txt', '/standalone_file.txt'])
            self.assertEqual(len(duplicates), 1)
            mock_walk.assert_called_once_with('/dir1') # Verify os.walk was only called for the directory

    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('os.path.isfile', MagicMock(return_value=True))
    @patch('os.path.getsize', MagicMock(side_effect=OSError("Permission denied")))
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    def test_find_duplicate_files_permission_error_getsize(self, mock_walk, mock_open_func):
        # Mock rationale: Test robustness against permission errors during size retrieval.
        mock_walk.return_value = [
            ('/dir1', [], ['file1.txt'])
        ]
        # os.path.getsize is mocked to raise OSError
        file_contents = {
            '/dir1/file1.txt': b"content",
        }
        mock_open_func.side_effect = lambda f, mode: mock_open(read_data=file_contents.get(f, b'')).return_value

        all_paths = ['/dir1', '/dir1/file1.txt']
        with patch('os.path.isfile', side_effect=lambda x: x in all_paths and x != '/dir1'), \
             patch('os.path.exists', side_effect=lambda x: x in all_paths):
            duplicates = find_duplicate_files(['/dir1'])
            self.assertEqual(duplicates, {}) # No files should be processed if size cannot be obtained

    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('os.path.isfile', MagicMock(return_value=True))
    @patch('os.path.getsize', MagicMock(return_value=100))
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    def test_find_duplicate_files_permission_error_open(self, mock_walk, mock_open_func):
        # Mock rationale: Test robustness against permission errors during file opening for hashing.
        mock_walk.return_value = [
            ('/dir1', [], ['file1.txt', 'file2.txt'])
        ]
        # os.path.getsize returns a valid size
        # builtins.open is mocked to raise IOError for file1.txt
        def open_side_effect(f, mode):
            if f == '/dir1/file1.txt':
                raise IOError("Permission denied")
            return mock_open(read_data=b"content").return_value

        mock_open_func.side_effect = open_side_effect

        all_paths = ['/dir1', '/dir1/file1.txt', '/dir1/file2.txt']
        with patch('os.path.isfile', side_effect=lambda x: x in all_paths and x != '/dir1'), \
             patch('os.path.exists', side_effect=lambda x: x in all_paths):
            duplicates = find_duplicate_files(['/dir1'])
            self.assertEqual(duplicates, {}) # file1 fails, file2 is unique, so no duplicates reported.
