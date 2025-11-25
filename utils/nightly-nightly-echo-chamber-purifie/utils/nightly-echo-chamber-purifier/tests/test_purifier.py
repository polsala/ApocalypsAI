import unittest
import os
import hashlib
from unittest.mock import patch, mock_open

# Import the functions to be tested
from src.purifier import calculate_file_hash, find_duplicate_files, CHUNK_SIZE

class TestPurifier(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_small_file(self, mock_file_open):
        # Mock rationale: We need to simulate reading file content without actual disk I/O.
        # mock_open allows us to control what 'read' returns.
        mock_file_open.return_value.read.side_effect = [b'content', b'']
        expected_hash = hashlib.sha256(b'content').hexdigest()
        self.assertEqual(calculate_file_hash('dummy_path.txt'), expected_hash)

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_large_file(self, mock_file_open):
        # Mock rationale: Simulate a file larger than CHUNK_SIZE to test chunked reading.
        # mock_open's side_effect allows returning multiple chunks.
        large_content = b'a' * (CHUNK_SIZE + 100)
        mock_file_open.return_value.read.side_effect = [
            large_content[:CHUNK_SIZE],
            large_content[CHUNK_SIZE:],
            b''
        ]
        expected_hash = hashlib.sha256(large_content).hexdigest()
        self.assertEqual(calculate_file_hash('large_file.bin'), expected_hash)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize')
    @patch('os.walk')
    def test_find_duplicate_files_basic(self, mock_os_walk, mock_os_getsize, mock_os_isfile, mock_file_open):
        # Mock rationale: Simulate a file system structure and file contents without actual disk I/O.
        # os.walk provides directory structure.
        # os.path.isfile confirms existence.
        # os.path.getsize provides file sizes.
        # mock_open provides file content for hashing.

        # Simulate directory structure:
        # root_dir/
        #   fileA.txt (content1)
        #   subdir/
        #     fileB.txt (content2)
        #     fileC.txt (content1) - duplicate of fileA.txt
        #   fileD.txt (content3)

        mock_os_walk.return_value = [
            ('root_dir', ['subdir'], ['fileA.txt', 'fileD.txt']),
            ('root_dir/subdir', [], ['fileB.txt', 'fileC.txt'])
        ]

        # Map file paths to their content and size
        file_data = {
            'root_dir/fileA.txt': {'content': b'content1', 'size': 10},
            'root_dir/subdir/fileB.txt': {'content': b'content2', 'size': 10},
            'root_dir/subdir/fileC.txt': {'content': b'content1', 'size': 10},
            'root_dir/fileD.txt': {'content': b'content3', 'size': 10},
        }

        def mock_getsize_side_effect(path):
            return file_data.get(path, {'size': 0})['size']

        def mock_open_side_effect(path, mode='r', **kwargs):
            if path in file_data:
                mock_file = mock_open(read_data=file_data[path]['content'])
                return mock_file.return_value
            raise FileNotFoundError

        mock_os_getsize.side_effect = mock_getsize_side_effect
        mock_file_open.side_effect = mock_open_side_effect

        duplicates = find_duplicate_files('root_dir', [], 1)

        content1_hash = hashlib.sha256(b'content1').hexdigest()
        expected_duplicates = {
            content1_hash: [
                'root_dir/fileA.txt',
                'root_dir/subdir/fileC.txt'
            ]
        }

        # Sort paths within lists for consistent comparison
        for h in expected_duplicates:
            expected_duplicates[h].sort()
        for h in duplicates:
            duplicates[h].sort()

        self.assertEqual(duplicates, expected_duplicates)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize')
    @patch('os.walk')
    def test_find_duplicate_files_with_exclusion(self, mock_os_walk, mock_os_getsize, mock_os_isfile, mock_file_open):
        # Mock rationale: Test the exclusion pattern functionality without actual file system interaction.

        mock_os_walk.return_value = [
            ('root_dir', ['temp_dir', 'data_dir'], ['fileA.txt']),
            ('root_dir/temp_dir', [], ['temp_log.txt', 'fileB.txt']),
            ('root_dir/data_dir', [], ['fileC.txt'])
        ]

        file_data = {
            'root_dir/fileA.txt': {'content': b'content1', 'size': 10},
            'root_dir/temp_dir/temp_log.txt': {'content': b'log_content', 'size': 10},
            'root_dir/temp_dir/fileB.txt': {'content': b'content1', 'size': 10},
            'root_dir/data_dir/fileC.txt': {'content': b'content1', 'size': 10},
        }

        def mock_getsize_side_effect(path):
            return file_data.get(path, {'size': 0})['size']

        def mock_open_side_effect(path, mode='r', **kwargs):
            if path in file_data:
                mock_file = mock_open(read_data=file_data[path]['content'])
                return mock_file.return_value
            raise FileNotFoundError

        mock_os_getsize.side_effect = mock_getsize_side_effect
        mock_file_open.side_effect = mock_open_side_effect

        # Exclude temp_dir and any .txt files directly under root_dir
        duplicates = find_duplicate_files('root_dir', ['root_dir/temp_dir/*', 'root_dir/*.txt'], 1)

        # Only fileC.txt should be processed from content1 group, as fileA.txt and fileB.txt are excluded.
        # Since only one file remains, it should not be in the duplicates list.
        expected_duplicates = {}

        self.assertEqual(duplicates, expected_duplicates)

        # Test with exclusion that still leaves duplicates
        mock_os_walk.return_value = [
            ('root_dir', ['subdir1', 'subdir2'], []),
            ('root_dir/subdir1', [], ['fileX.txt', 'fileY.txt']),
            ('root_dir/subdir2', [], ['fileZ.txt'])
        ]
        file_data_2 = {
            'root_dir/subdir1/fileX.txt': {'content': b'shared_content', 'size': 10},
            'root_dir/subdir1/fileY.txt': {'content': b'unique_content', 'size': 10},
            'root_dir/subdir2/fileZ.txt': {'content': b'shared_content', 'size': 10},
        }
        mock_os_getsize.side_effect = lambda p: file_data_2.get(p, {'size': 0})['size']
        mock_file_open.side_effect = lambda p, mode='r', **kwargs: mock_open(read_data=file_data_2[p]['content']).return_value if p in file_data_2 else mock_open().return_value

        # Exclude only fileY.txt
        duplicates_2 = find_duplicate_files('root_dir', ['root_dir/subdir1/fileY.txt'], 1)
        shared_content_hash = hashlib.sha256(b'shared_content').hexdigest()
        expected_duplicates_2 = {
            shared_content_hash: [
                'root_dir/subdir1/fileX.txt',
                'root_dir/subdir2/fileZ.txt'
            ]
        }
        for h in expected_duplicates_2:
            expected_duplicates_2[h].sort()
        for h in duplicates_2:
            duplicates_2[h].sort()

        self.assertEqual(duplicates_2, expected_duplicates_2)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize')
    @patch('os.walk')
    def test_find_duplicate_files_min_size(self, mock_os_walk, mock_os_getsize, mock_os_isfile, mock_file_open):
        # Mock rationale: Test the minimum file size filtering without actual file system interaction.

        mock_os_walk.return_value = [
            ('root_dir', [], ['small_file.txt', 'medium_file.txt', 'large_file.txt'])
        ]

        file_data = {
            'root_dir/small_file.txt': {'content': b's', 'size': 1},
            'root_dir/medium_file.txt': {'content': b'mm', 'size': 2},
            'root_dir/large_file.txt': {'content': b'll', 'size': 2},
        }

        def mock_getsize_side_effect(path):
            return file_data.get(path, {'size': 0})['size']

        def mock_open_side_effect(path, mode='r', **kwargs):
            if path in file_data:
                mock_file = mock_open(read_data=file_data[path]['content'])
                return mock_file.return_value
            raise FileNotFoundError

        mock_os_getsize.side_effect = mock_getsize_side_effect
        mock_file_open.side_effect = mock_open_side_effect

        # Test with min_size = 2
        duplicates = find_duplicate_files('root_dir', [], 2)

        medium_large_hash = hashlib.sha256(b'll').hexdigest() # medium and large have same content 'll'
        expected_duplicates = {
            medium_large_hash: [
                'root_dir/medium_file.txt',
                'root_dir/large_file.txt'
            ]
        }
        for h in expected_duplicates:
            expected_duplicates[h].sort()
        for h in duplicates:
            duplicates[h].sort()

        self.assertEqual(duplicates, expected_duplicates)

        # Test with min_size = 3 (should find no duplicates)
        duplicates_no_match = find_duplicate_files('root_dir', [], 3)
        self.assertEqual(duplicates_no_match, {})

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isfile', return_value=False)
    @patch('os.path.getsize')
    @patch('os.walk')
    def test_find_duplicate_files_non_file_entry(self, mock_os_walk, mock_os_getsize, mock_os_isfile, mock_file_open):
        # Mock rationale: Ensure that non-file entries (e.g., broken symlinks, directories mistakenly listed as files)
        # are correctly skipped by os.path.isfile check.

        mock_os_walk.return_value = [
            ('root_dir', [], ['not_a_file.txt'])
        ]
        # os.path.isfile is patched to return False, simulating a non-file entry

        duplicates = find_duplicate_files('root_dir', [], 1)
        self.assertEqual(duplicates, {})

    @patch('builtins.open', side_effect=IOError('Permission denied'))
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=10)
    @patch('os.walk')
    @patch('builtins.print') # Mock print to avoid actual output during test
    def test_calculate_file_hash_io_error(self, mock_print, mock_os_walk, mock_os_getsize, mock_os_isfile, mock_file_open):
        # Mock rationale: Simulate an IOError during file reading to ensure graceful handling.
        # mock_open raises IOError, and print is mocked to check warning output.

        # Test calculate_file_hash directly
        self.assertEqual(calculate_file_hash('unreadable.txt'), "")
        mock_print.assert_called_with("Warning: Could not read file unreadable.txt - Permission denied")

        # Test find_duplicate_files with an unreadable file
        mock_os_walk.return_value = [
            ('root_dir', [], ['unreadable.txt'])
        ]
        duplicates = find_duplicate_files('root_dir', [], 1)
        self.assertEqual(duplicates, {})
        mock_print.assert_called_with("Warning: Could not read file root_dir/unreadable.txt - Permission denied")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', side_effect=OSError('Access denied'))
    @patch('os.walk')
    @patch('builtins.print') # Mock print to avoid actual output during test
    def test_find_duplicate_files_getsize_error(self, mock_print, mock_os_walk, mock_os_getsize, mock_os_isfile, mock_file_open):
        # Mock rationale: Simulate an OSError during os.path.getsize to ensure graceful handling.
        # os.path.getsize raises OSError, and print is mocked to check warning output.

        mock_os_walk.return_value = [
            ('root_dir', [], ['no_size.txt'])
        ]
        mock_file_open.return_value.read.side_effect = [b'content', b''] # Provide content just in case it gets there

        duplicates = find_duplicate_files('root_dir', [], 1)
        self.assertEqual(duplicates, {})
        mock_print.assert_called_with("Warning: Could not get size for root_dir/no_size.txt - Access denied")
