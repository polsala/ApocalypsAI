import unittest
import os
import hashlib
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
import tempfile
import shutil

# Import the functions to be tested
from src.cleaner import find_old_files, find_duplicate_files, get_file_hash

class TestCosmicCacheCleaner(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing file operations
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory after tests
        shutil.rmtree(self.test_dir)

    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_old_files(self, mock_os_walk, mock_getmtime):
        # Mock rationale: We need to control the file system structure and modification times
        # without actually creating many files or relying on real system time. This ensures
        # deterministic and offline testing.
        # os.walk is mocked to provide a consistent directory structure.
        # os.path.getmtime is mocked to return specific timestamps for files.

        # Define a mock directory structure
        mock_os_walk.return_value = [
            (self.test_dir, [], ['file1.txt', 'file2.txt']),
            (os.path.join(self.test_dir, 'subdir'), [], ['file3.log'])
        ]

        # Define mock modification times
        now = datetime.now()
        old_date = (now - timedelta(days=100)).timestamp() # Older than 90 days
        recent_date = (now - timedelta(days=50)).timestamp() # Not older than 90 days

        # Map file paths to their mock modification times
        mock_getmtime.side_effect = {
            os.path.join(self.test_dir, 'file1.txt'): old_date,
            os.path.join(self.test_dir, 'file2.txt'): recent_date,
            os.path.join(self.test_dir, 'subdir', 'file3.log'): old_date,
        }.get

        # Test with default 90 days
        old_files = find_old_files(self.test_dir, 90)
        expected_old_files = [
            os.path.join(self.test_dir, 'file1.txt'),
            os.path.join(self.test_dir, 'subdir', 'file3.log')
        ]
        self.assertCountEqual(old_files, expected_old_files)

        # Test with a different threshold (e.g., 60 days)
        old_files_60_days = find_old_files(self.test_dir, 60)
        expected_old_files_60_days = [
            os.path.join(self.test_dir, 'file1.txt'),
            os.path.join(self.test_dir, 'subdir', 'file3.log')
        ]
        self.assertCountEqual(old_files_60_days, expected_old_files_60_days)

        # Test with a threshold that makes 'file2.txt' old
        old_date_for_file2 = (now - timedelta(days=100)).timestamp()
        mock_getmtime.side_effect = {
            os.path.join(self.test_dir, 'file1.txt'): old_date,
            os.path.join(self.test_dir, 'file2.txt'): old_date_for_file2, # Now old
            os.path.join(self.test_dir, 'subdir', 'file3.log'): old_date,
        }.get
        old_files_all_old = find_old_files(self.test_dir, 90)
        expected_old_files_all_old = [
            os.path.join(self.test_dir, 'file1.txt'),
            os.path.join(self.test_dir, 'file2.txt'),
            os.path.join(self.test_dir, 'subdir', 'file3.log')
        ]
        self.assertCountEqual(old_files_all_old, expected_old_files_all_old)

    @patch('src.cleaner.get_file_hash')
    @patch('os.walk')
    def test_find_duplicate_files(self, mock_os_walk, mock_get_file_hash):
        # Mock rationale: We need to control the file system structure and the hashes
        # returned for each file without actually creating files or computing hashes.
        # This ensures deterministic and offline testing.
        # os.walk is mocked to provide a consistent directory structure.
        # get_file_hash is mocked to return specific hash values for files.

        # Define a mock directory structure
        mock_os_walk.return_value = [
            (self.test_dir, [], ['fileA.txt', 'fileB.txt', 'fileC.txt']),
            (os.path.join(self.test_dir, 'sub'), [], ['fileD.txt', 'fileE.txt'])
        ]

        # Define mock hashes
        hash1 = 'hash_content_1'
        hash2 = 'hash_content_2'
        hash3 = 'hash_content_3'

        # Map file paths to their mock hashes
        mock_get_file_hash.side_effect = {
            os.path.join(self.test_dir, 'fileA.txt'): hash1,
            os.path.join(self.test_dir, 'fileB.txt'): hash2,
            os.path.join(self.test_dir, 'fileC.txt'): hash1, # Duplicate of fileA
            os.path.join(self.test_dir, 'sub', 'fileD.txt'): hash3,
            os.path.join(self.test_dir, 'sub', 'fileE.txt'): hash2, # Duplicate of fileB
        }.get

        duplicate_groups = find_duplicate_files(self.test_dir)

        # Expected groups of duplicates
        expected_duplicate_groups = [
            [os.path.join(self.test_dir, 'fileA.txt'), os.path.join(self.test_dir, 'fileC.txt')],
            [os.path.join(self.test_dir, 'fileB.txt'), os.path.join(self.test_dir, 'sub', 'fileE.txt')]
        ]

        # Sort inner lists for consistent comparison, as order within groups doesn't matter
        sorted_actual = [sorted(group) for group in duplicate_groups]
        sorted_expected = [sorted(group) for group in expected_duplicate_groups]

        # Compare the sets of sorted groups (order of groups doesn't matter)
        self.assertCountEqual(sorted_actual, sorted_expected)

    def test_get_file_hash(self):
        # Mock rationale: We need to ensure the hashing function works correctly
        # with file-like objects without actually touching the disk for real files
        # in all scenarios. Using tempfile for one case and mock_open for another
        # provides comprehensive, deterministic, and offline testing.

        # Test with an actual file created in the temporary directory
        test_file_path = os.path.join(self.test_dir, 'dummy.txt')
        content = b'test content'
        with open(test_file_path, 'wb') as f:
            f.write(content)

        expected_hash = hashlib.md5(content).hexdigest()
        actual_hash = get_file_hash(test_file_path)
        self.assertEqual(actual_hash, expected_hash)

        # Test with mock_open for a different content, ensuring file operations are mocked
        mock_file_content = b'another content for hashing'
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open:
            mocked_hash = get_file_hash('mock_path.txt')
            self.assertEqual(mocked_hash, hashlib.md5(mock_file_content).hexdigest())
            m_open.assert_called_once_with('mock_path.txt', 'rb')

        # Test handling of inaccessible file (get_file_hash should return None)
        with patch('builtins.open', side_effect=IOError) as m_open_fail:
            failed_hash = get_file_hash('non_existent_path.txt')
            self.assertIsNone(failed_hash)
            m_open_fail.assert_called_once_with('non_existent_path.txt', 'rb')
