import unittest
import os
import tempfile
import shutil
import hashlib
from unittest.mock import patch, mock_open
from src.echo_monitor import find_duplicates, calculate_file_hash

class TestEchoMonitor(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing file operations
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def _create_file(self, filename, content):
        """Helper to create a file in the test directory."""
        filepath = os.path.join(self.test_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath

    def test_calculate_file_hash_basic(self):
        filepath = self._create_file("test_file.txt", "hello world")
        expected_hash = hashlib.sha256(b"hello world").hexdigest()
        self.assertEqual(calculate_file_hash(filepath), expected_hash)

    def test_calculate_file_hash_empty_file(self):
        filepath = self._create_file("empty.txt", "")
        expected_hash = hashlib.sha256(b"").hexdigest()
        self.assertEqual(calculate_file_hash(filepath), expected_hash)

    def test_calculate_file_hash_non_existent_file(self):
        # Mock rationale: We want to test the error handling for non-existent files
        # without actually creating a file or relying on OS errors.
        with patch('builtins.open', side_effect=IOError("No such file or directory")):
            self.assertIsNone(calculate_file_hash("/non/existent/path.txt"))

    def test_find_duplicates_no_duplicates(self):
        self._create_file("file1.txt", "content A")
        self._create_file("file2.txt", "content B")
        self._create_file("subdir/file3.txt", "content C")
        
        duplicates = find_duplicates(self.test_dir)
        self.assertEqual(len(duplicates), 0)

    def test_find_duplicates_simple_duplicates(self):
        filepath1 = self._create_file("file1.txt", "duplicate content")
        filepath2 = self._create_file("file2.txt", "duplicate content")
        self._create_file("file3.txt", "unique content")

        duplicates = find_duplicates(self.test_dir)
        self.assertEqual(len(duplicates), 1)
        
        # Get the hash of the duplicate content
        duplicate_hash = hashlib.sha256(b"duplicate content").hexdigest()
        self.assertIn(duplicate_hash, duplicates)
        self.assertCountEqual(duplicates[duplicate_hash], [filepath1, filepath2])

    def test_find_duplicates_multiple_sets(self):
        filepath_a1 = self._create_file("a1.txt", "content A")
        filepath_a2 = self._create_file("a2.txt", "content A")
        filepath_b1 = self._create_file("b1.txt", "content B")
        filepath_b2 = self._create_file("b2.txt", "content B")
        self._create_file("c1.txt", "content C")

        duplicates = find_duplicates(self.test_dir)
        self.assertEqual(len(duplicates), 2)

        hash_a = hashlib.sha256(b"content A").hexdigest()
        hash_b = hashlib.sha256(b"content B").hexdigest()

        self.assertIn(hash_a, duplicates)
        self.assertCountEqual(duplicates[hash_a], [filepath_a1, filepath_a2])
        self.assertIn(hash_b, duplicates)
        self.assertCountEqual(duplicates[hash_b], [filepath_b1, filepath_b2])

    def test_find_duplicates_across_subdirectories(self):
        filepath1 = self._create_file("dir1/file1.txt", "shared content")
        filepath2 = self._create_file("dir2/file2.txt", "shared content")
        filepath3 = self._create_file("dir1/unique.txt", "unique content")

        duplicates = find_duplicates(self.test_dir)
        self.assertEqual(len(duplicates), 1)
        
        shared_hash = hashlib.sha256(b"shared content").hexdigest()
        self.assertIn(shared_hash, duplicates)
        self.assertCountEqual(duplicates[shared_hash], [filepath1, filepath2])

    def test_find_duplicates_empty_files_are_duplicates(self):
        filepath1 = self._create_file("empty1.txt", "")
        filepath2 = self._create_file("subdir/empty2.txt", "")
        self._create_file("non_empty.txt", "some content")

        duplicates = find_duplicates(self.test_dir)
        self.assertEqual(len(duplicates), 1)

        empty_hash = hashlib.sha256(b"").hexdigest()
        self.assertIn(empty_hash, duplicates)
        self.assertCountEqual(duplicates[empty_hash], [filepath1, filepath2])

    def test_find_duplicates_non_existent_directory(self):
        duplicates = find_duplicates("/non/existent/directory")
        self.assertEqual(len(duplicates), 0) # Should return empty dict and print error

    def test_find_duplicates_with_io_error_on_file(self):
        filepath1 = self._create_file("file1.txt", "content A")
        filepath2 = self._create_file("file2.txt", "content B") # This one will error
        filepath3 = self._create_file("file3.txt", "content A") # This one is a duplicate of file1

        # Mock rationale: Simulate an IOError when trying to read a specific file
        # to ensure the utility handles it gracefully and continues processing others.
        original_open = open
        def mock_open_for_error(file, mode='r', *args, **kwargs):
            if file == filepath2:
                raise IOError("Permission denied")
            return original_open(file, mode, *args, **kwargs)

        with patch('builtins.open', side_effect=mock_open_for_error):
            duplicates = find_duplicates(self.test_dir)
            self.assertEqual(len(duplicates), 1) # Only file1 and file3 should be found as duplicates

            hash_a = hashlib.sha256(b"content A").hexdigest()
            self.assertIn(hash_a, duplicates)
            self.assertCountEqual(duplicates[hash_a], [filepath1, filepath3])
