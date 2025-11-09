import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the path to allow importing optimizer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from optimizer import scan_directory, get_human_readable_size
sys.path.pop(0)

class TestOptimizer(unittest.TestCase):

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_empty_directory(self, mock_isdir, mock_walk, mock_getsize):
        # Mock rationale: Simulate an empty directory structure for testing.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_repo', [], [])
        ]
        mock_getsize.return_value = 0 # Should not be called for empty dir in this setup

        components = scan_directory('/mock_repo', 10.0)
        self.assertEqual(len(components), 0)

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_directory_with_small_files(self, mock_isdir, mock_walk, mock_getsize):
        # Mock rationale: Simulate a directory with files smaller than the threshold.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_repo', ['src', 'data'], ['small_file.txt']),
            ('/mock_repo/src', [], ['code.py']),
            ('/mock_repo/data', [], ['config.json'])
        ]
        
        # Define mock sizes for files
        def mock_getsize_side_effect(path):
            if 'small_file.txt' in path: return 1 * 1024 * 1024 # 1MB
            if 'code.py' in path: return 0.5 * 1024 * 1024 # 0.5MB
            if 'config.json' in path: return 0.1 * 1024 * 1024 # 0.1MB
            return 0 # Default for directories or other paths

        mock_getsize.side_effect = mock_getsize_side_effect

        components = scan_directory('/mock_repo', 10.0)
        self.assertEqual(len(components), 0)

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_directory_with_large_files_and_dirs(self, mock_isdir, mock_walk, mock_getsize):
        # Mock rationale: Simulate a complex directory structure with files and directories exceeding the threshold.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_repo', ['build', 'data', 'src'], ['README.md']),
            ('/mock_repo/build', [], ['large_artifact.zip', 'temp.log']),
            ('/mock_repo/data', [], ['huge_dataset.csv', 'small_data.json']),
            ('/mock_repo/src', [], ['main.py'])
        ]

        def mock_getsize_side_effect(path):
            if 'README.md' in path: return 0.01 * 1024 * 1024 # 0.01MB
            if 'large_artifact.zip' in path: return 150 * 1024 * 1024 # 150MB
            if 'temp.log' in path: return 5 * 1024 * 1024 # 5MB
            if 'huge_dataset.csv' in path: return 75 * 1024 * 1024 # 75MB
            if 'small_data.json' in path: return 0.2 * 1024 * 1024 # 0.2MB
            if 'main.py' in path: return 0.05 * 1024 * 1024 # 0.05MB
            return 0 # Default for directories or other paths

        mock_getsize.side_effect = mock_getsize_side_effect

        components = scan_directory('/mock_repo', 10.0)
        
        # Expected components based on the refined directory size calculation:
        # /mock_repo/build: 150MB (large_artifact.zip) + 5MB (temp.log) = 155MB
        # /mock_repo/data: 75MB (huge_dataset.csv) + 0.2MB (small_data.json) = 75.2MB
        # /mock_repo/src: 0.05MB (main.py)
        # /mock_repo: 0.01MB (README.md) + 155MB (build) + 75.2MB (data) + 0.05MB (src) = ~230.26MB

        # Expected heavy components (threshold 10MB), sorted by size descending:
        # 1. /mock_repo/build (DIR, 155MB)
        # 2. /mock_repo/data (DIR, 75.2MB)
        # 3. /mock_repo/data/huge_dataset.csv (FILE, 75MB)

        self.assertEqual(len(components), 3)
        
        # Verify the largest component
        self.assertEqual(components[0][1], 'DIR')
        self.assertEqual(components[0][2], '/mock_repo/build')
        self.assertAlmostEqual(components[0][0], 155 * 1024 * 1024)

        # Verify the second largest component
        self.assertEqual(components[1][1], 'DIR')
        self.assertEqual(components[1][2], '/mock_repo/data')
        self.assertAlmostEqual(components[1][0], 75.2 * 1024 * 1024)

        # Verify the third largest component
        self.assertEqual(components[2][1], 'FILE')
        self.assertEqual(components[2][2], '/mock_repo/data/huge_dataset.csv')
        self.assertAlmostEqual(components[2][0], 75 * 1024 * 1024)

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_custom_threshold(self, mock_isdir, mock_walk, mock_getsize):
        # Mock rationale: Test with a different size threshold to ensure filtering works correctly.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_repo', [], ['file1.bin', 'file2.bin', 'file3.bin'])
        ]

        def mock_getsize_side_effect(path):
            if 'file1.bin' in path: return 20 * 1024 * 1024 # 20MB
            if 'file2.bin' in path: return 5 * 1024 * 1024  # 5MB
            if 'file3.bin' in path: return 30 * 1024 * 1024 # 30MB
            return 0

        mock_getsize.side_effect = mock_getsize_side_effect

        # Test with threshold 25MB
        components = scan_directory('/mock_repo', 25.0)
        self.assertEqual(len(components), 1)
        self.assertEqual(components[0][1], 'FILE')
        self.assertEqual(components[0][2], '/mock_repo/file3.bin')
        self.assertAlmostEqual(components[0][0], 30 * 1024 * 1024)

        # Test with threshold 15MB
        components = scan_directory('/mock_repo', 15.0)
        self.assertEqual(len(components), 2)
        self.assertEqual(components[0][1], 'FILE')
        self.assertEqual(components[0][2], '/mock_repo/file3.bin')
        self.assertAlmostEqual(components[0][0], 30 * 1024 * 1024)
        self.assertEqual(components[1][1], 'FILE')
        self.assertEqual(components[1][2], '/mock_repo/file1.bin')
        self.assertAlmostEqual(components[1][0], 20 * 1024 * 1024)

    def test_get_human_readable_size(self):
        # Mock rationale: Test the size formatting utility function.
        self.assertEqual(get_human_readable_size(0), "0.00 B")
        self.assertEqual(get_human_readable_size(500), "500.00 B")
        self.assertEqual(get_human_readable_size(1024), "1.00 KB")
        self.assertEqual(get_human_readable_size(1024 * 1024), "1.00 MB")
        self.assertEqual(get_human_readable_size(1.5 * 1024 * 1024 * 1024), "1.50 GB")
        self.assertEqual(get_human_readable_size(1024 * 1024 * 1024 * 1024), "1.00 TB")
        self.assertEqual(get_human_readable_size(None), "N/A")

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_unreadable_file_handling(self, mock_isdir, mock_walk, mock_getsize):
        # Mock rationale: Ensure the scanner handles files for which getsize raises an OSError (e.g., permission denied, broken symlink) gracefully.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_repo', [], ['readable.txt', 'unreadable.txt'])
        ]

        def mock_getsize_side_effect(path):
            if 'readable.txt' in path: return 20 * 1024 * 1024 # 20MB
            if 'unreadable.txt' in path: raise OSError("Permission denied")
            return 0

        mock_getsize.side_effect = mock_getsize_side_effect

        components = scan_directory('/mock_repo', 10.0)
        self.assertEqual(len(components), 1)
        self.assertEqual(components[0][2], '/mock_repo/readable.txt')

if __name__ == '__main__':
    unittest.main()
