import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, mock_open
from src.defragmenter import calculate_file_hash, find_duplicate_files

class TestDefragmenter(unittest.TestCase):

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
        expected_hash = "5d41402abc4b2a76b9719d911017c592" # md5("hello world")
        self.assertEqual(calculate_file_hash(filepath), expected_hash)

    def test_calculate_file_hash_empty_file(self):
        filepath = self._create_file("empty.txt", "")
        expected_hash = "d41d8cd98f00b204e9800998ecf8427e" # md5("")
        self.assertEqual(calculate_file_hash(filepath), expected_hash)

    def test_calculate_file_hash_non_existent_file(self):
        # Mock rationale: We want to test the error handling for non-existent files
        # without actually creating a file or relying on OS-specific error messages.
        # The `calculate_file_hash` function prints a warning and returns None.
        with patch('builtins.open', side_effect=IOError("File not found")) as mock_open_func:
            with patch('builtins.print') as mock_print: # To suppress print output during test
                result = calculate_file_hash("/non/existent/path.txt")
                self.assertIsNone(result)
                mock_open_func.assert_called_once_with("/non/existent/path.txt", 'rb')
                mock_print.assert_called_once() # Ensure warning was printed

    def test_find_duplicate_files_no_duplicates(self):
        self._create_file("file1.txt", "content A")
        self._create_file("file2.txt", "content B")
        self._create_file("subdir/file3.txt", "content C")
        
        duplicates = find_duplicate_files(self.test_dir)
        self.assertEqual(len(duplicates), 0)

    def test_find_duplicate_files_with_duplicates(self):
        file_a_path = self._create_file("file_a.txt", "duplicate content")
        file_b_path = self._create_file("subdir/file_b.txt", "duplicate content")
        file_c_path = self._create_file("unique.txt", "unique content")
        file_d_path = self._create_file("another_subdir/file_d.txt", "duplicate content")

        duplicates = find_duplicate_files(self.test_dir)
        
        # md5("duplicate content")
        expected_hash = "646393962657e3f84305898864700778" 
        
        self.assertEqual(len(duplicates), 1)
        self.assertIn(expected_hash, duplicates)
        
        duplicate_paths = sorted(duplicates[expected_hash])
        expected_paths = sorted([file_a_path, file_b_path, file_d_path])
        self.assertEqual(duplicate_paths, expected_paths)

    def test_find_duplicate_files_multiple_duplicate_groups(self):
        file1_a = self._create_file("group1_a.txt", "content group 1")
        file1_b = self._create_file("group1_b.txt", "content group 1")
        file2_a = self._create_file("group2_a.txt", "content group 2")
        file2_b = self._create_file("subdir/group2_b.txt", "content group 2")
        file_unique = self._create_file("unique.txt", "unique content")

        duplicates = find_duplicate_files(self.test_dir)

        # Calculate actual hashes dynamically for robustness
        hash1_actual = calculate_file_hash(file1_a)
        hash2_actual = calculate_file_hash(file2_a)

        self.assertEqual(len(duplicates), 2)
        self.assertIn(hash1_actual, duplicates)
        self.assertIn(hash2_actual, duplicates)

        self.assertEqual(sorted(duplicates[hash1_actual]), sorted([file1_a, file1_b]))
        self.assertEqual(sorted(duplicates[hash2_actual]), sorted([file2_a, file2_b]))
        self.assertNotIn(calculate_file_hash(file_unique), duplicates)

    def test_find_duplicate_files_non_existent_directory(self):
        # Mock rationale: Test the error handling for an invalid directory path.
        # The function should raise a ValueError.
        with self.assertRaisesRegex(ValueError, "Directory not found"):
            find_duplicate_files("/non/existent/directory")

    def test_find_duplicate_files_with_verbose_output(self):
        self._create_file("file1.txt", "content A")
        self._create_file("file2.txt", "content A")
        
        # Mock rationale: Capture stdout to verify verbose messages are printed.
        with patch('builtins.print') as mock_print:
            find_duplicate_files(self.test_dir, verbose=True)
            mock_print.assert_any_call(f"Scanning '{self.test_dir}' for data dust...")
            mock_print.assert_any_call(unittest.mock.ANY) # Check for "Processed X files" (exact count might vary based on OS walk order)
            mock_print.assert_any_call(f"  Processed 2 files. Hashed 2 files.")


if __name__ == '__main__':
    unittest.main()
