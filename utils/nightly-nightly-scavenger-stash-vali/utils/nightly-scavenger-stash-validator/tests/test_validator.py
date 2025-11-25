import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
from io import StringIO
import hashlib

# Add the src directory to the path to allow importing validator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import validator

class TestValidator(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_get_file_info_basic(self, mock_getsize, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure without actual file system access.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log']),
            ('/test_dir/subdir', [], ['subfile.dat'])
        ]
        mock_isfile.side_effect = lambda x: x in ['/test_dir/file1.txt', '/test_dir/file2.log', '/test_dir/subdir/subfile.dat']
        mock_getsize.side_effect = lambda x: {
            '/test_dir/file1.txt': 100,
            '/test_dir/file2.log': 0,
            '/test_dir/subdir/subfile.dat': 500
        }.get(x, 0)

        file_info = validator.get_file_info('/test_dir')
        self.assertEqual(len(file_info), 3)
        self.assertIn({'path': '/test_dir/file1.txt', 'size': 100, 'hash': None}, file_info)
        self.assertIn({'path': '/test_dir/file2.log', 'size': 0, 'hash': None}, file_info)
        self.assertIn({'path': '/test_dir/subdir/subfile.dat', 'size': 500, 'hash': None}, file_info)

    def test_find_empty_files(self):
        # Mock rationale: Provide a pre-defined list of file info to test the filtering logic.
        file_info = [
            {'path': '/a/file1.txt', 'size': 100},
            {'path': '/a/empty.txt', 'size': 0},
            {'path': '/a/file2.log', 'size': 50},
            {'path': '/a/another_empty.dat', 'size': 0}
        ]
        empty = validator.find_empty_files(file_info)
        self.assertEqual(len(empty), 2)
        self.assertIn('/a/empty.txt', empty)
        self.assertIn('/a/another_empty.dat', empty)

    def test_find_large_files(self):
        # Mock rationale: Provide a pre-defined list of file info to test the filtering logic.
        file_info = [
            {'path': '/b/small.txt', 'size': 100},
            {'path': '/b/medium.log', 'size': 5 * 1024 * 1024},
            {'path': '/b/large.dat', 'size': 15 * 1024 * 1024},
            {'path': '/b/huge.bin', 'size': 25 * 1024 * 1024}
        ]
        max_size_bytes = 10 * 1024 * 1024 # 10 MB
        large = validator.find_large_files(file_info, max_size_bytes)
        self.assertEqual(len(large), 2)
        self.assertIn({'path': '/b/large.dat', 'size_mb': 15.0}, large)
        self.assertIn({'path': '/b/huge.bin', 'size_mb': 25.0}, large)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isfile', return_value=True)
    @patch('validator.calculate_file_hash') # Mock rationale: Avoid actual file I/O and ensure deterministic hash values.
    def test_find_duplicate_files(self, mock_calculate_file_hash, mock_isfile, mock_open):
        # Mock rationale: Simulate file content and hash calculation without actual file system access.
        mock_calculate_file_hash.side_effect = {
            '/c/fileA.txt': 'hash123',
            '/c/fileB.txt': 'hash456',
            '/c/fileC.txt': 'hash123',
            '/c/fileD.txt': 'hash789',
            '/c/fileE.txt': 'hash456'
        }.get

        file_info = [
            {'path': '/c/fileA.txt', 'size': 100},
            {'path': '/c/fileB.txt', 'size': 200},
            {'path': '/c/fileC.txt', 'size': 100},
            {'path': '/c/fileD.txt', 'size': 300},
            {'path': '/c/fileE.txt', 'size': 200},
            {'path': '/c/empty.txt', 'size': 0} # Empty files should be ignored for duplicates
        ]

        duplicates = validator.find_duplicate_files(file_info)
        self.assertEqual(len(duplicates), 2)
        self.assertIn('hash123', duplicates)
        self.assertIn('hash456', duplicates)
        self.assertEqual(set(duplicates['hash123']), {'/c/fileA.txt', '/c/fileC.txt'})
        self.assertEqual(set(duplicates['hash456']), {'/c/fileB.txt', '/c/fileE.txt'})

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isfile', return_value=True)
    def test_calculate_file_hash(self, mock_isfile, mock_open):
        # Mock rationale: Simulate reading file content without actual file system access.
        mock_file_content = b'test content for hashing'
        mock_open.return_value.read.side_effect = [mock_file_content, b''] # Read once, then EOF

        expected_hash = hashlib.sha256(mock_file_content).hexdigest()
        actual_hash = validator.calculate_file_hash('/dummy/path.txt')
        self.assertEqual(actual_hash, expected_hash)
        mock_open.assert_called_once_with('/dummy/path.txt', 'rb')

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir', return_value=True)
    @patch('validator.get_file_info')
    @patch('validator.find_empty_files')
    @patch('validator.find_large_files')
    @patch('validator.find_duplicate_files')
    def test_main_no_issues(self, mock_find_duplicates, mock_find_large, mock_find_empty, mock_get_file_info, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Isolate the main function's reporting logic from file system and core logic.
        mock_get_file_info.return_value = [{'path': '/d/file.txt', 'size': 100}]
        mock_find_empty.return_value = []
        mock_find_large.return_value = []
        mock_find_duplicates.return_value = {}

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/test_dir', max_size=100)):
            validator.main()
            output = mock_stdout.getvalue()
            self.assertIn('No issues found. Your stash is pristine!', output)
            self.assertIn('Total files scanned: 1', output)
            self.assertIn('Total issues found: 0', output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir', return_value=True)
    @patch('validator.get_file_info')
    @patch('validator.find_empty_files')
    @patch('validator.find_large_files')
    @patch('validator.find_duplicate_files')
    def test_main_with_issues(self, mock_find_duplicates, mock_find_large, mock_find_empty, mock_get_file_info, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Isolate the main function's reporting logic from file system and core logic.
        mock_get_file_info.return_value = [
            {'path': '/e/empty.txt', 'size': 0},
            {'path': '/e/large.bin', 'size': 15 * 1024 * 1024},
            {'path': '/e/dup1.txt', 'size': 100},
            {'path': '/e/dup2.txt', 'size': 100}
        ]
        mock_find_empty.return_value = ['/e/empty.txt']
        mock_find_large.return_value = [{'path': '/e/large.bin', 'size_mb': 15.0}]
        mock_find_duplicates.return_value = {'hash_val': ['/e/dup1.txt', '/e/dup2.txt']}

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/test_dir', max_size=10)):
            validator.main()
            output = mock_stdout.getvalue()
            self.assertIn('[!] Found 1 empty files:', output)
            self.assertIn('/e/empty.txt', output)
            self.assertIn('[!] Found 1 large files (exceeds 10 MB):', output)
            self.assertIn('/e/large.bin (15.0 MB)', output)
            self.assertIn('[!] Found 1 sets of duplicate files:', output)
            self.assertIn('Group 1 (SHA256: hash_val...', output)
            self.assertIn('/e/dup1.txt', output)
            self.assertIn('/e/dup2.txt', output)
            self.assertIn('Total files scanned: 4', output)
            self.assertIn('Total issues found: 3', output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir', return_value=False)
    def test_main_invalid_path(self, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Simulate an invalid directory path without actual file system interaction.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/nonexistent', max_size=100)):
            with self.assertRaises(SystemExit) as cm:
                validator.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Directory '/nonexistent' not found or is not a directory.", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
