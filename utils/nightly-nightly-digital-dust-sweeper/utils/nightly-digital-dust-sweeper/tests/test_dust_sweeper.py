import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from src.dust_sweeper import find_empty_directories, find_broken_symlinks, clean_up, main

class TestDustSweeper(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_dir = tempfile.mkdtemp()
        self.mock_stdout = MagicMock()
        self.mock_stderr = MagicMock()

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def _create_test_structure(self):
        """Helper to create a consistent test directory structure."""
        # Empty directories
        os.makedirs(os.path.join(self.test_dir, "empty_dir_1"))
        os.makedirs(os.path.join(self.test_dir, "parent_dir", "empty_child_dir"))
        os.makedirs(os.path.join(self.test_dir, "non_empty_dir", "sub_dir"))
        with open(os.path.join(self.test_dir, "non_empty_dir", "file.txt"), "w") as f:
            f.write("content")

        # Files
        with open(os.path.join(self.test_dir, "file_a.txt"), "w") as f:
            f.write("hello")
        with open(os.path.join(self.test_dir, "parent_dir", "file_b.txt"), "w") as f:
            f.write("world")

        # Symbolic links
        # Valid symlink
        os.symlink(
            os.path.join(self.test_dir, "file_a.txt"),
            os.path.join(self.test_dir, "link_to_file_a.txt")
        )
        # Broken symlink (target does not exist)
        os.symlink(
            os.path.join(self.test_dir, "non_existent_target.txt"),
            os.path.join(self.test_dir, "broken_link_1.txt")
        )
        # Broken symlink in a subdirectory
        os.symlink(
            os.path.join(self.test_dir, "non_empty_dir", "another_non_existent.txt"),
            os.path.join(self.test_dir, "non_empty_dir", "broken_link_2.txt")
        )
        # Symlink to a directory
        os.symlink(
            os.path.join(self.test_dir, "non_empty_dir"),
            os.path.join(self.test_dir, "link_to_dir")
        )
        # Broken symlink to a directory
        os.symlink(
            os.path.join(self.test_dir, "non_existent_dir"),
            os.path.join(self.test_dir, "broken_dir_link")
        )

    def test_find_empty_directories(self):
        self._create_test_structure()
        expected_empty_dirs = [
            os.path.join(self.test_dir, "empty_dir_1"),
            os.path.join(self.test_dir, "parent_dir", "empty_child_dir")
        ]
        found_empty_dirs = find_empty_directories(self.test_dir)
        self.assertCountEqual(found_empty_dirs, expected_empty_dirs)

        # Test with a non-existent path
        self.assertEqual(find_empty_directories("/non/existent/path"), [])
        # Mock rationale: os.path.isdir is mocked to simulate a non-existent path without actual file system interaction.
        with patch('os.path.isdir', return_value=False):
            self.assertEqual(find_empty_directories("/mock/path"), [])

    def test_find_broken_symlinks(self):
        self._create_test_structure()
        expected_broken_links = [
            os.path.join(self.test_dir, "broken_link_1.txt"),
            os.path.join(self.test_dir, "non_empty_dir", "broken_link_2.txt"),
            os.path.join(self.test_dir, "broken_dir_link")
        ]
        found_broken_links = find_broken_symlinks(self.test_dir)
        self.assertCountEqual(found_broken_links, expected_broken_links)

        # Test with a non-existent path
        self.assertEqual(find_broken_symlinks("/non/existent/path"), [])
        # Mock rationale: os.path.isdir is mocked to simulate a non-existent path without actual file system interaction.
        with patch('os.path.isdir', return_value=False):
            self.assertEqual(find_broken_symlinks("/mock/path"), [])

    def test_clean_up_empty_directories(self):
        self._create_test_structure()
        empty_dirs_to_remove = [
            os.path.join(self.test_dir, "empty_dir_1"),
            os.path.join(self.test_dir, "parent_dir", "empty_child_dir")
        ]
        # Ensure they exist before cleanup
        for d in empty_dirs_to_remove:
            self.assertTrue(os.path.isdir(d))

        removed_dirs, removed_links = clean_up(empty_dirs_to_remove, [], verbose=True)
        self.assertEqual(removed_dirs, 2)
        self.assertEqual(removed_links, 0)

        # Ensure they are removed
        for d in empty_dirs_to_remove:
            self.assertFalse(os.path.exists(d))

        # Test with an OSError during rmdir
        # Mock rationale: os.rmdir is mocked to simulate a permission error or other OSError during cleanup.
        with patch('os.rmdir', side_effect=OSError("Permission denied")):
            removed_dirs, removed_links = clean_up(empty_dirs_to_remove, [], verbose=True)
            self.assertEqual(removed_dirs, 0) # None removed due to error
            self.assertEqual(removed_links, 0)

    def test_clean_up_broken_symlinks(self):
        self._create_test_structure()
        broken_links_to_remove = [
            os.path.join(self.test_dir, "broken_link_1.txt"),
            os.path.join(self.test_dir, "non_empty_dir", "broken_link_2.txt")
        ]
        # Ensure they exist before cleanup
        for l in broken_links_to_remove:
            self.assertTrue(os.path.islink(l))

        removed_dirs, removed_links = clean_up([], broken_links_to_remove, verbose=True)
        self.assertEqual(removed_dirs, 0)
        self.assertEqual(removed_links, 2)

        # Ensure they are removed
        for l in broken_links_to_remove:
            self.assertFalse(os.path.exists(l)) # os.path.exists returns false for removed links

        # Test with an OSError during remove
        # Mock rationale: os.remove is mocked to simulate a permission error or other OSError during cleanup.
        with patch('os.remove', side_effect=OSError("Permission denied")):
            removed_dirs, removed_links = clean_up([], broken_links_to_remove, verbose=True)
            self.assertEqual(removed_dirs, 0)
            self.assertEqual(removed_links, 0) # None removed due to error

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_dry_run(self, mock_parse_args, mock_stderr, mock_stdout):
        self._create_test_structure()
        mock_parse_args.return_value = MagicMock(
            path=self.test_dir,
            clean=False,
            verbose=False
        )
        main()
        mock_stdout.assert_called() # Ensure some output happened
        self.assertIn("Dry run complete", mock_stdout.mock_calls[-1].args[0])
        self.assertIn("Found 2 empty directories", mock_stdout.mock_calls[5].args[0])
        self.assertIn("Found 3 broken symbolic links", mock_stdout.mock_calls[9].args[0])
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "empty_dir_1"))) # Should still exist
        self.assertTrue(os.path.islink(os.path.join(self.test_dir, "broken_link_1.txt"))) # Should still exist

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_clean_run(self, mock_parse_args, mock_stderr, mock_stdout):
        self._create_test_structure()
        mock_parse_args.return_value = MagicMock(
            path=self.test_dir,
            clean=True,
            verbose=False
        )
        main()
        mock_stdout.assert_called()
        self.assertIn("Cleanup complete", mock_stdout.mock_calls[-1].args[0])
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "empty_dir_1"))) # Should be removed
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "parent_dir", "empty_child_dir"))) # Should be removed
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "broken_link_1.txt"))) # Should be removed
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "non_empty_dir", "broken_link_2.txt"))) # Should be removed
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "broken_dir_link"))) # Should be removed

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        mock_parse_args.return_value = MagicMock(
            path="/non/existent/path",
            clean=False,
            verbose=False
        )
        main()
        mock_stderr.assert_called_with("Error: The specified path '/non/existent/path' is not a valid directory.", file=sys.stderr)
        mock_exit.assert_called_with(1)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_dust_found(self, mock_parse_args, mock_stderr, mock_stdout):
        # Create a clean directory with no empty dirs or broken links
        os.makedirs(os.path.join(self.test_dir, "only_files"))
        with open(os.path.join(self.test_dir, "only_files", "file.txt"), "w") as f:
            f.write("content")
        os.symlink(
            os.path.join(self.test_dir, "only_files", "file.txt"),
            os.path.join(self.test_dir, "only_files", "valid_link.txt")
        )

        mock_parse_args.return_value = MagicMock(
            path=self.test_dir,
            clean=True,
            verbose=False
        )
        main()
        mock_stdout.assert_called()
        self.assertIn("No empty directories found.", mock_stdout.mock_calls[5].args[0])
        self.assertIn("No broken symbolic links found.", mock_stdout.mock_calls[7].args[0])
        self.assertIn("Nothing to clean up.", mock_stdout.mock_calls[-2].args[0])


if __name__ == '__main__':
    unittest.main()
