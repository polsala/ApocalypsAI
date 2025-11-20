import unittest
import os
import tempfile
import shutil
from unittest.mock import patch
from io import StringIO
import logging
import argparse

# Import the function to test
from src.sweeper import clean_empty_dirs, main

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_root = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_root) # Change CWD to simplify path handling in tests

        # Suppress logging during tests to keep output clean
        self.logger = logging.getLogger()
        self.original_level = self.logger.level
        self.logger.setLevel(logging.CRITICAL)

    def tearDown(self):
        # Clean up the temporary directory
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_root)
        # Restore logging level
        self.logger.setLevel(self.original_level)

    def _create_dirs(self, *paths):
        for path in paths:
            os.makedirs(os.path.join(self.test_root, path), exist_ok=True)

    def _create_files(self, *paths):
        for path in paths:
            dir_name = os.path.dirname(path)
            if dir_name:
                os.makedirs(os.path.join(self.test_root, dir_name), exist_ok=True)
            with open(os.path.join(self.test_root, path), 'w') as f:
                f.write("test content")

    def test_removes_single_empty_directory(self):
        self._create_dirs("empty_dir")
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "empty_dir")))
        removed = clean_empty_dirs(self.test_root)
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "empty_dir")))
        self.assertIn(os.path.join(self.test_root, "empty_dir"), removed)
        self.assertEqual(len(removed), 1)

    def test_removes_nested_empty_directories(self):
        self._create_dirs("parent/child/grandchild")
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "parent/child/grandchild")))
        removed = clean_empty_dirs(self.test_root)
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "parent/child/grandchild")))
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "parent/child")))
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "parent")))
        self.assertEqual(len(removed), 3)
        self.assertIn(os.path.join(self.test_root, "parent/child/grandchild"), removed)
        self.assertIn(os.path.join(self.test_root, "parent/child"), removed)
        self.assertIn(os.path.join(self.test_root, "parent"), removed)

    def test_does_not_remove_directories_with_files(self):
        self._create_dirs("dir_with_file")
        self._create_files("dir_with_file/file.txt")
        self._create_dirs("empty_sibling")
        removed = clean_empty_dirs(self.test_root)
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "dir_with_file/file.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "dir_with_file")))
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "empty_sibling")))
        self.assertEqual(len(removed), 1)
        self.assertIn(os.path.join(self.test_root, "empty_sibling"), removed)

    def test_does_not_remove_root_directory_if_it_becomes_empty(self):
        # Create a structure where everything under root_dir is removed,
        # making root_dir itself empty, but root_dir should not be removed.
        self._create_dirs("root_child/empty_sub")
        removed = clean_empty_dirs(self.test_root)
        self.assertTrue(os.path.exists(self.test_root)) # Root should still exist
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "root_child/empty_sub")))
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "root_child")))
        self.assertEqual(len(removed), 2) # Only root_child/empty_sub and root_child should be removed

    def test_dry_run_mode(self):
        self._create_dirs("empty_dir_dry_run/sub_empty")
        removed = clean_empty_dirs(self.test_root, dry_run=True)
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "empty_dir_dry_run/sub_empty")))
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "empty_dir_dry_run")))
        self.assertEqual(len(removed), 2) # Should report what *would* be removed
        self.assertIn(os.path.join(self.test_root, "empty_dir_dry_run/sub_empty"), removed)
        self.assertIn(os.path.join(self.test_root, "empty_dir_dry_run"), removed)

    def test_non_existent_root_directory(self):
        non_existent_path = os.path.join(self.test_root, "non_existent")
        removed = clean_empty_dirs(non_existent_path)
        self.assertEqual(len(removed), 0)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_dry_run(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: We need to control command-line arguments and capture stdout/stderr
        # without actually running the script from the command line. This ensures deterministic
        # testing of the main function's logic and output without side effects.
        mock_parse_args.return_value = argparse.Namespace(path=self.test_root, dry_run=True)
        self._create_dirs("main_test_empty/sub_empty")

        main()

        output = mock_stdout.getvalue()
        self.assertIn("Running in DRY RUN mode", output)
        self.assertIn("Would have removed 2 empty directories", output)
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "main_test_empty/sub_empty"))) # Should still exist

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_actual_run(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Similar to the dry-run test, this allows us to simulate command-line
        # execution and verify actual deletion behavior and output without affecting the real filesystem.
        mock_parse_args.return_value = argparse.Namespace(path=self.test_root, dry_run=False)
        self._create_dirs("main_test_actual/sub_actual")

        main()

        output = mock_stdout.getvalue()
        self.assertIn("Removed empty directory", output)
        self.assertIn("Removed 2 empty directories", output)
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "main_test_actual/sub_actual"))) # Should be removed

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_no_empty_dirs(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Ensures the main function correctly reports when no empty directories are found,
        # without needing actual filesystem changes or command-line input.
        mock_parse_args.return_value = argparse.Namespace(path=self.test_root, dry_run=False)
        self._create_files("some_file.txt") # Ensure root is not empty

        main()

        output = mock_stdout.getvalue()
        self.assertIn("No empty directories found to remove", output)
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "some_file.txt")))

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_non_existent_path(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Verifies the main function's error handling and output when an invalid path is provided,
        # without requiring a non-existent path on the actual system.
        non_existent_path = os.path.join(self.test_root, "definitely_not_here")
        mock_parse_args.return_value = argparse.Namespace(path=non_existent_path, dry_run=False)

        main()

        error_output = mock_stderr.getvalue()
        self.assertIn(f"Error: Root directory '{non_existent_path}' does not exist or is not a directory.", error_output)
        stdout_output = mock_stdout.getvalue()
        self.assertIn("No empty directories found to remove", stdout_output)


if __name__ == '__main__':
    unittest.main()
