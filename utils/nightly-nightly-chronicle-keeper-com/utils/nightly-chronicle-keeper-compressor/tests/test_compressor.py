import unittest
import os
import tempfile
import shutil
import sys
from io import StringIO
from unittest.mock import patch

# Add the src directory to the Python path for importing compressor.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import compressor

class TestCompressor(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

        # Create test files
        self.file_a_content = b"This is the content of file A."
        self.file_b_content = b"This is the content of file B."
        self.large_file_content = b"X" * (2 * 1024 * 1024) # 2 MB

        self.file_a_path = os.path.join(self.test_dir, "file_a.txt")
        self.file_a_copy_path = os.path.join(self.test_dir, "file_a_copy.txt")
        self.file_b_path = os.path.join(self.test_dir, "file_b.txt")
        self.large_file_path = os.path.join(self.test_dir, "large_file.bin")
        self.empty_file_path = os.path.join(self.test_dir, "empty_file.txt")

        # Create a subdirectory
        self.subdir_path = os.path.join(self.test_dir, "subdir")
        os.makedirs(self.subdir_path)
        self.file_c_path = os.path.join(self.subdir_path, "file_c.txt")

        with open(self.file_a_path, "wb") as f: f.write(self.file_a_content)
        with open(self.file_a_copy_path, "wb") as f: f.write(self.file_a_content)
        with open(self.file_b_path, "wb") as f: f.write(self.file_b_content)
        with open(self.large_file_path, "wb") as f: f.write(self.large_file_content)
        with open(self.empty_file_path, "wb") as f: pass # Empty file
        with open(self.file_c_path, "wb") as f: f.write(b"Content for file C.")

        self.expected_total_files = 6
        self.expected_total_size = (
            len(self.file_a_content) * 2 +
            len(self.file_b_content) +
            len(self.large_file_content) +
            0 + # empty file
            len(b"Content for file C.")
        )

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def test_get_file_hash(self):
        # Test that two identical files have the same hash
        hash_a = compressor.get_file_hash(self.file_a_path)
        hash_a_copy = compressor.get_file_hash(self.file_a_copy_path)
        hash_b = compressor.get_file_hash(self.file_b_path)

        self.assertIsNotNone(hash_a)
        self.assertEqual(hash_a, hash_a_copy)
        self.assertNotEqual(hash_a, hash_b)

        # Test hash of an empty file
        hash_empty = compressor.get_file_hash(self.empty_file_path)
        self.assertEqual(hash_empty, hashlib.md5(b'').hexdigest())

        # Test non-existent file
        self.assertIsNone(compressor.get_file_hash(os.path.join(self.test_dir, "non_existent.txt")))

    def test_scan_directory(self):
        min_size_for_large = 1 * 1024 * 1024 # 1 MB
        duplicates, large_files, empty_files, total_files, total_size = compressor.scan_directory(self.test_dir, min_size_for_large)

        self.assertEqual(total_files, self.expected_total_files)
        self.assertEqual(total_size, self.expected_total_size)

        # Test duplicate detection
        self.assertEqual(len(duplicates), 1)
        duplicate_hash = compressor.get_file_hash(self.file_a_path)
        self.assertIn(duplicate_hash, duplicates)
        self.assertIn(self.file_a_path, duplicates[duplicate_hash])
        self.assertIn(self.file_a_copy_path, duplicates[duplicate_hash])
        self.assertEqual(len(duplicates[duplicate_hash]), 2)

        # Test large file detection
        self.assertEqual(len(large_files), 1)
        self.assertEqual(large_files[0][0], self.large_file_path)
        self.assertEqual(large_files[0][1], len(self.large_file_content))

        # Test empty file detection
        self.assertEqual(len(empty_files), 1)
        self.assertIn(self.empty_file_path, empty_files)

    def test_scan_directory_no_large_files(self):
        # Set min_size_for_large very high, so no files are considered large
        min_size_for_large = 10 * 1024 * 1024 # 10 MB
        duplicates, large_files, empty_files, total_files, total_size = compressor.scan_directory(self.test_dir, min_size_for_large)

        self.assertEqual(len(large_files), 0)
        self.assertEqual(total_files, self.expected_total_files)
        self.assertEqual(total_size, self.expected_total_size)

    def test_scan_directory_all_large_files(self):
        # Set min_size_for_large very low, so all non-empty files are considered large
        min_size_for_large = 1 # 1 byte
        duplicates, large_files, empty_files, total_files, total_size = compressor.scan_directory(self.test_dir, min_size_for_large)

        # 5 files are non-empty
        self.assertEqual(len(large_files), 5)
        self.assertEqual(total_files, self.expected_total_files)
        self.assertEqual(total_size, self.expected_total_size)

    def test_generate_report(self):
        min_size_for_large = 1 * 1024 * 1024 # 1 MB
        duplicates, large_files, empty_files, total_files, total_size = compressor.scan_directory(self.test_dir, min_size_for_large)

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        compressor.generate_report(duplicates, large_files, empty_files, total_files, total_size)

        sys.stdout = sys.__stdout__ # Reset stdout
        output = captured_output.getvalue()

        self.assertIn("--- Chronicle Keeper's Content Compressor Report ---", output)
        self.assertIn(f"Scanned {total_files} files, totaling {compressor.format_size(total_size)}.", output)
        self.assertIn("### Duplicate Files Found ###", output)
        self.assertIn(self.file_a_path, output)
        self.assertIn(self.file_a_copy_path, output)
        self.assertIn("### Large Files Found ###", output)
        self.assertIn(self.large_file_path, output)
        self.assertIn("### Empty Files Found ###", output)
        self.assertIn(self.empty_file_path, output)
        self.assertIn("--- End of Report ---", output)

    def test_main_function(self):
        # Mock argparse to pass arguments programmatically
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
            mock_parse_args.return_value = argparse.Namespace(
                path=self.test_dir,
                min_size=1 * 1024 * 1024, # 1 MB
                report_only=True
            )
            # Capture stdout
            captured_output = StringIO()
            sys.stdout = captured_output

            compressor.main()

            sys.stdout = sys.__stdout__ # Reset stdout
            output = captured_output.getvalue()

            self.assertIn(f"Scanning directory: {self.test_dir}...", output)
            self.assertIn("### Duplicate Files Found ###", output)
            self.assertIn("### Large Files Found ###", output)
            self.assertIn("### Empty Files Found ###", output)

    def test_main_function_invalid_path(self):
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
            mock_parse_args.return_value = argparse.Namespace(
                path="/non/existent/path",
                min_size=100,
                report_only=True
            )
            # Capture stderr and check for exit code 1
            with self.assertRaises(SystemExit) as cm:
                with patch('sys.stderr', new=StringIO()) as fake_stderr:
                    compressor.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: The provided path '/non/existent/path' is not a valid directory.", fake_stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
