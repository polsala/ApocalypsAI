import unittest
import os
import hashlib
from unittest.mock import patch, mock_open, MagicMock
from src.deduplicator import calculate_file_hash, find_duplicate_files

class TestDeduplicator(unittest.TestCase):

    def test_calculate_file_hash(self):
        # Mock rationale: We don't want to read actual files during tests.
        # We provide specific content to ensure deterministic hash calculation.
        mock_file_content = b"test content for hashing"
        expected_hash = hashlib.sha256(mock_file_content).hexdigest()

        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open:
            # Simulate reading in blocks, even if content is small
            m_open.return_value.read.side_effect = [mock_file_content, b''] 
            
            self.assertEqual(calculate_file_hash("dummy_path.txt"), expected_hash)
            m_open.assert_called_once_with("dummy_path.txt", 'rb')

    def test_find_duplicate_files_no_duplicates(self):
        # Mock rationale: Simulate a directory structure with unique files.
        # This avoids actual file system interaction and ensures determinism.
        mock_dir = "/mock/data"
        mock_walk_return = [
            (mock_dir, [], ["file1.txt", "file2.txt"]),
        ]
        
        # Mock file content and their hashes
        file1_content = b"unique content 1"
        file2_content = b"unique content 2"
        hash1 = hashlib.sha256(file1_content).hexdigest()
        hash2 = hashlib.sha256(file2_content).hexdigest()

        # Mock os.walk
        with patch('os.walk', return_value=mock_walk_return), \
             patch('os.path.islink', return_value=False), \
             patch('src.deduplicator.calculate_file_hash') as m_calculate_hash:
            
            # Mock calculate_file_hash to return specific hashes for specific files
            def side_effect_calculate_hash(filepath, *args, **kwargs):
                if filepath == os.path.join(mock_dir, "file1.txt"):
                    return hash1
                elif filepath == os.path.join(mock_dir, "file2.txt"):
                    return hash2
                return "some_other_hash" # Fallback
            
            m_calculate_hash.side_effect = side_effect_calculate_hash

            duplicates = find_duplicate_files(mock_dir)
            self.assertEqual(duplicates, {})
            m_calculate_hash.assert_any_call(os.path.join(mock_dir, "file1.txt"))
            m_calculate_hash.assert_any_call(os.path.join(mock_dir, "file2.txt"))

    def test_find_duplicate_files_with_duplicates(self):
        # Mock rationale: Simulate a directory structure with duplicate files.
        # This allows testing the core logic of duplicate detection without real files.
        mock_dir = "/mock/data"
        mock_walk_return = [
            (mock_dir, ["subdir"], ["fileA.txt", "fileB.txt"]),
            (os.path.join(mock_dir, "subdir"), [], ["fileC.txt"]),
        ]

        # Mock file content and their hashes
        content_duplicate = b"duplicate content"
        content_unique = b"unique content"
        hash_duplicate = hashlib.sha256(content_duplicate).hexdigest()
        hash_unique = hashlib.sha256(content_unique).hexdigest()

        with patch('os.walk', return_value=mock_walk_return), \
             patch('os.path.islink', return_value=False), \
             patch('src.deduplicator.calculate_file_hash') as m_calculate_hash:
            
            def side_effect_calculate_hash(filepath, *args, **kwargs):
                if filepath in [os.path.join(mock_dir, "fileA.txt"), os.path.join(mock_dir, "subdir", "fileC.txt")]:
                    return hash_duplicate
                elif filepath == os.path.join(mock_dir, "fileB.txt"):
                    return hash_unique
                return "some_other_hash"
            
            m_calculate_hash.side_effect = side_effect_calculate_hash

            duplicates = find_duplicate_files(mock_dir)
            
            expected_duplicates = {
                hash_duplicate: [
                    os.path.join(mock_dir, "fileA.txt"),
                    os.path.join(mock_dir, "subdir", "fileC.txt")
                ]
            }
            self.assertEqual(duplicates, expected_duplicates)
            self.assertIn(os.path.join(mock_dir, "fileA.txt"), duplicates[hash_duplicate])
            self.assertIn(os.path.join(mock_dir, "subdir", "fileC.txt"), duplicates[hash_duplicate])
            self.assertNotIn(hash_unique, duplicates) # Ensure unique files are not in duplicates

    def test_find_duplicate_files_with_symlink(self):
        # Mock rationale: Ensure symlinks are skipped to prevent issues like infinite loops
        # or incorrect duplicate detection if the target is already scanned.
        mock_dir = "/mock/data"
        mock_walk_return = [
            (mock_dir, [], ["file1.txt", "link_to_file1.txt"]),
        ]
        
        file1_content = b"content"
        hash1 = hashlib.sha256(file1_content).hexdigest()

        with patch('os.walk', return_value=mock_walk_return), \
             patch('os.path.islink') as m_islink, \
             patch('src.deduplicator.calculate_file_hash') as m_calculate_hash:
            
            m_islink.side_effect = lambda p: p == os.path.join(mock_dir, "link_to_file1.txt")
            m_calculate_hash.return_value = hash1 # For file1.txt

            duplicates = find_duplicate_files(mock_dir)
            self.assertEqual(duplicates, {}) # No duplicates because symlink is skipped
            m_calculate_hash.assert_called_once_with(os.path.join(mock_dir, "file1.txt"))
            m_islink.assert_any_call(os.path.join(mock_dir, "link_to_file1.txt"))
            m_islink.assert_any_call(os.path.join(mock_dir, "file1.txt")) # os.walk will check this too

    def test_find_duplicate_files_io_error(self):
        # Mock rationale: Test error handling when a file cannot be read.
        # This ensures the utility is robust against file system issues.
        mock_dir = "/mock/data"
        mock_walk_return = [
            (mock_dir, [], ["unreadable.txt", "readable.txt"]),
        ]
        
        readable_content = b"readable content"
        readable_hash = hashlib.sha256(readable_content).hexdigest()

        with patch('os.walk', return_value=mock_walk_return), \
             patch('os.path.islink', return_value=False), \
             patch('src.deduplicator.calculate_file_hash') as m_calculate_hash, \
             patch('builtins.print') as m_print: # Capture print statements
            
            def side_effect_calculate_hash(filepath, *args, **kwargs):
                if filepath == os.path.join(mock_dir, "unreadable.txt"):
                    raise IOError("Permission denied")
                elif filepath == os.path.join(mock_dir, "readable.txt"):
                    return readable_hash
                return "some_other_hash"
            
            m_calculate_hash.side_effect = side_effect_calculate_hash

            duplicates = find_duplicate_files(mock_dir)
            self.assertEqual(duplicates, {}) # No duplicates expected in this scenario
            m_print.assert_called_with(f"Warning: Could not read file {os.path.join(mock_dir, 'unreadable.txt')}: Permission denied")
            m_calculate_hash.assert_any_call(os.path.join(mock_dir, "unreadable.txt"))
            m_calculate_hash.assert_any_call(os.path.join(mock_dir, "readable.txt"))
