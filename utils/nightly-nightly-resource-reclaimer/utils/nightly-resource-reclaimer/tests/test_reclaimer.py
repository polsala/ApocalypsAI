import unittest
from unittest.mock import patch, mock_open
import os
import sys
import io
import hashlib

# Mock rationale: We need to simulate file system interactions (os.walk, os.path.isfile, os.path.getsize, file reading) 
# without actually creating files on disk or relying on the real file system state. 
# This ensures tests are deterministic, fast, and isolated.

# Import the functions to be tested
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from reclaimer import calculate_file_hash, find_duplicates_and_empty_dirs

class TestReclaimer(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.md5')
    def test_calculate_file_hash(self, mock_md5, mock_file_open):
        # Mock rationale: Simulate file content and MD5 hashing without actual file I/O.
        mock_file_open.return_value.__enter__.return_value.read.side_effect = [b'test content', b'']
        mock_hasher = mock_md5.return_value
        mock_hasher.hexdigest.return_value = 'd41d8cd98f00b204e9800998ecf8427e' # MD5 for 'test content'

        result = calculate_file_hash('/fake/path/file.txt')
        self.assertEqual(result, 'd41d8cd98f00b204e9800998ecf8427e')
        mock_file_open.assert_called_once_with('/fake/path/file.txt', 'rb')
        mock_hasher.update.assert_called_once_with(b'test content')

    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.islink', return_value=False)
    @patch('os.path.getsize')
    @patch('reclaimer.calculate_file_hash')
    def test_find_duplicates_and_empty_dirs_no_issues(self, mock_calculate_hash, mock_getsize, mock_islink, mock_isfile, mock_walk):
        # Mock rationale: Simulate a file system with no duplicates or empty directories.
        # os.walk: Controls the directory structure.
        # os.path.isfile/islink: Ensures files are treated as regular files.
        # os.path.getsize: Provides file sizes for reporting.
        # reclaimer.calculate_file_hash: Provides deterministic hashes for files.
        
        mock_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['fileA.txt']),
            ('/root/dir1', [], ['fileB.txt']),
            ('/root/dir2', ['subdir'], ['fileC.txt']),
            ('/root/dir2/subdir', [], ['fileD.txt'])
        ]
        mock_calculate_hash.side_effect = {
            '/root/fileA.txt': 'hashA',
            '/root/dir1/fileB.txt': 'hashB',
            '/root/dir2/fileC.txt': 'hashC',
            '/root/dir2/subdir/fileD.txt': 'hashD'
        }.get
        mock_getsize.side_effect = {
            '/root/fileA.txt': 100,
            '/root/dir1/fileB.txt': 200,
            '/root/dir2/fileC.txt': 300,
            '/root/dir2/subdir/fileD.txt': 400
        }.get

        duplicates, empty_dirs, potential_reclaim_size = find_duplicates_and_empty_dirs('/root')

        self.assertEqual(duplicates, {})
        self.assertEqual(empty_dirs, [])
        self.assertEqual(potential_reclaim_size, 0)

    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.islink', return_value=False)
    @patch('os.path.getsize')
    @patch('reclaimer.calculate_file_hash')
    def test_find_duplicates_only(self, mock_calculate_hash, mock_getsize, mock_islink, mock_isfile, mock_walk):
        # Mock rationale: Simulate a file system with duplicate files but no empty directories.
        mock_walk.return_value = [
            ('/root', ['dir1'], ['file1.txt', 'file2.txt']),
            ('/root/dir1', [], ['file3.txt'])
        ]
        mock_calculate_hash.side_effect = {
            '/root/file1.txt': 'hash_dup',
            '/root/file2.txt': 'hash_dup',
            '/root/dir1/file3.txt': 'hash_unique'
        }.get
        mock_getsize.side_effect = {
            '/root/file1.txt': 100,
            '/root/file2.txt': 100,
            '/root/dir1/file3.txt': 50
        }.get

        duplicates, empty_dirs, potential_reclaim_size = find_duplicates_and_empty_dirs('/root')

        expected_duplicates = {
            'hash_dup': ['/root/file1.txt', '/root/file2.txt']
        }
        self.assertEqual(duplicates, expected_duplicates)
        self.assertEqual(empty_dirs, [])
        self.assertEqual(potential_reclaim_size, 100) # One duplicate file of 100 bytes

    @patch('os.walk')
    @patch('os.path.isfile', return_value=False) # No files in empty dirs
    @patch('os.path.islink', return_value=False)
    @patch('os.path.getsize', return_value=0) # Not relevant for empty dirs, but good to mock
    @patch('reclaimer.calculate_file_hash', return_value=None) # Not relevant for empty dirs
    def test_find_empty_dirs_only(self, mock_calculate_hash, mock_getsize, mock_islink, mock_isfile, mock_walk):
        # Mock rationale: Simulate a file system with empty directories but no files.
        mock_walk.return_value = [
            ('/root', ['empty1', 'non_empty'], []),
            ('/root/empty1', [], []),
            ('/root/non_empty', ['sub_empty'], []),
            ('/root/non_empty/sub_empty', [], [])
        ]

        duplicates, empty_dirs, potential_reclaim_size = find_duplicates_and_empty_dirs('/root')

        expected_empty_dirs = [
            '/root/empty1',
            '/root/non_empty/sub_empty'
        ]
        # The order of empty_dirs might vary based on os.walk implementation, so sort for comparison.
        self.assertEqual(duplicates, {})
        self.assertEqual(sorted(empty_dirs), sorted(expected_empty_dirs))
        self.assertEqual(potential_reclaim_size, 0)

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.islink', return_value=False)
    @patch('os.path.getsize')
    @patch('reclaimer.calculate_file_hash')
    def test_find_mixed_issues(self, mock_calculate_hash, mock_getsize, mock_islink, mock_isfile, mock_walk):
        # Mock rationale: Simulate a file system with both duplicate files and empty directories.
        mock_walk.return_value = [
            ('/root', ['dir_dup', 'dir_empty'], ['fileA.txt', 'fileB.txt']),
            ('/root/dir_dup', [], ['fileC.txt']),
            ('/root/dir_empty', [], []),
            ('/root/another_empty', [], []) # Another empty dir
        ]
        
        # Configure isfile for specific paths
        def mock_isfile_side_effect(path):
            return path in ['/root/fileA.txt', '/root/fileB.txt', '/root/dir_dup/fileC.txt']
        mock_isfile.side_effect = mock_isfile_side_effect

        mock_calculate_hash.side_effect = {
            '/root/fileA.txt': 'hash_dup_1',
            '/root/fileB.txt': 'hash_dup_1',
            '/root/dir_dup/fileC.txt': 'hash_unique'
        }.get
        mock_getsize.side_effect = {
            '/root/fileA.txt': 100,
            '/root/fileB.txt': 100,
            '/root/dir_dup/fileC.txt': 50
        }.get

        duplicates, empty_dirs, potential_reclaim_size = find_duplicates_and_empty_dirs('/root')

        expected_duplicates = {
            'hash_dup_1': ['/root/fileA.txt', '/root/fileB.txt']
        }
        expected_empty_dirs = [
            '/root/dir_empty',
            '/root/another_empty'
        ]

        self.assertEqual(duplicates, expected_duplicates)
        self.assertEqual(sorted(empty_dirs), sorted(expected_empty_dirs))
        self.assertEqual(potential_reclaim_size, 100)

    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.islink', return_value=True) # Test with a symlink
    @patch('os.path.getsize')
    @patch('reclaimer.calculate_file_hash')
    def test_symlink_ignored(self, mock_calculate_hash, mock_getsize, mock_islink, mock_isfile, mock_walk):
        # Mock rationale: Ensure symlinks are ignored during file processing.
        mock_walk.return_value = [
            ('/root', [], ['link_to_file.txt'])
        ]
        mock_calculate_hash.return_value = 'some_hash'
        mock_getsize.return_value = 100

        duplicates, empty_dirs, potential_reclaim_size = find_duplicates_and_empty_dirs('/root')

        self.assertEqual(duplicates, {})
        self.assertEqual(empty_dirs, [])
        self.assertEqual(potential_reclaim_size, 0)
        mock_calculate_hash.assert_not_called() # Should not try to hash a symlink

    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.islink', return_value=False)
    @patch('os.path.getsize', side_effect=OSError) # Simulate permission error for getsize
    @patch('reclaimer.calculate_file_hash', return_value='hash_val')
    def test_getsize_error_handling(self, mock_calculate_hash, mock_getsize, mock_islink, mock_isfile, mock_walk):
        # Mock rationale: Test robustness when os.path.getsize fails (e.g., permission denied).
        mock_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt'])
        ]
        mock_calculate_hash.side_effect = {
            '/root/file1.txt': 'hash_dup',
            '/root/file2.txt': 'hash_dup'
        }.get

        duplicates, empty_dirs, potential_reclaim_size = find_duplicates_and_empty_dirs('/root')

        expected_duplicates = {
            'hash_dup': ['/root/file1.txt', '/root/file2.txt']
        }
        self.assertEqual(duplicates, expected_duplicates)
        self.assertEqual(empty_dirs, [])
        self.assertEqual(potential_reclaim_size, 0) # Should be 0 if getsize fails for all duplicates

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('os.path.isdir', return_value=True)
    @patch('reclaimer.find_duplicates_and_empty_dirs')
    def test_main_output(self, mock_find, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Capture stdout/stderr and mock the core logic to test the main function's output formatting.
        mock_find.return_value = (
            {'hash1': ['/path/fileA.txt', '/path/fileB.txt']},
            ['/path/empty_dir'],
            1024 # 1 KB potential reclaim
        )
        
        # Simulate command line arguments
        test_args = ['reclaimer.py', '/path']
        with patch('sys.argv', test_args):
            from reclaimer import main
            main()
            output = mock_stdout.getvalue()
            self.assertIn('Scanning /path...', output)
            self.assertIn('--- Duplicate Files Found ---', output)
            self.assertIn('Group 1 (MD5: hash1):', output)
            self.assertIn('  - /path/fileA.txt (1 KB)', output)
            self.assertIn('  - /path/fileB.txt (1 KB)', output)
            self.assertIn('--- Empty Directories Found ---', output)
            self.assertIn('  - /path/empty_dir/', output)
            self.assertIn('Scan complete. Reclaimed potential: 1 KB (from duplicates) + 1 empty directories.', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('os.path.isdir', return_value=False)
    def test_main_invalid_path(self, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Test error handling for invalid input path.
        test_args = ['reclaimer.py', '/nonexistent']
        with patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                from reclaimer import main
                main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: '/nonexistent' is not a valid directory.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_no_args(self, mock_stderr, mock_stdout):
        # Mock rationale: Test error handling for missing command line arguments.
        test_args = ['reclaimer.py']
        with patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                from reclaimer import main
                main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Usage: python reclaimer.py <path_to_scan>", mock_stdout.getvalue())
