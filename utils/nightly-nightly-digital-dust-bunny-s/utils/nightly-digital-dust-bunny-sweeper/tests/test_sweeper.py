import unittest
from unittest.mock import patch
import os
from src.sweeper import find_dust_bunnies

class TestSweeper(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_empty_directory(self, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with an empty directory.
        # os.path.isdir is mocked to confirm the root path is valid.
        # os.walk is mocked to return specific directory traversal results.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', ['dir1', 'empty_dir'], ['file1.txt']),
            ('/root/dir1', [], ['file2.txt']),
            ('/root/empty_dir', [], []), # This is the empty directory
        ]

        empty_dirs, pycache_dirs = find_dust_bunnies('/root')
        self.assertIn('/root/empty_dir', empty_dirs)
        self.assertEqual(len(empty_dirs), 1)
        self.assertEqual(len(pycache_dirs), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_pycache_directory(self, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with a __pycache__ directory.
        # os.path.isdir is mocked to confirm the root path is valid.
        # os.walk is mocked to return specific directory traversal results.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', ['dir1', '__pycache__'], ['file1.py']),
            ('/root/dir1', [], ['file2.py']),
            ('/root/__pycache__', ['sub_cache'], ['compiled.pyc']), # This is the __pycache__
            ('/root/__pycache__/sub_cache', [], ['another.pyc']),
        ]

        empty_dirs, pycache_dirs = find_dust_bunnies('/root')
        self.assertIn('/root/__pycache__', pycache_dirs)
        self.assertEqual(len(pycache_dirs), 1)
        self.assertEqual(len(empty_dirs), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_both_empty_and_pycache(self, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with both an empty and a __pycache__ directory.
        # os.path.isdir is mocked to confirm the root path is valid.
        # os.walk is mocked to return specific directory traversal results.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', ['empty_dir', '__pycache__'], ['main.py']),
            ('/root/empty_dir', [], []), # Empty directory
            ('/root/__pycache__', [], ['compiled.pyc']), # __pycache__ directory
        ]

        empty_dirs, pycache_dirs = find_dust_bunnies('/root')
        self.assertIn('/root/empty_dir', empty_dirs)
        self.assertIn('/root/__pycache__', pycache_dirs)
        self.assertEqual(len(empty_dirs), 1)
        self.assertEqual(len(pycache_dirs), 1)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_nothing(self, mock_walk, mock_isdir):
        # Mock rationale: Simulate a clean directory structure with no dust bunnies.
        # os.path.isdir is mocked to confirm the root path is valid.
        # os.walk is mocked to return specific directory traversal results.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file1.txt', 'file2.py']),
            ('/root/dir1', [], ['subfile.txt']),
            ('/root/dir2', ['sub_dir'], []),
            ('/root/dir2/sub_dir', [], ['another_file.md']),
        ]

        empty_dirs, pycache_dirs = find_dust_bunnies('/root')
        self.assertEqual(len(empty_dirs), 0)
        self.assertEqual(len(pycache_dirs), 0)

    @patch('os.path.isdir')
    def test_non_existent_path(self, mock_isdir):
        # Mock rationale: Simulate a non-existent root path.
        # os.path.isdir is mocked to return False for the given path.
        mock_isdir.return_value = False
        empty_dirs, pycache_dirs = find_dust_bunnies('/non_existent_path')
        self.assertEqual(len(empty_dirs), 0)
        self.assertEqual(len(pycache_dirs), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_pycache_is_not_also_empty_dir(self, mock_walk, mock_isdir):
        # Mock rationale: Ensure a __pycache__ directory, even if empty, is only reported as __pycache__.
        # os.path.isdir is mocked to confirm the root path is valid.
        # os.walk is mocked to return specific directory traversal results.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', ['__pycache__'], []),
            ('/root/__pycache__', [], []), # This __pycache__ is also empty
        ]

        empty_dirs, pycache_dirs = find_dust_bunnies('/root')
        self.assertIn('/root/__pycache__', pycache_dirs)
        self.assertEqual(len(pycache_dirs), 1)
        self.assertEqual(len(empty_dirs), 0) # Should not be counted as an empty dir too

if __name__ == '__main__':
    unittest.main()
