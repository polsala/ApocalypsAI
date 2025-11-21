import unittest
import os
from unittest.mock import patch, MagicMock
from collections import namedtuple
from pathlib import Path

# Import the function to be tested
from src.auditor import audit_directory, get_file_size_human_readable

# Mock os.walk and os.path.getsize for deterministic, offline testing
# Mock rationale: We need to simulate a file system without actually creating files
# on disk. This ensures tests are fast, deterministic, and don't have side effects.

# Helper for mocking os.walk
WalkResult = namedtuple('WalkResult', ['root', 'dirs', 'files'])

class TestApocalypseArchiveAuditor(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_empty_directory(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty directory structure.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            WalkResult('/mock/archive', [], [])
        ]
        mock_getsize.side_effect = lambda x: 0 # Should not be called for empty dir

        report = audit_directory('/mock/archive')

        self.assertEqual(report['summary']['total_files'], 0)
        self.assertEqual(report['summary']['total_size'], '0 B')
        self.assertEqual(report['summary']['total_size_bytes'], 0)
        self.assertEqual(report['file_types'], {})
        self.assertEqual(report['largest_files'], [])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.abspath', side_effect=lambda x: x) # Mock rationale: Simplify path resolution for testing.
    def test_single_level_directory(self, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Mock rationale: Simulate a directory with files at the top level.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            WalkResult('/mock/archive', [], ['file1.txt', 'image.jpg', 'doc.pdf']),
        ]
        # Mock rationale: Provide specific sizes for mocked files.
        mock_getsize.side_effect = lambda p: {
            '/mock/archive/file1.txt': 100,
            '/mock/archive/image.jpg': 5000,
            '/mock/archive/doc.pdf': 2000,
        }.get(p, 0)

        report = audit_directory('/mock/archive')

        self.assertEqual(report['summary']['total_files'], 3)
        self.assertEqual(report['summary']['total_size'], '7.91 KB')
        self.assertEqual(report['summary']['total_size_bytes'], 7100)
        self.assertEqual(report['file_types']['.txt']['count'], 1)
        self.assertEqual(report['file_types']['.jpg']['count'], 1)
        self.assertEqual(report['file_types']['.pdf']['count'], 1)
        self.assertEqual(report['file_types']['.txt']['size_bytes'], 100)
        self.assertEqual(report['file_types']['.jpg']['size_bytes'], 5000)
        self.assertEqual(report['file_types']['.pdf']['size_bytes'], 2000)
        self.assertEqual(len(report['largest_files']), 3)
        self.assertEqual(report['largest_files'][0]['path'], '/mock/archive/image.jpg')
        self.assertEqual(report['largest_files'][0]['size_bytes'], 5000)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.abspath', side_effect=lambda x: x)
    def test_multi_level_directory(self, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Mock rationale: Simulate a directory with nested subdirectories and files.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            WalkResult('/mock/archive', ['sub1', 'sub2'], ['root_file.txt']),
            WalkResult('/mock/archive/sub1', [], ['sub1_file.log', 'sub1_image.png']),
            WalkResult('/mock/archive/sub2', ['sub2_nested'], ['sub2_doc.pdf']),
            WalkResult('/mock/archive/sub2/sub2_nested', [], ['deep_data.json']),
        ]
        mock_getsize.side_effect = lambda p: {
            '/mock/archive/root_file.txt': 100,
            '/mock/archive/sub1/sub1_file.log': 200,
            '/mock/archive/sub1/sub1_image.png': 10000,
            '/mock/archive/sub2/sub2_doc.pdf': 5000,
            '/mock/archive/sub2/sub2_nested/deep_data.json': 300,
        }.get(p, 0)

        report = audit_directory('/mock/archive')

        self.assertEqual(report['summary']['total_files'], 5)
        self.assertEqual(report['summary']['total_size_bytes'], 15600) # 100+200+10000+5000+300
        self.assertEqual(report['file_types']['.txt']['count'], 1)
        self.assertEqual(report['file_types']['.log']['count'], 1)
        self.assertEqual(report['file_types']['.png']['count'], 1)
        self.assertEqual(report['file_types']['.pdf']['count'], 1)
        self.assertEqual(report['file_types']['.json']['count'], 1)
        self.assertEqual(len(report['largest_files']), 5)
        self.assertEqual(report['largest_files'][0]['path'], '/mock/archive/sub1/sub1_image.png')
        self.assertEqual(report['largest_files'][1]['path'], '/mock/archive/sub2/sub2_doc.pdf')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.abspath', side_effect=lambda x: x)
    def test_max_depth_parameter(self, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Mock rationale: Test the max_depth functionality by simulating a deep structure
        # and checking if files beyond the depth are ignored.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            WalkResult('/mock/archive', ['sub1'], ['root_file.txt']), # Depth 0
            WalkResult('/mock/archive/sub1', ['sub2'], ['sub1_file.log']), # Depth 1
            WalkResult('/mock/archive/sub1/sub2', [], ['sub2_file.json']), # Depth 2
        ]
        mock_getsize.side_effect = lambda p: {
            '/mock/archive/root_file.txt': 100,
            '/mock/archive/sub1/sub1_file.log': 200,
            '/mock/archive/sub1/sub2/sub2_file.json': 300,
        }.get(p, 0)

        # Test with depth 0 (only root directory)
        report_depth_0 = audit_directory('/mock/archive', max_depth=0)
        self.assertEqual(report_depth_0['summary']['total_files'], 1)
        self.assertEqual(report_depth_0['summary']['total_size_bytes'], 100)
        self.assertIn('.txt', report_depth_0['file_types'])
        self.assertNotIn('.log', report_depth_0['file_types'])
        self.assertNotIn('.json', report_depth_0['file_types'])

        # Test with depth 1 (root + immediate subdirectories)
        report_depth_1 = audit_directory('/mock/archive', max_depth=1)
        self.assertEqual(report_depth_1['summary']['total_files'], 2)
        self.assertEqual(report_depth_1['summary']['total_size_bytes'], 300)
        self.assertIn('.txt', report_depth_1['file_types'])
        self.assertIn('.log', report_depth_1['file_types'])
        self.assertNotIn('.json', report_depth_1['file_types'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.abspath', side_effect=lambda x: x)
    def test_top_n_largest_parameter(self, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Mock rationale: Simulate a directory with many files of varying sizes
        # and verify that only the top N largest are returned.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            WalkResult('/mock/archive', [], [f'file{i}.txt' for i in range(10)])
        ]
        # Assign distinct sizes to ensure sorting works
        mock_getsize.side_effect = lambda p: {
            f'/mock/archive/file{i}.txt': (i + 1) * 100 for i in range(10)
        }.get(p, 0)

        report = audit_directory('/mock/archive', top_n_largest=3)
        self.assertEqual(len(report['largest_files']), 3)
        self.assertEqual(report['largest_files'][0]['path'], '/mock/archive/file9.txt') # Largest
        self.assertEqual(report['largest_files'][1]['path'], '/mock/archive/file8.txt')
        self.assertEqual(report['largest_files'][2]['path'], '/mock/archive/file7.txt') # 3rd largest

    @patch('os.path.isdir')
    def test_directory_not_found(self, mock_isdir):
        # Mock rationale: Simulate the scenario where the target directory does not exist.
        mock_isdir.return_value = False
        with self.assertRaises(FileNotFoundError):
            audit_directory('/nonexistent/path')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.abspath', side_effect=lambda x: x)
    def test_files_with_no_extension(self, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Mock rationale: Test handling of files without an extension.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            WalkResult('/mock/archive', [], ['README', 'config', 'script.sh'])
        ]
        mock_getsize.side_effect = lambda p: {
            '/mock/archive/README': 100,
            '/mock/archive/config': 200,
            '/mock/archive/script.sh': 50,
        }.get(p, 0)

        report = audit_directory('/mock/archive')
        self.assertEqual(report['file_types']['[no_extension]']['count'], 2)
        self.assertEqual(report['file_types']['.sh']['count'], 1)
        self.assertEqual(report['file_types']['[no_extension]']['size_bytes'], 300)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.abspath', side_effect=lambda x: x)
    def test_os_error_on_getsize(self, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Mock rationale: Simulate a file that causes an OSError (e.g., permission denied, broken symlink).
        # The auditor should gracefully skip such files.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            WalkResult('/mock/archive', [], ['good_file.txt', 'bad_file.txt'])
        ]
        def getsize_side_effect(path):
            if 'bad_file.txt' in path:
                raise OSError("Permission denied")
            return 100
        mock_getsize.side_effect = getsize_side_effect

        report = audit_directory('/mock/archive')
        self.assertEqual(report['summary']['total_files'], 1) # Only good_file.txt counted
        self.assertEqual(report['summary']['total_size_bytes'], 100)
        self.assertIn('.txt', report['file_types'])
        self.assertEqual(report['file_types']['.txt']['count'], 1)


class TestGetFileSizeHumanReadable(unittest.TestCase):
    # Mock rationale: This is a pure function, no external dependencies to mock.
    def test_bytes(self):
        self.assertEqual(get_file_size_human_readable(0), "0 B")
        self.assertEqual(get_file_size_human_readable(100), "100.0 B")
        self.assertEqual(get_file_size_human_readable(1023), "1023.0 B")

    def test_kilobytes(self):
        self.assertEqual(get_file_size_human_readable(1024), "1.0 KB")
        self.assertEqual(get_file_size_human_readable(1536), "1.5 KB") # 1.5 * 1024
        self.assertEqual(get_file_size_human_readable(1024 * 10), "10.0 KB")

    def test_megabytes(self):
        self.assertEqual(get_file_size_human_readable(1024 * 1024), "1.0 MB")
        self.assertEqual(get_file_size_human_readable(1024 * 1024 * 2.5), "2.5 MB")

    def test_gigabytes(self):
        self.assertEqual(get_file_size_human_readable(1024**3), "1.0 GB")

    def test_terabytes(self):
        self.assertEqual(get_file_size_human_readable(1024**4), "1.0 TB")

    def test_large_number(self):
        self.assertEqual(get_file_size_human_readable(123456789012345), "112.28 TB")


if __name__ == '__main__':
    unittest.main()
