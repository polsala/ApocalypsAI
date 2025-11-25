import unittest
import os
import hashlib
from unittest.mock import patch, mock_open, MagicMock
from src.resonator import calculate_file_hash, find_duplicate_files

class TestResonator(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash(self, mock_file_open):
        # Mock rationale: We don't want to read actual files during testing.
        # We simulate file content to ensure the hashing logic works correctly.
        mock_file_open.return_value.read.side_effect = [b"test content", b""] # Read once, then EOF

        expected_hash = hashlib.sha256(b"test content").hexdigest()
        self.assertEqual(calculate_file_hash("dummy_path.txt"), expected_hash)

        mock_file_open.assert_called_once_with("dummy_path.txt", 'rb')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.islink', return_value=False) # Mock rationale: Assume no symlinks for basic tests
    def test_find_duplicate_files_no_duplicates(self, mock_islink, mock_walk, mock_getsize, mock_file_open):
        # Mock rationale: Simulate a file system structure without actually creating files.
        # This makes tests deterministic and fast.
        mock_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt']),
        ]
        
        # Mock rationale: Simulate file sizes and content for hashing.
        # Each file has unique content, so no duplicates should be found.
        mock_getsize.side_effect = [10, 12] # file1.txt, file2.txt
        mock_file_open.side_effect = [
            mock_open(read_data=b"content1").return_value,
            mock_open(read_data=b"content2").return_value,
        ]

        duplicates = find_duplicate_files("/root")
        self.assertEqual(len(duplicates), 0)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.islink', return_value=False)
    def test_find_duplicate_files_with_duplicates(self, mock_islink, mock_walk, mock_getsize, mock_file_open):
        # Mock rationale: Simulate a file system with two files having identical content.
        mock_walk.return_value = [
            ('/root', ['subdir'], ['fileA.txt']),
            ('/root/subdir', [], ['fileB.txt']),
        ]
        
        # Mock rationale: Simulate file sizes and content.
        # fileA.txt and fileB.txt have the same content.
        mock_getsize.side_effect = [15, 15] # fileA.txt, fileB.txt
        mock_file_open.side_effect = [
            mock_open(read_data=b"duplicate content").return_value, # for fileA.txt
            mock_open(read_data=b"duplicate content").return_value, # for fileB.txt
        ]

        duplicates = find_duplicate_files("/root")
        self.assertEqual(len(duplicates), 1)

        expected_hash = hashlib.sha256(b"duplicate content").hexdigest()
        self.assertIn(expected_hash, duplicates)
        self.assertCountEqual(duplicates[expected_hash], [
            os.path.join('/root', 'fileA.txt'),
            os.path.join('/root/subdir', 'fileB.txt')
        ])

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.islink', return_value=False)
    def test_find_duplicate_files_empty_file_skipped(self, mock_islink, mock_walk, mock_getsize, mock_file_open):
        # Mock rationale: Ensure that empty files are correctly skipped as per logic.
        mock_walk.return_value = [
            ('/root', [], ['empty.txt', 'real.txt']),
        ]
        
        # Mock rationale: Simulate sizes, one file is empty.
        mock_getsize.side_effect = [0, 10] # empty.txt, real.txt
        mock_file_open.return_value.read.side_effect = [b"real content", b""] # Only real.txt is opened

        duplicates = find_duplicate_files("/root")
        self.assertEqual(len(duplicates), 0) # No duplicates, and empty file shouldn't cause issues

        # Ensure 'empty.txt' was not opened for hashing
        mock_file_open.assert_called_once_with(os.path.join('/root', 'real.txt'), 'rb')

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    @patch('os.path.getsize', return_value=10)
    @patch('os.walk')
    @patch('os.path.islink', return_value=False)
    @patch('sys.stderr', new_callable=MagicMock) # Mock rationale: Capture stderr output for warnings
    def test_find_duplicate_files_io_error_handling(self, mock_stderr, mock_islink, mock_walk, mock_getsize, mock_file_open):
        # Mock rationale: Simulate a scenario where a file cannot be read (e.g., permission error).
        # The utility should handle this gracefully and not crash.
        mock_walk.return_value = [
            ('/root', [], ['unreadable.txt']),
        ]
        
        duplicates = find_duplicate_files("/root")
        self.assertEqual(len(duplicates), 0)
        mock_stderr.write.assert_called_with("Warning: Could not hash file: /root/unreadable.txt\n")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.islink', return_value=True) # Mock rationale: Test symlink skipping
    def test_find_duplicate_files_symlink_skipped(self, mock_islink, mock_walk, mock_getsize, mock_file_open):
        # Mock rationale: Ensure symbolic links are skipped to prevent issues.
        mock_walk.return_value = [
            ('/root', [], ['link.txt']),
        ]
        
        # Mock rationale: getsize and open should not be called for a symlink
        mock_getsize.side_effect = [10] # This should not be called if islink is True
        mock_file_open.return_value.read.side_effect = [b"content", b""] # This should not be called

        duplicates = find_duplicate_files("/root")
        self.assertEqual(len(duplicates), 0)
        mock_getsize.assert_not_called()
        mock_file_open.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.islink', return_value=False)
    def test_find_duplicate_files_os_error_getsize(self, mock_islink, mock_walk, mock_getsize, mock_file_open):
        # Mock rationale: Simulate a file disappearing or becoming inaccessible between os.walk and os.path.getsize.
        mock_walk.return_value = [
            ('/root', [], ['disappearing.txt']),
        ]
        mock_getsize.side_effect = OSError("File not found") # Simulate file disappearing
        
        duplicates = find_duplicate_files("/root")
        self.assertEqual(len(duplicates), 0)
        mock_file_open.assert_not_called() # File should not be opened if getsize fails

if __name__ == '__main__':
    unittest.main()
