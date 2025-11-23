import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from src.sweeper import find_broken_symlinks, find_empty_directories, remove_paths, main

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing filesystem operations
        self.test_dir = tempfile.mkdtemp()
        self.original_getcwd = os.getcwd()
        os.chdir(self.test_dir) # Change to temp dir for relative path tests

    def tearDown(self):
        # Clean up the temporary directory
        os.chdir(self.original_getcwd)
        shutil.rmtree(self.test_dir)

    def _create_test_structure(self):
        """Helper to create a complex test directory structure."""
        # Create files
        with open(os.path.join(self.test_dir, "file1.txt"), "w") as f:
            f.write("content")
        with open(os.path.join(self.test_dir, "file2.log"), "w") as f:
            f.write("content")

        # Create directories
        os.makedirs(os.path.join(self.test_dir, "empty_dir_a"))
        os.makedirs(os.path.join(self.test_dir, "empty_dir_b", "sub_empty"))
        os.makedirs(os.path.join(self.test_dir, "full_dir"))
        os.makedirs(os.path.join(self.test_dir, "dir_with_file"))
        with open(os.path.join(self.test_dir, "dir_with_file", "inner_file.txt"), "w") as f:
            f.write("content")

        # Create valid symlinks
        os.symlink(os.path.join(self.test_dir, "file1.txt"), os.path.join(self.test_dir, "link_to_file1.txt"))
        os.symlink(os.path.join(self.test_dir, "full_dir"), os.path.join(self.test_dir, "link_to_full_dir"))

        # Create broken symlinks
        self.broken_link_abs = os.path.join(self.test_dir, "broken_link_abs")
        os.symlink(os.path.join(self.test_dir, "non_existent_target.txt"), self.broken_link_abs)

        self.broken_link_rel = os.path.join(self.test_dir, "broken_link_rel")
        os.symlink("non_existent_relative_target.txt", self.broken_link_rel)

        # Broken symlink in a subdirectory
        os.makedirs(os.path.join(self.test_dir, "sub_dir"))
        self.broken_link_sub = os.path.join(self.test_dir, "sub_dir", "broken_link_sub")
        os.symlink("../non_existent_sub_target.txt", self.broken_link_sub)

        # Create a file in an empty dir to make it not empty
        with open(os.path.join(self.test_dir, "empty_dir_b", "sub_empty", "temp.txt"), "w") as f:
            f.write("temp")
        # Then remove it to ensure it's empty again for testing
        os.remove(os.path.join(self.test_dir, "empty_dir_b", "sub_empty", "temp.txt"))


    def test_find_broken_symlinks(self):
        self._create_test_structure()
        broken_links = find_broken_symlinks(self.test_dir)
        expected_links = sorted([
            self.broken_link_abs,
            self.broken_link_rel,
            self.broken_link_sub,
        ])
        self.assertEqual(sorted(broken_links), expected_links)

        # Test with verbose output
        with patch('builtins.print') as mock_print:
            find_broken_symlinks(self.test_dir, verbose=True)
            self.assertTrue(any("Found broken symlink" in call.args[0] for call in mock_print.call_args_list))

    def test_find_empty_directories(self):
        self._create_test_structure()
        empty_dirs = find_empty_directories(self.test_dir)
        expected_dirs = sorted([
            os.path.join(self.test_dir, "empty_dir_b", "sub_empty"),
            os.path.join(self.test_dir, "empty_dir_a"),
        ])
        self.assertEqual(sorted(empty_dirs), expected_dirs)

        # Test with verbose output
        with patch('builtins.print') as mock_print:
            find_empty_directories(self.test_dir, verbose=True)
            self.assertTrue(any("Found empty directory" in call.args[0] for call in mock_print.call_args_list))

    def test_remove_paths_symlinks(self):
        self._create_test_structure()
        broken_links = find_broken_symlinks(self.test_dir)
        initial_count = len(broken_links)
        self.assertTrue(initial_count > 0)

        removed_count = remove_paths(broken_links, "broken symlink")
        self.assertEqual(removed_count, initial_count)

        # Verify links are gone
        for link in broken_links:
            self.assertFalse(os.path.exists(link))
            self.assertFalse(os.path.islink(link))

        # Test with verbose output
        with patch('builtins.print') as mock_print:
            # Recreate links for verbose test
            os.symlink(os.path.join(self.test_dir, "non_existent_target.txt"), self.broken_link_abs)
            remove_paths([self.broken_link_abs], "broken symlink", verbose=True)
            self.assertTrue(any("Removed broken symlink" in call.args[0] for call in mock_print.call_args_list))

    def test_remove_paths_empty_dirs(self):
        self._create_test_structure()
        empty_dirs = find_empty_directories(self.test_dir)
        initial_count = len(empty_dirs)
        self.assertTrue(initial_count > 0)

        removed_count = remove_paths(empty_dirs, "empty directory")
        self.assertEqual(removed_count, initial_count)

        # Verify directories are gone
        for d in empty_dirs:
            self.assertFalse(os.path.exists(d))
            self.assertFalse(os.path.isdir(d))

        # Test with verbose output
        with patch('builtins.print') as mock_print:
            # Recreate an empty dir for verbose test
            os.makedirs(os.path.join(self.test_dir, "temp_empty_dir"))
            remove_paths([os.path.join(self.test_dir, "temp_empty_dir")], "empty directory", verbose=True)
            self.assertTrue(any("Removed empty directory" in call.args[0] for call in mock_print.call_args_list))

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_args(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments without actually running the script via subprocess.
        # This allows testing the main function's argument parsing and logic directly.
        mock_parse_args.return_value = MagicMock(
            path=self.test_dir,
            remove_symlinks=False,
            remove_empty_dirs=False,
            verbose=False
        )
        self._create_test_structure()

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("Found 3 broken symbolic link(s)", mock_stdout.getvalue())
        self.assertIn("Found 2 empty directory(ies)", mock_stdout.getvalue())
        self.assertIn("No items were removed", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_remove_all(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments for removing all debris.
        # This allows testing the removal logic and output.
        mock_parse_args.return_value = MagicMock(
            path=self.test_dir,
            remove_symlinks=True,
            remove_empty_dirs=True,
            verbose=False
        )
        self._create_test_structure()

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("Successfully removed 3 broken symbolic link(s).", mock_stdout.getvalue())
        self.assertIn("Successfully removed 2 empty directory(ies).", mock_stdout.getvalue())
        self.assertIn("Total items removed: 5.", mock_stdout.getvalue())

        # Verify actual removal
        self.assertEqual(len(find_broken_symlinks(self.test_dir)), 0)
        self.assertEqual(len(find_empty_directories(self.test_dir)), 0)

    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_path(self, mock_parse_args, mock_stderr):
        # Mock rationale: Simulate an invalid path argument to test error handling.
        mock_parse_args.return_value = MagicMock(
            path="/non/existent/path",
            remove_symlinks=False,
            remove_empty_dirs=False,
            verbose=False
        )
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: The specified path '/non/existent/path' is not a valid directory.", mock_stderr.getvalue())

    @patch('os.remove')
    @patch('os.rmdir')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_remove_paths_error_handling(self, mock_stderr, mock_rmdir, mock_remove):
        # Mock rationale: Simulate OSError during removal to ensure error messages are printed.
        mock_remove.side_effect = OSError("Permission denied")
        mock_rmdir.side_effect = OSError("Directory not empty")

        # Test file removal error
        paths_to_remove = [os.path.join(self.test_dir, "dummy_file.txt")]
        with open(paths_to_remove[0], "w") as f:
            f.write("content")
        removed_count = remove_paths(paths_to_remove, "file")
        self.assertEqual(removed_count, 0)
        self.assertIn("Error removing file", mock_stderr.getvalue())
        mock_stderr.reset_mock()

        # Test directory removal error
        paths_to_remove = [os.path.join(self.test_dir, "dummy_dir")]
        os.makedirs(paths_to_remove[0])
        removed_count = remove_paths(paths_to_remove, "directory")
        self.assertEqual(removed_count, 0)
        self.assertIn("Error removing directory", mock_stderr.getvalue())
