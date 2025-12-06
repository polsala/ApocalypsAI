import unittest
import sys
from unittest.mock import patch, mock_open
import os

# Mock rationale: We need to simulate file system operations (reading files, checking existence)
# without actually touching the disk. This ensures tests are deterministic, fast, and isolated
# from the host environment's file system state.

# Add the src directory to the path to allow importing checksum_buddy
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import checksum_buddy
sys.path.pop(0)

class TestChecksumBuddy(unittest.TestCase):

    def setUp(self):
        # Define some test file contents and their expected checksums
        self.test_file_content_small = b"Hello, ApocalypsAI!"
        self.test_file_content_large = b"" # Simulate a larger file
        for i in range(1000):
            self.test_file_content_large += b"This is a line of content for a larger file. " + str(i).encode() + b"\n"

        # Pre-calculated checksums for 'Hello, ApocalypsAI!'
        self.sha256_small = '0e255554625b0f49622522770519199346618520786961204098481358056215'
        self.md5_small = '0a492160291129990861110034a7428e'

        # Pre-calculated checksums for the 'large' content
        # Using a fixed seed for content generation ensures this is deterministic
        import hashlib
        hasher_sha256_large = hashlib.sha256()
        hasher_md5_large = hashlib.md5()
        hasher_sha256_large.update(self.test_file_content_large)
        hasher_md5_large.update(self.test_file_content_large)
        self.sha256_large = hasher_sha256_large.hexdigest()
        self.md5_large = hasher_md5_large.hexdigest()

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data=b'test data')
    def test_calculate_checksum_sha256(self, mock_file, mock_exists):
        # Mock rationale: We mock os.path.exists to confirm the file is 'present'
        # and builtins.open to provide specific 'test data' without actual file I/O.
        expected_checksum = '912ec803b2ce49e4a541068d495ab57037581111d13774849d401564e2621081'
        checksum = checksum_buddy.calculate_checksum('/fake/path/file.txt', 'sha256')
        self.assertEqual(checksum, expected_checksum)
        mock_exists.assert_called_once_with('/fake/path/file.txt')
        mock_file.assert_called_once_with('/fake/path/file.txt', 'rb')

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data=b'test data')
    def test_calculate_checksum_md5(self, mock_file, mock_exists):
        # Mock rationale: Same as above, ensuring MD5 calculation works with mocked file content.
        expected_checksum = 'f1d2d2f924e986ac86eab403177164d0'
        checksum = checksum_buddy.calculate_checksum('/fake/path/file.txt', 'md5')
        self.assertEqual(checksum, expected_checksum)
        mock_exists.assert_called_once_with('/fake/path/file.txt')
        mock_file.assert_called_once_with('/fake/path/file.txt', 'rb')

    @patch('os.path.exists', return_value=False)
    def test_calculate_checksum_file_not_found(self, mock_exists):
        # Mock rationale: We mock os.path.exists to simulate a non-existent file,
        # verifying the FileNotFoundError is raised correctly.
        with self.assertRaises(FileNotFoundError):
            checksum_buddy.calculate_checksum('/nonexistent/file.txt', 'sha256')
        mock_exists.assert_called_once_with('/nonexistent/file.txt')

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    def test_calculate_checksum_empty_file(self, mock_file, mock_exists):
        # Mock rationale: Test with an empty file content to ensure correct checksum generation.
        sha256_empty = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        md5_empty = 'd41d8cd98f00b204e9800998ecf8427e'

        checksum_sha256 = checksum_buddy.calculate_checksum('/fake/path/empty.txt', 'sha256')
        self.assertEqual(checksum_sha256, sha256_empty)

        checksum_md5 = checksum_buddy.calculate_checksum('/fake/path/empty.txt', 'md5')
        self.assertEqual(checksum_md5, md5_empty)

    @patch('os.path.exists', return_value=True)
    def test_calculate_checksum_io_error(self, mock_exists):
        # Mock rationale: Simulate an IOError during file reading to ensure error handling.
        with patch('builtins.open', side_effect=IOError('Permission denied')) as mock_file:
            with self.assertRaisesRegex(IOError, 'Permission denied'):
                checksum_buddy.calculate_checksum('/fake/path/unreadable.txt', 'sha256')
            mock_file.assert_called_once_with('/fake/path/unreadable.txt', 'rb')

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('os.path.exists', return_value=True)
    def test_main_generate_sha256(self, mock_exists, mock_stderr, mock_stdout):
        # Mock rationale: We mock sys.stdout and sys.stderr to capture printed output
        # and os.path.exists to simulate file presence. We also mock builtins.open
        # to provide specific content for checksum calculation.
        with patch('builtins.open', new_callable=mock_open, read_data=self.test_file_content_small) as mock_file:
            test_args = ['checksum_buddy.py', 'generate', '--file', '/fake/path/small.txt', '--algorithm', 'sha256']
            with patch('sys.argv', test_args):
                checksum_buddy.main()
                self.assertIn(f"Checksum (SHA256): {self.sha256_small}", mock_stdout.getvalue())
            mock_exists.assert_called_once_with('/fake/path/small.txt')
            mock_file.assert_called_once_with('/fake/path/small.txt', 'rb')

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('os.path.exists', return_value=True)
    def test_main_generate_md5(self, mock_exists, mock_stderr, mock_stdout):
        # Mock rationale: Same as above, but for MD5 generation.
        with patch('builtins.open', new_callable=mock_open, read_data=self.test_file_content_small) as mock_file:
            test_args = ['checksum_buddy.py', 'generate', '--file', '/fake/path/small.txt', '--algorithm', 'md5']
            with patch('sys.argv', test_args):
                checksum_buddy.main()
                self.assertIn(f"Checksum (MD5): {self.md5_small}", mock_stdout.getvalue())
            mock_exists.assert_called_once_with('/fake/path/small.txt')
            mock_file.assert_called_once_with('/fake/path/small.txt', 'rb')

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('os.path.exists', return_value=True)
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    def test_main_verify_match(self, mock_exit, mock_exists, mock_stderr, mock_stdout):
        # Mock rationale: We mock sys.stdout, sys.stderr, os.path.exists, and builtins.open
        # to simulate a successful checksum verification. sys.exit is mocked to prevent test termination.
        with patch('builtins.open', new_callable=mock_open, read_data=self.test_file_content_small) as mock_file:
            test_args = ['checksum_buddy.py', 'verify', '--file', '/fake/path/small.txt',
                         '--expected-checksum', self.sha256_small, '--algorithm', 'sha256']
            with patch('sys.argv', test_args):
                checksum_buddy.main()
                self.assertIn("Checksum MATCHES!", mock_stdout.getvalue())
                mock_exit.assert_called_once_with(0)
            mock_exists.assert_called_once_with('/fake/path/small.txt')
            mock_file.assert_called_once_with('/fake/path/small.txt', 'rb')

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('os.path.exists', return_value=True)
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    def test_main_verify_mismatch(self, mock_exit, mock_exists, mock_stderr, mock_stdout):
        # Mock rationale: Same as above, but simulating a checksum mismatch.
        with patch('builtins.open', new_callable=mock_open, read_data=self.test_file_content_small) as mock_file:
            test_args = ['checksum_buddy.py', 'verify', '--file', '/fake/path/small.txt',
                         '--expected-checksum', 'a' * len(self.sha256_small), '--algorithm', 'sha256'] # Incorrect hash
            with patch('sys.argv', test_args):
                checksum_buddy.main()
                self.assertIn("Checksum MISMATCH!", mock_stdout.getvalue())
                mock_exit.assert_called_once_with(1)
            mock_exists.assert_called_once_with('/fake/path/small.txt')
            mock_file.assert_called_once_with('/fake/path/small.txt', 'rb')

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('os.path.exists', return_value=False)
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    def test_main_file_not_found_error(self, mock_exit, mock_exists, mock_stderr, mock_stdout):
        # Mock rationale: Simulate a FileNotFoundError during main execution.
        test_args = ['checksum_buddy.py', 'generate', '--file', '/nonexistent/file.txt']
        with patch('sys.argv', test_args):
            checksum_buddy.main()
            self.assertIn("Error: File not found: /nonexistent/file.txt", mock_stderr.getvalue())
            mock_exit.assert_called_once_with(1)
        mock_exists.assert_called_once_with('/nonexistent/file.txt')

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('os.path.exists', return_value=True)
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    def test_main_io_error_during_read(self, mock_exit, mock_exists, mock_stderr, mock_stdout):
        # Mock rationale: Simulate an IOError during file reading within the main function.
        with patch('builtins.open', side_effect=IOError('Disk full')) as mock_file:
            test_args = ['checksum_buddy.py', 'generate', '--file', '/fake/path/unreadable.txt']
            with patch('sys.argv', test_args):
                checksum_buddy.main()
                self.assertIn("Error: Error reading file /fake/path/unreadable.txt: Disk full", mock_stderr.getvalue())
                mock_exit.assert_called_once_with(1)
            mock_exists.assert_called_once_with('/fake/path/unreadable.txt')
            mock_file.assert_called_once_with('/fake/path/unreadable.txt', 'rb')

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('os.path.exists', return_value=True)
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    def test_main_large_file_sha256(self, mock_exit, mock_exists, mock_stderr, mock_stdout):
        # Mock rationale: Test with a larger mocked file content to ensure chunking works correctly.
        with patch('builtins.open', new_callable=mock_open, read_data=self.test_file_content_large) as mock_file:
            test_args = ['checksum_buddy.py', 'generate', '--file', '/fake/path/large.txt', '--algorithm', 'sha256']
            with patch('sys.argv', test_args):
                checksum_buddy.main()
                self.assertIn(f"Checksum (SHA256): {self.sha256_large}", mock_stdout.getvalue())
            mock_exists.assert_called_once_with('/fake/path/large.txt')
            mock_file.assert_called_once_with('/fake/path/large.txt', 'rb')

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('os.path.exists', return_value=True)
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    def test_main_large_file_md5(self, mock_exit, mock_exists, mock_stderr, mock_stdout):
        # Mock rationale: Test with a larger mocked file content to ensure chunking works correctly for MD5.
        with patch('builtins.open', new_callable=mock_open, read_data=self.test_file_content_large) as mock_file:
            test_args = ['checksum_buddy.py', 'generate', '--file', '/fake/path/large.txt', '--algorithm', 'md5']
            with patch('sys.argv', test_args):
                checksum_buddy.main()
                self.assertIn(f"Checksum (MD5): {self.md5_large}", mock_stdout.getvalue())
            mock_exists.assert_called_once_with('/fake/path/large.txt')
            mock_file.assert_called_once_with('/fake/path/large.txt', 'rb')
