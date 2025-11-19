import unittest
import os
import tempfile
import shutil
import hashlib
from unittest.mock import patch
from io import StringIO

from src.resonator import _calculate_file_hash, _find_files, find_duplicate_files, main

class TestResonator(unittest.TestCase):

    temp_dir = None

    @classmethod
    def setUpClass(cls):
        # Mock rationale: Use tempfile to create a temporary directory for all tests.
        # This ensures tests are isolated from the actual file system and are deterministic.
        cls.temp_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        # Mock rationale: Clean up the temporary directory after all tests are done.
        # This prevents test artifacts from polluting the system.
        if cls.temp_dir and os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)

    def setUp(self):
        # Create a unique subdirectory for each test to ensure isolation between tests.
        self.test_case_dir = tempfile.mkdtemp(dir=self.temp_dir)

    def tearDown(self):
        # Clean up the test-specific subdirectory.
        if os.path.exists(self.test_case_dir):
            shutil.rmtree(self.test_case_dir)

    def _create_file(self, filename, content):
        filepath = os.path.join(self.test_case_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath

    def _get_hash(self, content):
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def test_calculate_file_hash(self):
        content = "This is some test content."
        filepath = self._create_file("test_file.txt", content)
        expected_hash = self._get_hash(content)
        self.assertEqual(_calculate_file_hash(filepath), expected_hash)

        # Test with empty file
        empty_filepath = self._create_file("empty_file.txt", "")
        expected_empty_hash = self._get_hash("")
        self.assertEqual(_calculate_file_hash(empty_filepath), expected_empty_hash)

        # Test non-existent file
        self.assertIsNone(_calculate_file_hash(os.path.join(self.test_case_dir, "non_existent.txt")))

    def test_find_files_empty_dir(self):
        # Mock rationale: The test_case_dir is an empty directory.
        # This tests the base case of no files being found.
        files = list(_find_files(self.test_case_dir))
        self.assertEqual(len(files), 0)

    def test_find_files_single_file(self):
        filepath = self._create_file("single.txt", "content")
        files = list(_find_files(self.test_case_dir))
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0], filepath)

    def test_find_files_nested_files(self):
        file1 = self._create_file("dir1/file1.txt", "content1")
        file2 = self._create_file("dir1/dir2/file2.txt", "content2")
        files = sorted(list(_find_files(self.test_case_dir)))
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0], file1)
        self.assertEqual(files[1], file2)

    def test_find_duplicate_files_no_duplicates(self):
        self._create_file("file1.txt", "content1")
        self._create_file("file2.txt", "content2")
        duplicates = find_duplicate_files([self.test_case_dir])
        self.assertEqual(len(duplicates), 0)

    def test_find_duplicate_files_with_duplicates(self):
        content_a = "duplicate content A"
        content_b = "unique content B"

        file_a1 = self._create_file("a1.txt", content_a)
        file_a2 = self._create_file("subdir/a2.txt", content_a)
        file_b1 = self._create_file("b1.txt", content_b)

        duplicates = find_duplicate_files([self.test_case_dir])
        self.assertEqual(len(duplicates), 1)
        self.assertIn(sorted([file_a1, file_a2]), [sorted(d) for d in duplicates])

    def test_find_duplicate_files_multiple_duplicate_groups(self):
        content_a = "duplicate content A"
        content_b = "duplicate content B"

        file_a1 = self._create_file("a1.txt", content_a)
        file_a2 = self._create_file("subdir/a2.txt", content_a)
        file_b1 = self._create_file("b1.txt", content_b)
        file_b2 = self._create_file("b2.txt", content_b)

        duplicates = find_duplicate_files([self.test_case_dir])
        self.assertEqual(len(duplicates), 2)
        expected_groups = [sorted([file_a1, file_a2]), sorted([file_b1, file_b2])]
        actual_groups = [sorted(d) for d in duplicates]
        self.assertIn(expected_groups[0], actual_groups)
        self.assertIn(expected_groups[1], actual_groups)

    def test_find_duplicate_files_mixed_paths(self):
        content_a = "mixed path content"
        file_a1 = self._create_file("file_in_dir.txt", content_a)
        
        # Create a second temp dir for a file that's passed directly
        second_temp_dir = tempfile.mkdtemp(dir=self.temp_dir)
        file_a2_path = os.path.join(second_temp_dir, "direct_file.txt")
        with open(file_a2_path, 'w') as f:
            f.write(content_a)

        duplicates = find_duplicate_files([self.test_case_dir, file_a2_path])
        self.assertEqual(len(duplicates), 1)
        self.assertIn(sorted([file_a1, file_a2_path]), [sorted(d) for d in duplicates])

        shutil.rmtree(second_temp_dir) # Clean up the extra temp dir

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_duplicates_output(self, mock_parse_args, mock_stdout):
        # Mock rationale: Mock argparse to control CLI arguments without actual command line input.
        # Mock sys.stdout to capture printed output for assertion, ensuring deterministic output checks.
        mock_parse_args.return_value = argparse.Namespace(path=[self.test_case_dir])
        self._create_file("unique1.txt", "content1")
        self._create_file("unique2.txt", "content2")

        main()
        output = mock_stdout.getvalue()
        self.assertIn("No duplicate files found.", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_duplicates_output(self, mock_parse_args, mock_stdout):
        # Mock rationale: Same as above, for testing output when duplicates are found.
        mock_parse_args.return_value = argparse.Namespace(path=[self.test_case_dir])
        content = "duplicate content for main test"
        file1 = self._create_file("main_file1.txt", content)
        file2 = self._create_file("main_file2.txt", content)

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Found 1 groups of duplicate files:", output)
        self.assertIn(file1, output)
        self.assertIn(file2, output)
        self.assertIn(self._get_hash(content), output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_path_warning(self, mock_parse_args, mock_stdout):
        # Mock rationale: Test how the utility handles invalid paths provided via CLI.
        mock_parse_args.return_value = argparse.Namespace(path=[self.test_case_dir, "/non/existent/path"])
        self._create_file("unique.txt", "content")

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Warning: Path '/non/existent/path' is not a valid file or directory. Skipping.", output)
        self.assertIn("No duplicate files found.", output) # Assuming only unique file in valid path

if __name__ == '__main__':
    unittest.main()
