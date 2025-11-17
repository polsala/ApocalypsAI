import unittest
import os
import hashlib
from unittest.mock import patch, mock_open
from collections import defaultdict
from io import StringIO

# Import the functions to be tested
from src.monitor import calculate_file_hash, find_duplicate_files, main

class TestEchoChamberMonitor(unittest.TestCase):

    # Mock rationale: We need to simulate file system operations (reading files, walking directories)
    # without actually touching the disk. This ensures tests are fast, deterministic, and isolated.
    # `os.walk` is mocked to control the directory structure, and `open` is mocked to control file content.

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_success(self, mock_file_open):
        # Mock rationale: Simulate a file with known content to get a predictable hash.
        mock_file_open.return_value.read.side_effect = [b"test content", b""]
        expected_hash = hashlib.sha256(b"test content").hexdigest()
        self.assertEqual(calculate_file_hash("dummy_path.txt"), expected_hash)
        mock_file_open.assert_called_with("dummy_path.txt", 'rb')

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_calculate_file_hash_io_error(self, mock_file_open):
        # Mock rationale: Simulate a file that cannot be read due to an IOError.
        self.assertIsNone(calculate_file_hash("unreadable_path.txt"))
        mock_file_open.assert_called_with("unreadable_path.txt", 'rb')

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.islink', return_value=False) # Mock rationale: Ensure symlinks are not processed by default
    def test_find_duplicate_files_no_duplicates(self, mock_islink, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory with unique files.
        mock_os_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt'])
        ]
        
        # Mock rationale: Provide distinct content for each file.
        mock_file_open.side_effect = [
            mock_open(read_data=b"content1").return_value,
            mock_open(read_data=b"content2").return_value,
        ]

        duplicates = find_duplicate_files('/root')
        self.assertEqual(len(duplicates), 0)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.islink', return_value=False)
    def test_find_duplicate_files_with_duplicates(self, mock_islink, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory with duplicate files across different paths.
        mock_os_walk.return_value = [
            ('/root', ['subdir'], ['fileA.txt', 'fileB.txt']),
            ('/root/subdir', [], ['fileC.txt'])
        ]

        # Mock rationale: fileA.txt and fileC.txt have the same content. fileB.txt is unique.
        mock_file_open.side_effect = [
            mock_open(read_data=b"duplicate content").return_value, # fileA.txt
            mock_open(read_data=b"unique content").return_value,    # fileB.txt
            mock_open(read_data=b"duplicate content").return_value, # fileC.txt
        ]

        duplicates = find_duplicate_files('/root')
        self.assertEqual(len(duplicates), 1)
        
        duplicate_hash = hashlib.sha256(b"duplicate content").hexdigest()
        self.assertIn(duplicate_hash, duplicates)
        self.assertCountEqual(duplicates[duplicate_hash], ['/root/fileA.txt', '/root/subdir/fileC.txt'])

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.islink', return_value=True) # Mock rationale: Test skipping symbolic links
    def test_find_duplicate_files_skips_symlinks(self, mock_islink, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory containing a symbolic link.
        mock_os_walk.return_value = [
            ('/root', [], ['symlink.txt', 'realfile.txt'])
        ]
        
        # Mock rationale: Only realfile.txt should be opened.
        mock_file_open.return_value.read.side_effect = [b"real content", b""]

        duplicates = find_duplicate_files('/root')
        self.assertEqual(len(duplicates), 0) # No duplicates, and symlink is skipped
        # Ensure 'open' was only called for 'realfile.txt'
        mock_file_open.assert_called_once_with('/root/realfile.txt', 'rb')


    @patch('os.walk', return_value=[]) # Mock rationale: Simulate an empty directory.
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.islink', return_value=False)
    def test_find_duplicate_files_empty_directory(self, mock_islink, mock_file_open, mock_os_walk):
        duplicates = find_duplicate_files('/empty')
        self.assertEqual(len(duplicates), 0)
        mock_file_open.assert_not_called()

    @patch('os.path.isdir', return_value=True)
    @patch('src.monitor.find_duplicate_files')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_duplicates_output(self, mock_stdout, mock_find_duplicates, mock_isdir):
        # Mock rationale: Simulate the scenario where no duplicates are found.
        mock_find_duplicates.return_value = {}
        
        # Mock rationale: Simulate command-line arguments.
        with patch('argparse.ArgumentParser.parse_args', return_value=unittest.mock.Mock(path='/test_dir')):
            main()
            output = mock_stdout.getvalue()
            self.assertIn("No echoes detected", output)
            self.assertNotIn("sets of duplicate files", output)

    @patch('os.path.isdir', return_value=True)
    @patch('src.monitor.find_duplicate_files')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_duplicates_output(self, mock_stdout, mock_find_duplicates, mock_isdir):
        # Mock rationale: Simulate the scenario where duplicates are found.
        duplicate_hash_1 = hashlib.sha256(b"content A").hexdigest()
        duplicate_hash_2 = hashlib.sha256(b"content B").hexdigest()
        mock_find_duplicates.return_value = {
            duplicate_hash_1: ['/test_dir/file1.txt', '/test_dir/sub/fileA.txt'],
            duplicate_hash_2: ['/test_dir/file2.txt', '/test_dir/fileB.txt']
        }

        # Mock rationale: Simulate command-line arguments.
        with patch('argparse.ArgumentParser.parse_args', return_value=unittest.mock.Mock(path='/test_dir')):
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Found 2 sets of duplicate files", output)
            self.assertIn(f"Hash: {duplicate_hash_1}", output)
            self.assertIn(f"  - /test_dir/file1.txt", output)
            self.assertIn(f"  - /test_dir/sub/fileA.txt", output)
            self.assertIn(f"Hash: {duplicate_hash_2}", output)
            self.assertIn(f"  - /test_dir/file2.txt", output)
            self.assertIn(f"  - /test_dir/fileB.txt", output)
            self.assertIn("Scan complete. No more echoes detected.", output)

    @patch('os.path.isdir', return_value=False)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_stdout, mock_isdir):
        # Mock rationale: Simulate an invalid directory path provided as argument.
        with patch('argparse.ArgumentParser.parse_args', return_value=unittest.mock.Mock(path='/non_existent_dir')):
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Error: Directory not found at '/non_existent_dir'", output)
            mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
