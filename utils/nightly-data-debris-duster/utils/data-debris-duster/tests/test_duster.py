import unittest
import os
import tempfile
import shutil
from unittest.mock import patch
import sys
from io import StringIO

# Import the duster functions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from duster import find_empty_dirs, clean_empty_dirs, main

class TestDataDebrisDuster(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_root = tempfile.mkdtemp()
        self.create_test_dirs()

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_root)

    def create_test_dirs(self):
        """
        Creates a specific directory structure for testing.
        - root/
            - empty_dir_1/
            - empty_dir_2/
                - nested_empty_dir/
            - non_empty_dir_1/
                - file.txt
            - non_empty_dir_2/
                - sub_non_empty/
                    - another_file.txt
            - mixed_dir/
                - empty_child/
                - file_in_mixed.txt
        """
        os.makedirs(os.path.join(self.test_root, "empty_dir_1"))
        os.makedirs(os.path.join(self.test_root, "empty_dir_2", "nested_empty_dir"))
        
        non_empty_path_1 = os.path.join(self.test_root, "non_empty_dir_1")
        os.makedirs(non_empty_path_1)
        with open(os.path.join(non_empty_path_1, "file.txt"), "w") as f:
            f.write("content")

        non_empty_path_2 = os.path.join(self.test_root, "non_empty_dir_2", "sub_non_empty")
        os.makedirs(non_empty_path_2)
        with open(os.path.join(non_empty_path_2, "another_file.txt"), "w") as f:
            f.write("more content")

        mixed_dir_path = os.path.join(self.test_root, "mixed_dir")
        os.makedirs(mixed_dir_path)
        os.makedirs(os.path.join(mixed_dir_path, "empty_child"))
        with open(os.path.join(mixed_dir_path, "file_in_mixed.txt"), "w") as f:
            f.write("mixed content")

    def test_find_empty_dirs(self):
        # Test the find_empty_dirs utility function
        expected_empty = sorted([
            os.path.join(self.test_root, "empty_dir_1"),
            os.path.join(self.test_root, "empty_dir_2", "nested_empty_dir"),
            os.path.join(self.test_root, "mixed_dir", "empty_child"),
        ])
        found = sorted(find_empty_dirs(self.test_root))
        self.assertEqual(found, expected_empty)

    def test_clean_empty_dirs_dry_run(self):
        # Test clean_empty_dirs in dry-run mode (default)
        found, removed = clean_empty_dirs(self.test_root, dry_run=True)
        
        expected_found = sorted([
            os.path.join(self.test_root, "empty_dir_1"),
            os.path.join(self.test_root, "empty_dir_2", "nested_empty_dir"),
            os.path.join(self.test_root, "empty_dir_2"), # This becomes empty after nested_empty_dir is conceptually removed
            os.path.join(self.test_root, "mixed_dir", "empty_child"),
        ])
        
        # The order of `found` from clean_empty_dirs (topdown=False) might be different
        # but the set of paths should match.
        self.assertSetEqual(set(found), set(expected_found))
        self.assertEqual(removed, []) # Nothing should be removed in dry run

        # Verify directories still exist
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "empty_dir_1")))
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "empty_dir_2", "nested_empty_dir")))
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "mixed_dir", "empty_child")))

    def test_clean_empty_dirs_actual_clean(self):
        # Test clean_empty_dirs with actual removal
        found, removed = clean_empty_dirs(self.test_root, dry_run=False)

        expected_removed = sorted([
            os.path.join(self.test_root, "empty_dir_1"),
            os.path.join(self.test_root, "empty_dir_2", "nested_empty_dir"),
            os.path.join(self.test_root, "empty_dir_2"),
            os.path.join(self.test_root, "mixed_dir", "empty_child"),
        ])
        
        self.assertSetEqual(set(removed), set(expected_removed))
        self.assertSetEqual(set(found), set(expected_removed)) # In actual clean, found == removed

        # Verify directories are removed
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "empty_dir_1")))
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "empty_dir_2", "nested_empty_dir")))
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "empty_dir_2")))
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "mixed_dir", "empty_child")))
        
        # Verify non-empty directories still exist
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "non_empty_dir_1", "file.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "non_empty_dir_2", "sub_non_empty", "another_file.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.test_root, "mixed_dir", "file_in_mixed.txt")))

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_dry_run_output(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: We need to capture stdout/stderr and control command-line arguments
        # without actually running the script from the command line.
        mock_parse_args.return_value = argparse.Namespace(path=self.test_root, clean=False)
        
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Scanning", output)
        self.assertIn("Detected Digital Debris", output)
        self.assertIn(os.path.join(self.test_root, "empty_dir_1"), output)
        self.assertIn(os.path.join(self.test_root, "empty_dir_2"), output) # Parent also listed
        self.assertIn(os.path.join(self.test_root, "empty_dir_2", "nested_empty_dir"), output)
        self.assertIn(os.path.join(self.test_root, "mixed_dir", "empty_child"), output)
        self.assertIn("Total debris piles found: 4", output)
        self.assertIn("Run with '--clean' to remove these digital debris piles.", output)
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_clean_output(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Capture stdout/stderr and control arguments for clean mode.
        mock_parse_args.return_value = argparse.Namespace(path=self.test_root, clean=True)
        
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Scanning", output)
        self.assertIn("Detected Digital Debris", output)
        self.assertIn("Debris Successfully Dusted", output)
        self.assertIn("Total debris piles removed: 4", output)
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "empty_dir_1")))
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "empty_dir_2", "nested_empty_dir")))
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "empty_dir_2")))
        self.assertFalse(os.path.exists(os.path.join(self.test_root, "mixed_dir", "empty_child")))
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Test error handling for invalid paths and prevent actual script exit.
        invalid_path = os.path.join(self.test_root, "non_existent_path")
        mock_parse_args.return_value = argparse.Namespace(path=invalid_path, clean=False)
        
        main()
        self.assertIn(f"Error: Path '{os.path.abspath(invalid_path)}' does not exist or is not a directory.", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_empty_dirs(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Test the output when no empty directories are found.
        # Create a test root with no empty directories
        shutil.rmtree(self.test_root) # Clear existing structure
        self.test_root = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_root, "only_non_empty"))
        with open(os.path.join(self.test_root, "only_non_empty", "file.txt"), "w") as f:
            f.write("content")

        mock_parse_args.return_value = argparse.Namespace(path=self.test_root, clean=False)
        
        main()
        output = mock_stdout.getvalue()
        self.assertIn("No digital debris found. Your filesystem is pristine!", output)
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('os.rmdir')
    @patch('sys.stderr', new_callable=StringIO)
    def test_clean_empty_dirs_permission_error(self, mock_stderr, mock_rmdir):
        # Mock rationale: Simulate an OSError during rmdir to test error handling.
        mock_rmdir.side_effect = OSError("Permission denied")

        # Create a simple empty directory for this specific test
        empty_dir = os.path.join(self.test_root, "permission_denied_empty")
        os.makedirs(empty_dir)

        found, removed = clean_empty_dirs(self.test_root, dry_run=False)

        self.assertIn(empty_dir, found)
        self.assertNotIn(empty_dir, removed) # Should not be in removed due to error
        mock_rmdir.assert_called_once_with(empty_dir)
        self.assertIn(f"Error removing {empty_dir}: Permission denied", mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
