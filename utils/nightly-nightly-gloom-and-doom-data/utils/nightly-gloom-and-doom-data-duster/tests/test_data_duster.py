import unittest
import os
import time
import hashlib
from unittest.mock import patch, mock_open
from src.data_duster import scan_directory, generate_report, get_file_hash

# Mock rationale:
# os.walk: Simulates directory structure traversal without actual file system access.
# os.path.isdir: Controls whether the target path is considered a directory.
# os.path.getmtime: Provides deterministic modification times for files.
# os.path.getsize: Provides deterministic file sizes.
# open: Mocks file content reading for hashing, ensuring deterministic hashes.
# time.time: Fixes the "current time" for age calculations, making tests repeatable.
# print: Captures console output to verify report generation.

class TestDataDuster(unittest.TestCase):

    # Define a fixed current time for deterministic age calculations
    MOCK_CURRENT_TIME = time.mktime(time.strptime("2023-01-01 12:00:00", "%Y-%m-%d %H:%M:%S"))

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_directory_empty(self, mock_open_func, mock_getsize, mock_getmtime, mock_walk, mock_isdir, mock_time):
        """Test scanning an empty directory."""
        mock_walk.return_value = [
            ('/mock/path', [], [])
        ]
        results = scan_directory('/mock/path', age_days=365, size_mb=100, detect_duplicates=False)
        self.assertEqual(len(results['old_files']), 0)
        self.assertEqual(len(results['large_files']), 0)
        self.assertEqual(len(results['duplicate_files']), 0)

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_directory_old_files(self, mock_open_func, mock_getsize, mock_getmtime, mock_walk, mock_isdir, mock_time):
        """Test detection of old files."""
        # File modified 2 years ago (older than 365 days threshold)
        old_file_mtime = self.MOCK_CURRENT_TIME - (2 * 365 * 24 * 60 * 60)
        # File modified 6 months ago (not older than 365 days threshold)
        recent_file_mtime = self.MOCK_CURRENT_TIME - (0.5 * 365 * 24 * 60 * 60)

        mock_walk.return_value = [
            ('/mock/path', [], ['old_doc.txt', 'recent_report.pdf'])
        ]
        mock_getmtime.side_effect = lambda p: {
            '/mock/path/old_doc.txt': old_file_mtime,
            '/mock/path/recent_report.pdf': recent_file_mtime,
        }.get(p, self.MOCK_CURRENT_TIME)
        mock_getsize.return_value = 10 # Small size, not relevant for age test

        results = scan_directory('/mock/path', age_days=365, size_mb=100, detect_duplicates=False)
        self.assertEqual(len(results['old_files']), 1)
        self.assertEqual(results['old_files'][0][0], '/mock/path/old_doc.txt')
        self.assertEqual(results['old_files'][0][1], old_file_mtime)

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_directory_large_files(self, mock_open_func, mock_getsize, mock_getmtime, mock_walk, mock_isdir, mock_time):
        """Test detection of large files."""
        # Large file (200MB, larger than 100MB threshold)
        large_file_size = 200 * 1024 * 1024
        # Small file (50MB, not larger than 100MB threshold)
        small_file_size = 50 * 1024 * 1024

        mock_walk.return_value = [
            ('/mock/path', [], ['huge_archive.zip', 'small_image.jpg'])
        ]
        mock_getmtime.return_value = self.MOCK_CURRENT_TIME # Not relevant for size test
        mock_getsize.side_effect = lambda p: {
            '/mock/path/huge_archive.zip': large_file_size,
            '/mock/path/small_image.jpg': small_file_size,
        }.get(p, 10)

        results = scan_directory('/mock/path', age_days=365, size_mb=100, detect_duplicates=False)
        self.assertEqual(len(results['large_files']), 1)
        self.assertEqual(results['large_files'][0][0], '/mock/path/huge_archive.zip')
        self.assertEqual(results['large_files'][0][1], large_file_size)

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_directory_duplicate_files(self, mock_open_func, mock_getsize, mock_getmtime, mock_walk, mock_isdir, mock_time):
        """Test detection of duplicate files."""
        mock_walk.return_value = [
            ('/mock/path', [], ['fileA.txt', 'fileB.txt', 'fileC.txt'])
        ]
        mock_getmtime.return_value = self.MOCK_CURRENT_TIME
        mock_getsize.return_value = 100 # Not relevant for duplicate test

        # Mock file content for hashing
        mock_open_func.side_effect = [
            mock_open(read_data=b"content of file A").return_value, # fileA.txt
            mock_open(read_data=b"content of file A").return_value, # fileB.txt (duplicate of A)
            mock_open(read_data=b"content of file C").return_value, # fileC.txt
        ]

        results = scan_directory('/mock/path', age_days=365, size_mb=100, detect_duplicates=True)
        self.assertEqual(len(results['duplicate_files']), 1)
        # The hash for "content of file A"
        expected_hash = hashlib.sha256(b"content of file A").hexdigest()
        self.assertEqual(results['duplicate_files'][0][0], expected_hash)
        self.assertIn('/mock/path/fileA.txt', results['duplicate_files'][0][1])
        self.assertIn('/mock/path/fileB.txt', results['duplicate_files'][0][1])
        self.assertEqual(len(results['duplicate_files'][0][1]), 2)

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.isdir', return_value=False)
    def test_scan_directory_invalid_path(self, mock_isdir, mock_time):
        """Test scanning with an invalid path."""
        with self.assertRaises(ValueError) as cm:
            scan_directory('/nonexistent/path', age_days=365, size_mb=100, detect_duplicates=False)
        self.assertIn("not a valid directory", str(cm.exception))

    @patch('sys.stdout')
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    def test_generate_report_empty(self, mock_time, mock_stdout):
        """Test report generation for empty results."""
        results = {
            'old_files': [],
            'large_files': [],
            'duplicate_files': []
        }
        generate_report(results)
        output = mock_stdout.write.call_args[0][0]
        self.assertIn("No ancient artifacts found", output)
        self.assertIn("No bloated behemoths found", output)
        self.assertIn("No insidious duplicates found", output)

    @patch('sys.stdout')
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    def test_generate_report_full(self, mock_time, mock_stdout):
        """Test report generation with all types of findings."""
        old_file_mtime = self.MOCK_CURRENT_TIME - (2 * 365 * 24 * 60 * 60)
        large_file_size = 200 * 1024 * 1024
        duplicate_hash = hashlib.sha256(b"duplicate content").hexdigest()

        results = {
            'old_files': [('/mock/path/old.log', old_file_mtime)],
            'large_files': [('/mock/path/huge.iso', large_file_size)],
            'duplicate_files': [(duplicate_hash, ['/mock/path/dup1.txt', '/mock/path/dup2.txt'])]
        }
        generate_report(results)
        output = mock_stdout.write.call_args[0][0]

        self.assertIn("Ancient Artifacts", output)
        self.assertIn("/mock/path/old.log", output)
        self.assertIn("Bloated Behemoths", output)
        self.assertIn("/mock/path/huge.iso", output)
        self.assertIn("Insidious Duplicates", output)
        self.assertIn(duplicate_hash[:10], output)
        self.assertIn("/mock/path/dup1.txt", output)
        self.assertIn("/mock/path/dup2.txt", output)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout')
    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    def test_generate_report_to_file(self, mock_time, mock_stdout, mock_open_func):
        """Test report generation to a file."""
        results = {
            'old_files': [], 'large_files': [], 'duplicate_files': []
        }
        output_filename = "test_report.txt"
        generate_report(results, output_file=output_filename)

        mock_open_func.assert_called_once_with(output_filename, 'w')
        handle = mock_open_func()
        self.assertTrue(handle.write.called)
        self.assertIn("Report saved to test_report.txt", mock_stdout.write.call_args[0][0])

    def test_get_file_hash(self):
        """Test file hashing utility."""
        mock_file_content = b"This is some test content for hashing."
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            expected_hash = hashlib.sha256(mock_file_content).hexdigest()
            actual_hash = get_file_hash("dummy_path.txt")
            self.assertEqual(actual_hash, expected_hash)

if __name__ == '__main__':
    unittest.main()
