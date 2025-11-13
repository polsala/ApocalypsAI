import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, mock_open
from src.scavenger import ResourceScavenger

class TestResourceScavenger(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)

        # Create some dummy files and directories
        os.makedirs(os.path.join(self.test_dir, 'subdir1'))
        os.makedirs(os.path.join(self.test_dir, 'subdir2'))

        # Small file
        with open(os.path.join(self.test_dir, 'small.txt'), 'w') as f:
            f.write('a' * 100) # 100 bytes

        # Large file (relative to 1MB min_size for tests)
        self.large_file_path = os.path.join(self.test_dir, 'subdir1', 'large.bin')
        with open(self.large_file_path, 'wb') as f:
            f.write(b'b' * (2 * 1024 * 1024)) # 2 MB

        # Another large file
        self.another_large_file_path = os.path.join(self.test_dir, 'subdir2', 'huge.data')
        with open(self.another_large_file_path, 'wb') as f:
            f.write(b'c' * (3 * 1024 * 1024)) # 3 MB

        # Duplicate files
        self.dup_file1_path = os.path.join(self.test_dir, 'doc1.txt')
        self.dup_file2_path = os.path.join(self.test_dir, 'subdir1', 'doc_copy.txt')
        self.dup_content = 'This is duplicate content.'
        with open(self.dup_file1_path, 'w') as f:
            f.write(self.dup_content)
        with open(self.dup_file2_path, 'w') as f:
            f.write(self.dup_content)
        
        # Unique file with same size as duplicates but different content
        self.unique_file_path = os.path.join(self.test_dir, 'unique.txt')
        with open(self.unique_file_path, 'w') as f:
            f.write('This is unique content.')

        # Empty file
        with open(os.path.join(self.test_dir, 'empty.log'), 'w') as f:
            pass

    @patch('src.scavenger.hashlib.md5')
    def test_scan_for_large_files(self, mock_md5):
        # Mock rationale: hashlib.md5 is not directly involved in large file scanning.
        # It's patched to ensure tests are isolated and don't rely on its behavior for this specific test.
        # The actual hashing logic is tested separately in find_duplicate_files.
        scavenger = ResourceScavenger(self.test_dir, min_size_mb=1)
        scavenger.scan_for_large_files()

        self.assertEqual(len(scavenger.large_files), 2)
        # Check if the large files are correctly identified and sorted by size (descending)
        self.assertEqual(scavenger.large_files[0][0], self.another_large_file_path)
        self.assertAlmostEqual(scavenger.large_files[0][1], 3 * 1024 * 1024)
        self.assertEqual(scavenger.large_files[1][0], self.large_file_path)
        self.assertAlmostEqual(scavenger.large_files[1][1], 2 * 1024 * 1024)

        # Test with a higher min_size_mb, expecting no large files
        scavenger_high_threshold = ResourceScavenger(self.test_dir, min_size_mb=5)
        scavenger_high_threshold.scan_for_large_files()
        self.assertEqual(len(scavenger_high_threshold.large_files), 0)

    @patch('builtins.open', new_callable=mock_open)
    @patch('src.scavenger.hashlib.md5')
    def test_find_duplicate_files(self, mock_md5_constructor, mock_builtin_open):
        # Mock rationale: `builtins.open` is mocked to prevent actual file I/O during hash calculation,
        # making the test faster and independent of file system state. `hashlib.md5` is mocked
        # to return predictable hash values for specific file contents, ensuring deterministic tests.
        # This allows us to control the 'content' of files without writing them to disk repeatedly.

        # Configure mock_md5 to return specific hashes for specific contents
        mock_md5_instance = mock_md5_constructor.return_value
        mock_md5_instance.hexdigest.side_effect = [
            'hash_dup_content', # For self.dup_file1_path
            'hash_unique_content', # For self.unique_file_path
            'hash_dup_content', # For self.dup_file2_path
            'hash_large_file', # For self.large_file_path (if processed)
            'hash_another_large_file', # For self.another_large_file_path (if processed)
            'hash_small_file', # For small.txt (if processed)
            'hash_empty_file' # For empty.log (if processed)
        ]

        # Configure mock_open to return specific content for specific files
        def mock_open_side_effect(file_path, mode='r', **kwargs):
            if file_path == self.dup_file1_path or file_path == self.dup_file2_path:
                return mock_open(read_data=self.dup_content).return_value
            elif file_path == self.unique_file_path:
                return mock_open(read_data='This is unique content.').return_value
            elif file_path == os.path.join(self.test_dir, 'small.txt'):
                return mock_open(read_data='a' * 100).return_value
            elif file_path == self.large_file_path:
                return mock_open(read_data=b'b' * (2 * 1024 * 1024)).return_value
            elif file_path == self.another_large_file_path:
                return mock_open(read_data=b'c' * (3 * 1024 * 1024)).return_value
            elif file_path == os.path.join(self.test_dir, 'empty.log'):
                return mock_open(read_data='').return_value
            else:
                # Fallback for other files if needed, or raise an error for unexpected access
                raise FileNotFoundError(f"Unexpected file access: {file_path}")

        mock_builtin_open.side_effect = mock_open_side_effect

        scavenger = ResourceScavenger(self.test_dir, min_size_mb=1)
        scavenger.find_duplicate_files()

        self.assertEqual(len(scavenger.duplicate_files), 1)
        self.assertIn('hash_dup_content', scavenger.duplicate_files)
        self.assertCountEqual(
            scavenger.duplicate_files['hash_dup_content'],
            [self.dup_file1_path, self.dup_file2_path]
        )

        # Ensure unique file is not marked as duplicate
        self.assertNotIn('hash_unique_content', scavenger.duplicate_files)

        # Test with no duplicates
        # Create a new temp dir with no duplicates
        no_dup_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, no_dup_dir)
        with open(os.path.join(no_dup_dir, 'fileA.txt'), 'w') as f: f.write('contentA')
        with open(os.path.join(no_dup_dir, 'fileB.txt'), 'w') as f: f.write('contentB')

        # Reset mocks for the new scavenger instance
        mock_md5_instance.hexdigest.side_effect = ['hashA', 'hashB']
        mock_builtin_open.side_effect = lambda fp, mode='r', **kwargs: (
            mock_open(read_data='contentA').return_value if 'fileA' in fp else
            mock_open(read_data='contentB').return_value
        )

        scavenger_no_dups = ResourceScavenger(no_dup_dir)
        scavenger_no_dups.find_duplicate_files()
        self.assertEqual(len(scavenger_no_dups.duplicate_files), 0)

    def test_generate_report(self):
        scavenger = ResourceScavenger(self.test_dir, min_size_mb=1)
        scavenger.large_files = [
            (self.another_large_file_path, 3 * 1024 * 1024),
            (self.large_file_path, 2 * 1024 * 1024)
        ]
        scavenger.duplicate_files = {
            'hash_dup_content': [self.dup_file1_path, self.dup_file2_path]
        }

        report = scavenger.generate_report()
        self.assertIn("--- Resource Scavenger Report ---", report)
        self.assertIn(f"Scanning: {self.test_dir}", report)
        self.assertIn("[LARGE FILES ( > 1.0 MB )]", report)
        self.assertIn(f"  - {self.another_large_file_path} (3.0 MB)", report)
        self.assertIn(f"  - {self.large_file_path} (2.0 MB)", report)
        self.assertIn("[DUPLICATE FILES]", report)
        self.assertIn("  - Hash: hash_dup_content", report)
        self.assertIn(f"    - {self.dup_file1_path}", report)
        self.assertIn(f"    - {self.dup_file2_path}", report)
        self.assertIn("--- Scavenging complete! ---", report)

    def test_generate_report_no_findings(self):
        scavenger = ResourceScavenger(self.test_dir, min_size_mb=100)
        # No large files or duplicates will be found with these settings/mocked state
        scavenger.scan_for_large_files()
        scavenger.find_duplicate_files()

        report = scavenger.generate_report()
        self.assertIn("No excessively large files detected. Good job, scavenger!", report)
        self.assertIn("No duplicate files found. Your data is uniquely precious!", report)

    def test_invalid_path(self):
        with self.assertRaises(ValueError) as cm:
            ResourceScavenger('/non/existent/path', min_size_mb=1)
        self.assertIn("not a valid directory", str(cm.exception))

    @patch('src.scavenger.os.path.getsize', side_effect=OSError('Permission denied'))
    def test_os_error_handling(self, mock_getsize):
        # Mock rationale: Simulates an OSError (e.g., permission denied) during file size retrieval.
        # This ensures the scavenger gracefully handles such errors without crashing, printing a warning instead.
        scavenger = ResourceScavenger(self.test_dir, min_size_mb=1)
        
        # Capture stdout to check warning messages
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            scavenger.scan_for_large_files()
        output = f.getvalue()
        self.assertIn("[WARNING] Could not access", output)
        self.assertEqual(len(scavenger.large_files), 0)

        f = io.StringIO()
        with redirect_stdout(f):
            scavenger.find_duplicate_files()
        output = f.getvalue()
        self.assertIn("[WARNING] Could not access", output)
        self.assertEqual(len(scavenger.duplicate_files), 0)

if __name__ == '__main__':
    unittest.main()
