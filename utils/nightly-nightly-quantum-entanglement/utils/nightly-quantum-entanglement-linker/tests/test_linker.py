import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import hashlib
from collections import defaultdict

# Import the functions to be tested
from src.linker import calculate_file_hash, find_duplicate_files, link_duplicates

class TestQuantumEntanglementLinker(unittest.TestCase):

    # Mock rationale: We need to simulate file content for hashing without actual disk I/O.
    # mock_open allows us to control what `open()` returns when reading.
    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    def test_calculate_file_hash(self, mock_file):
        test_path = "/fake/path/to/file.txt"
        expected_hash = hashlib.sha256(b'test content').hexdigest()
        self.assertEqual(calculate_file_hash(test_path), expected_hash)
        mock_file.assert_called_once_with(test_path, 'rb')

    # Mock rationale: Simulate a file that cannot be opened to test error handling.
    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_calculate_file_hash_io_error(self, mock_file):
        test_path = "/fake/path/to/unreadable.txt"
        self.assertIsNone(calculate_file_hash(test_path))
        mock_file.assert_called_once_with(test_path, 'rb')

    # Mock rationale: Simulate directory traversal and file properties without actual filesystem.
    # os.walk is mocked to return a predefined directory structure.
    # os.path.getsize is mocked to return specific sizes for files.
    # builtins.open is mocked to provide content for hashing.
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.islink', return_value=False) # Mock rationale: Ensure symlinks are not processed
    def test_find_duplicate_files(self, mock_islink, mock_file_open, mock_getsize, mock_walk):
        # Setup mock os.walk to simulate a directory structure
        mock_walk.return_value = [
            ('/root', ('dir1', 'dir2'), ('fileA.txt', 'fileB.txt')),
            ('/root/dir1', (), ('fileC.txt', 'fileD.txt')),
            ('/root/dir2', (), ('fileE.txt',)),
        ]

        # Setup mock os.path.getsize for each file
        # fileA and fileC are duplicates (same size, same content)
        # fileB and fileD are duplicates (same size, same content)
        # fileE is unique
        mock_getsize.side_effect = lambda p: {
            '/root/fileA.txt': 10,
            '/root/fileB.txt': 20,
            '/root/dir1/fileC.txt': 10,
            '/root/dir1/fileD.txt': 20,
            '/root/dir2/fileE.txt': 30,
            '/root/empty.txt': 0, # Should be skipped
        }.get(p, 1) # Default to 1 for any unexpected path

        # Setup mock_open to provide content for hashing
        def mock_open_side_effect(filepath, mode='r'):
            if 'fileA.txt' in filepath or 'fileC.txt' in filepath:
                mock_file_open.return_value.read.return_value = b'content_10'
            elif 'fileB.txt' in filepath or 'fileD.txt' in filepath:
                mock_file_open.return_value.read.return_value = b'content_20'
            elif 'fileE.txt' in filepath:
                mock_file_open.return_value.read.return_value = b'content_30'
            else:
                mock_file_open.return_value.read.return_value = b''
            return mock_file_open.return_value
        mock_file_open.side_effect = mock_open_side_effect

        # Calculate expected hashes
        hash_10 = hashlib.sha256(b'content_10').hexdigest()
        hash_20 = hashlib.sha256(b'content_20').hexdigest()

        duplicates = find_duplicate_files('/root')

        # Assertions
        self.assertIn(hash_10, duplicates)
        self.assertIn(hash_20, duplicates)
        self.assertNotIn(hashlib.sha256(b'content_30').hexdigest(), duplicates) # fileE is unique

        self.assertCountEqual(duplicates[hash_10], ['/root/fileA.txt', '/root/dir1/fileC.txt'])
        self.assertCountEqual(duplicates[hash_20], ['/root/fileB.txt', '/root/dir1/fileD.txt'])
        self.assertEqual(len(duplicates), 2)

    # Mock rationale: Simulate the filesystem operations (os.remove, os.link, os.path.exists, os.samefile)
    # without actually modifying the disk. This allows testing the linking logic deterministically.
    @patch('os.remove')
    @patch('os.link')
    @patch('os.path.exists')
    @patch('os.samefile')
    def test_link_duplicates_dry_run(self, mock_samefile, mock_exists, mock_link, mock_remove):
        duplicate_groups = {
            'hash1': ['/path/to/file1.txt', '/path/to/duplicate1.txt', '/path/to/another_dup1.txt'],
            'hash2': ['/path/to/file2.txt', '/path/to/duplicate2.txt']
        }
        
        # Mock rationale: All files exist for this test case.
        mock_exists.return_value = True
        # Mock rationale: No files are initially hard links to each other.
        mock_samefile.return_value = False

        actions = link_duplicates(duplicate_groups, dry_run=True)

        self.assertEqual(len(actions), 4) # 2 for hash1, 1 for hash2
        self.assertIn("DRY RUN: Would replace '/path/to/duplicate1.txt' with hard link to '/path/to/file1.txt'", actions)
        self.assertIn("DRY RUN: Would replace '/path/to/another_dup1.txt' with hard link to '/path/to/file1.txt'", actions)
        self.assertIn("DRY RUN: Would replace '/path/to/duplicate2.txt' with hard link to '/path/to/file2.txt'", actions)
        
        mock_remove.assert_not_called()
        mock_link.assert_not_called()

    @patch('os.remove')
    @patch('os.link')
    @patch('os.path.exists')
    @patch('os.samefile')
    def test_link_duplicates_execute(self, mock_samefile, mock_exists, mock_link, mock_remove):
        duplicate_groups = {
            'hash1': ['/path/to/file1.txt', '/path/to/duplicate1.txt'],
        }
        
        # Mock rationale: All files exist for this test case.
        mock_exists.return_value = True
        # Mock rationale: No files are initially hard links to each other.
        mock_samefile.return_value = False

        actions = link_duplicates(duplicate_groups, dry_run=False)

        self.assertEqual(len(actions), 1)
        self.assertIn("LINKED: '/path/to/duplicate1.txt' now links to '/path/to/file1.txt'", actions)
        
        mock_remove.assert_called_once_with('/path/to/duplicate1.txt')
        mock_link.assert_called_once_with('/path/to/file1.txt', '/path/to/duplicate1.txt')

    @patch('os.remove')
    @patch('os.link')
    @patch('os.path.exists')
    @patch('os.samefile')
    def test_link_duplicates_execute_original_missing(self, mock_samefile, mock_exists, mock_link, mock_remove):
        duplicate_groups = {
            'hash1': ['/path/to/missing_original.txt', '/path/to/duplicate1.txt'],
        }
        
        # Mock rationale: Simulate the original file being missing.
        mock_exists.side_effect = lambda p: p != '/path/to/missing_original.txt'
        mock_samefile.return_value = False

        actions = link_duplicates(duplicate_groups, dry_run=False)

        self.assertEqual(len(actions), 1)
        self.assertIn("WARNING: Original file '/path/to/missing_original.txt' for hash hash1... not found. Skipping group.", actions)
        
        mock_remove.assert_not_called()
        mock_link.assert_not_called()

    @patch('os.remove')
    @patch('os.link')
    @patch('os.path.exists')
    @patch('os.samefile')
    def test_link_duplicates_execute_duplicate_missing(self, mock_samefile, mock_exists, mock_link, mock_remove):
        duplicate_groups = {
            'hash1': ['/path/to/file1.txt', '/path/to/missing_duplicate.txt'],
        }
        
        # Mock rationale: Simulate the duplicate file being missing.
        mock_exists.side_effect = lambda p: p != '/path/to/missing_duplicate.txt'
        mock_samefile.return_value = False

        actions = link_duplicates(duplicate_groups, dry_run=False)

        self.assertEqual(len(actions), 1)
        self.assertIn("WARNING: Duplicate file '/path/to/missing_duplicate.txt' not found. Skipping.", actions)
        
        mock_remove.assert_not_called()
        mock_link.assert_not_called()

    @patch('os.remove')
    @patch('os.link')
    @patch('os.path.exists')
    @patch('os.samefile')
    def test_link_duplicates_execute_already_linked(self, mock_samefile, mock_exists, mock_link, mock_remove):
        duplicate_groups = {
            'hash1': ['/path/to/file1.txt', '/path/to/duplicate1.txt'],
        }
        
        # Mock rationale: Both files exist, and the duplicate is already a hard link to the original.
        mock_exists.return_value = True
        mock_samefile.return_value = True # Simulate already linked

        actions = link_duplicates(duplicate_groups, dry_run=False)

        self.assertEqual(len(actions), 1)
        self.assertIn("SKIPPED: '/path/to/duplicate1.txt' is already a hard link to '/path/to/file1.txt'", actions)
        
        mock_remove.assert_not_called()
        mock_link.assert_not_called()

    @patch('os.remove', side_effect=OSError("Permission denied"))
    @patch('os.link')
    @patch('os.path.exists', return_value=True)
    @patch('os.samefile', return_value=False)
    def test_link_duplicates_execute_remove_error(self, mock_samefile, mock_exists, mock_link, mock_remove):
        duplicate_groups = {
            'hash1': ['/path/to/file1.txt', '/path/to/duplicate1.txt'],
        }
        
        actions = link_duplicates(duplicate_groups, dry_run=False)

        self.assertEqual(len(actions), 1)
        self.assertIn("ERROR: Could not link '/path/to/duplicate1.txt' to '/path/to/file1.txt': Permission denied", actions)
        
        mock_remove.assert_called_once_with('/path/to/duplicate1.txt')
        mock_link.assert_not_called() # Link should not be called if remove fails

    @patch('os.remove')
    @patch('os.link', side_effect=OSError("Disk full"))
    @patch('os.path.exists', return_value=True)
    @patch('os.samefile', return_value=False)
    def test_link_duplicates_execute_link_error(self, mock_samefile, mock_exists, mock_link, mock_remove):
        duplicate_groups = {
            'hash1': ['/path/to/file1.txt', '/path/to/duplicate1.txt'],
        }
        
        actions = link_duplicates(duplicate_groups, dry_run=False)

        self.assertEqual(len(actions), 1)
        self.assertIn("ERROR: Could not link '/path/to/duplicate1.txt' to '/path/to/file1.txt': Disk full", actions)
        
        mock_remove.assert_called_once_with('/path/to/duplicate1.txt')
        mock_link.assert_called_once_with('/path/to/file1.txt', '/path/to/duplicate1.txt')
