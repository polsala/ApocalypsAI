import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
from collections import defaultdict
import hashlib

# Add the src directory to the path to allow importing purifier
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from purifier import calculate_file_hash, find_duplicate_files, main

class TestPurifier(unittest.TestCase):

    def setUp(self):
        # Mock os.path.isfile for calculate_file_hash
        self.isfile_patcher = patch('os.path.isfile')
        self.mock_isfile = self.isfile_patcher.start()
        self.mock_isfile.return_value = True # Assume files exist by default for hash calculation

        # Mock os.path.islink for find_duplicate_files
        self.islink_patcher = patch('os.path.islink')
        self.mock_islink = self.islink_patcher.start()
        self.mock_islink.return_value = False # Assume no symlinks by default

        # Mock os.path.isdir for main function
        self.isdir_patcher = patch('os.path.isdir')
        self.mock_isdir = self.isdir_patcher.start()
        self.mock_isdir.return_value = True # Assume the start path is a directory

    def tearDown(self):
        self.isfile_patcher.stop()
        self.islink_patcher.stop()
        self.isdir_patcher.stop()

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_md5(self, mock_file):
        # Mock rationale: We don't want to read actual files during tests.
        # We provide mock content to ensure the hash calculation logic is correct.
        mock_file.return_value.read.side_effect = [b"content", b" of a file", b""]
        expected_hash = hashlib.md5(b"content of a file").hexdigest()
        self.assertEqual(calculate_file_hash("/path/to/file.txt", hash_algo='md5'), expected_hash)

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_sha256(self, mock_file):
        # Mock rationale: Same as above, testing different hash algorithm.
        mock_file.return_value.read.side_effect = [b"another content", b""]
        expected_hash = hashlib.sha256(b"another content").hexdigest()
        self.assertEqual(calculate_file_hash("/path/to/file2.txt", hash_algo='sha256'), expected_hash)

    def test_calculate_file_hash_non_existent_file(self):
        # Mock rationale: Test behavior when os.path.isfile returns False.
        self.mock_isfile.return_value = False
        self.assertIsNone(calculate_file_hash("/non/existent/file.txt"))

    @patch('os.walk')
    @patch('purifier.calculate_file_hash')
    def test_find_duplicate_files_no_duplicates(self, mock_calculate_hash, mock_walk):
        # Mock rationale: Simulate a file system structure and file hashes without actual disk I/O.
        # os.walk provides directory structure, calculate_file_hash provides content hashes.
        mock_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt']),
        ]
        mock_calculate_hash.side_effect = {
            '/root/file1.txt': 'hash1',
            '/root/file2.txt': 'hash2',
        }.get
        
        duplicates = find_duplicate_files('/root')
        self.assertEqual(duplicates, {})

    @patch('os.walk')
    @patch('purifier.calculate_file_hash')
    def test_find_duplicate_files_with_duplicates(self, mock_calculate_hash, mock_walk):
        # Mock rationale: Simulate a file system with duplicate content.
        mock_walk.return_value = [
            ('/root', ['subdir'], ['fileA.txt', 'fileB.txt']),
            ('/root/subdir', [], ['fileC.txt']),
        ]
        mock_calculate_hash.side_effect = {
            '/root/fileA.txt': 'hash_dup',
            '/root/fileB.txt': 'hash_unique',
            '/root/subdir/fileC.txt': 'hash_dup',
        }.get
        
        duplicates = find_duplicate_files('/root')
        expected_duplicates = {
            'hash_dup': ['/root/fileA.txt', '/root/subdir/fileC.txt']
        }
        self.assertEqual(duplicates, expected_duplicates)

    @patch('os.walk')
    @patch('purifier.calculate_file_hash')
    def test_find_duplicate_files_with_excluded_directory(self, mock_calculate_hash, mock_walk):
        # Mock rationale: Verify that specified directories are skipped by os.walk.
        mock_walk.return_value = [
            ('/root', ['excluded_dir', 'included_dir'], ['file1.txt']),
            ('/root/excluded_dir', [], ['excluded_file.txt']),
            ('/root/included_dir', [], ['file2.txt']),
        ]
        mock_calculate_hash.side_effect = {
            '/root/file1.txt': 'hash1',
            '/root/included_dir/file2.txt': 'hash2',
        }.get

        duplicates = find_duplicate_files('/root', exclude_dirs=['excluded_dir'])
        self.assertEqual(duplicates, {}) # No duplicates in this setup, just testing exclusion
        
        # Ensure that 'excluded_dir' was indeed excluded from the walk
        # The mock_walk.call_args_list will show how os.walk was called and how dirnames were modified
        # This is a bit tricky to assert directly on the in-place modification of dirnames.
        # A simpler check is to ensure that files from excluded_dir are not processed.
        self.assertNotIn(('/root/excluded_dir/excluded_file.txt',), [call.args for call in mock_calculate_hash.call_args_list])


    @patch('os.walk')
    @patch('purifier.calculate_file_hash')
    def test_find_duplicate_files_with_symlink(self, mock_calculate_hash, mock_walk):
        # Mock rationale: Ensure symbolic links are skipped to prevent issues.
        mock_walk.return_value = [
            ('/root', [], ['file1.txt', 'link_to_file1.txt']),
        ]
        self.mock_islink.side_effect = lambda p: p == '/root/link_to_file1.txt'
        mock_calculate_hash.side_effect = {
            '/root/file1.txt': 'hash1',
        }.get

        duplicates = find_duplicate_files('/root')
        self.assertEqual(duplicates, {})
        # Ensure calculate_file_hash was not called for the symlink
        self.assertNotIn(('/root/link_to_file1.txt',), [call.args for call in mock_calculate_hash.call_args_list])


    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('purifier.find_duplicate_files')
    def test_main_no_duplicates(self, mock_find_duplicates, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulate running the main script without actual file system interaction
        # and capture stdout/stderr to verify output.
        mock_parse_args.return_value = MagicMock(path="/test_dir", hash_algo="md5", exclude=[])
        mock_find_duplicates.return_value = {}
        
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        mock_stdout.write.assert_any_call("No duplicate files found. Your echo chamber is pure!\n")
        mock_stderr.assert_not_called()

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('purifier.find_duplicate_files')
    def test_main_with_duplicates(self, mock_find_duplicates, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulate running the main script with duplicates found.
        mock_parse_args.return_value = MagicMock(path="/test_dir", hash_algo="md5", exclude=[])
        mock_find_duplicates.return_value = {
            'hash123': ['/test_dir/fileA.txt', '/test_dir/subdir/fileB.txt']
        }
        
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        mock_stdout.write.assert_any_call("Found 1 sets of duplicate files:\n")
        mock_stdout.write.assert_any_call("\nHash: hash123\n")
        mock_stdout.write.assert_any_call("  - /test_dir/fileA.txt\n")
        mock_stdout.write.assert_any_call("  - /test_dir/subdir/fileB.txt\n")
        mock_stderr.assert_not_called()

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir') # Explicitly mock isdir for this test
    def test_main_invalid_path(self, mock_isdir, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Test error handling for non-existent starting directory.
        mock_parse_args.return_value = MagicMock(path="/non_existent_dir", hash_algo="md5", exclude=[])
        mock_isdir.return_value = False # Simulate directory not found
        
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        mock_stderr.write.assert_any_call("Error: Directory '/non_existent_dir' not found.\n")
        mock_stdout.assert_not_called()

if __name__ == '__main__':
    unittest.main()
