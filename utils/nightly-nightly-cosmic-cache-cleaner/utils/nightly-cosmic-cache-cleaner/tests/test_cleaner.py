import unittest
import os
import shutil
import tempfile
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Import the cleaner module from its expected path
from src.cleaner import clean_project, DEFAULT_CLEAN_CONFIG, get_cosmic_message

class TestCosmicCacheCleaner(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()

        # Create some files and directories to be cleaned
        os.makedirs(os.path.join(self.test_dir, "__pycache__"))
        os.makedirs(os.path.join(self.test_dir, "build"))
        os.makedirs(os.path.join(self.test_dir, "src", ".pytest_cache"))
        os.makedirs(os.path.join(self.test_dir, "nested", "dist"))
        os.makedirs(os.path.join(self.test_dir, "keep_this"))

        with open(os.path.join(self.test_dir, "main.pyc"), "w") as f:
            f.write("compiled")
        with open(os.path.join(self.test_dir, "app.log"), "w") as f:
            f.write("log data")
        with open(os.path.join(self.test_dir, "src", "temp.tmp"), "w") as f:
            f.write("temp data")
        with open(os.path.join(self.test_dir, "src", "config.py"), "w") as f:
            f.write("config data")
        with open(os.path.join(self.test_dir, ".DS_Store"), "w") as f:
            f.write("mac os metadata")
        with open(os.path.join(self.test_dir, "keep_this", "important.txt"), "w") as f:
            f.write("important data")

        # Create some files/dirs that should NOT be cleaned by default config
        os.makedirs(os.path.join(self.test_dir, "node_modules")) # Not in default config
        with open(os.path.join(self.test_dir, "package.json"), "w") as f:
            f.write("{}")

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)
        sys.stdout = self.original_stdout # Restore stdout

    def get_stdout(self):
        return sys.stdout.getvalue()

    def test_get_cosmic_message(self):
        self.assertIn("Scanning the digital nebula", get_cosmic_message("scanning", "project"))
        self.assertIn("temporal anomaly directory", get_cosmic_message("found_dir", "dir"))
        self.assertIn("Cosmic Cleansing Complete", get_cosmic_message("summary_start", ""))

    @patch('os.path.isdir')
    def test_clean_project_invalid_path(self, mock_isdir):
        # Mock rationale: Prevent actual file system checks for path validity
        # and simulate an invalid path without creating one.
        mock_isdir.return_value = False
        dirs, files = clean_project("/non/existent/path", DEFAULT_CLEAN_CONFIG, dry_run=True)
        self.assertEqual(dirs, 0)
        self.assertEqual(files, 0)
        self.assertIn("Error: Path '/non/existent/path' is not a valid directory.", self.get_stdout())

    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_clean_project_dry_run(self, mock_os_remove, mock_shutil_rmtree):
        # Mock rationale: Ensure no actual file system modifications occur during dry run tests.
        # We only want to verify that the correct paths are identified and reported.
        dirs_removed, files_removed = clean_project(self.test_dir, DEFAULT_CLEAN_CONFIG, dry_run=True)

        # In dry-run, nothing should be actually removed
        mock_shutil_rmtree.assert_not_called()
        mock_os_remove.assert_not_called()

        # The clean_project function returns 0,0 for dry_run because nothing was *actually* removed.
        # The output messages are what we need to check for dry-run.
        self.assertEqual(dirs_removed, 0)
        self.assertEqual(files_removed, 0)

        output = self.get_stdout()
        self.assertIn(get_cosmic_message("dry_run_dir", os.path.join(self.test_dir, "__pycache__")), output)
        self.assertIn(get_cosmic_message("dry_run_dir", os.path.join(self.test_dir, "build")), output)
        self.assertIn(get_cosmic_message("dry_run_dir", os.path.join(self.test_dir, "src", ".pytest_cache")), output)
        self.assertIn(get_cosmic_message("dry_run_dir", os.path.join(self.test_dir, "nested", "dist")), output)
        self.assertIn(get_cosmic_message("dry_run_file", os.path.join(self.test_dir, ".DS_Store")), output)
        self.assertIn(get_cosmic_message("dry_run_file", os.path.join(self.test_dir, "main.pyc")), output)
        self.assertIn(get_cosmic_message("dry_run_file", os.path.join(self.test_dir, "app.log")), output)
        self.assertIn(get_cosmic_message("dry_run_file", os.path.join(self.test_dir, "src", "temp.tmp")), output)

        # Ensure non-target items are not mentioned
        self.assertNotIn("important.txt", output)
        self.assertNotIn("config.py", output)
        self.assertNotIn("node_modules", output)

    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_clean_project_actual_run(self, mock_os_remove, mock_shutil_rmtree):
        # Mock rationale: Prevent actual file system modifications during tests.
        # We want to verify that `rmtree` and `remove` are called with the correct arguments.
        # The actual existence of files/dirs is handled by the setUp creating them,
        # and the mocks intercept the deletion calls.
        
        dirs_removed, files_removed = clean_project(self.test_dir, DEFAULT_CLEAN_CONFIG, dry_run=False)

        # Check that rmtree and remove were called for the correct items
        expected_dirs = [
            os.path.join(self.test_dir, "__pycache__"),
            os.path.join(self.test_dir, "build"),
            os.path.join(self.test_dir, "src", ".pytest_cache"),
            os.path.join(self.test_dir, "nested", "dist"),
        ]
        expected_files = [
            os.path.join(self.test_dir, ".DS_Store"),
            os.path.join(self.test_dir, "main.pyc"),
            os.path.join(self.test_dir, "app.log"),
            os.path.join(self.test_dir, "src", "temp.tmp"),
        ]

        self.assertEqual(mock_shutil_rmtree.call_count, len(expected_dirs))
        for d_path in expected_dirs:
            mock_shutil_rmtree.assert_any_call(d_path)

        self.assertEqual(mock_os_remove.call_count, len(expected_files))
        for f_path in expected_files:
            mock_os_remove.assert_any_call(f_path)

        self.assertEqual(dirs_removed, len(expected_dirs))
        self.assertEqual(files_removed, len(expected_files))

        output = self.get_stdout()
        self.assertIn(get_cosmic_message("removing_dir", os.path.join(self.test_dir, "__pycache__")), output)
        self.assertIn(get_cosmic_message("removing_file", os.path.join(self.test_dir, "main.pyc")), output)
        self.assertIn(get_cosmic_message("summary_dirs", str(len(expected_dirs))), output)
        self.assertIn(get_cosmic_message("summary_files", str(len(expected_files))), output)

        # Ensure non-target items are not mentioned
        self.assertNotIn("important.txt", output)
        self.assertNotIn("config.py", output)
        self.assertNotIn("node_modules", output)

    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_clean_project_no_clutter(self, mock_os_remove, mock_shutil_rmtree):
        # Mock rationale: Simulate a clean directory without creating all the clutter.
        # We'll create a minimal temp dir and run the cleaner.
        shutil.rmtree(self.test_dir) # Clear the default setup
        self.test_dir = tempfile.mkdtemp()
        with open(os.path.join(self.test_dir, "clean_file.txt"), "w") as f:
            f.write("clean")

        dirs_removed, files_removed = clean_project(self.test_dir, DEFAULT_CLEAN_CONFIG, dry_run=False)

        mock_shutil_rmtree.assert_not_called()
        mock_os_remove.assert_not_called()

        self.assertEqual(dirs_removed, 0)
        self.assertEqual(files_removed, 0)
        self.assertIn(get_cosmic_message("no_clutter", ""), self.get_stdout())

    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_clean_project_custom_config(self, mock_os_remove, mock_shutil_rmtree):
        # Mock rationale: Test that the cleaner respects custom configurations.
        # We'll use a custom config and verify the correct calls are made.
        custom_config = {
            "directories": ["custom_cache"],
            "file_patterns": ["*.temp"],
        }
        os.makedirs(os.path.join(self.test_dir, "custom_cache"))
        with open(os.path.join(self.test_dir, "data.temp"), "w") as f:
            f.write("temp data")

        # Also ensure default items are NOT cleaned with custom config
        # unless explicitly included.
        # The setUp creates default items, so they should be ignored here.

        dirs_removed, files_removed = clean_project(self.test_dir, custom_config, dry_run=False)

        self.assertEqual(dirs_removed, 1)
        self.assertEqual(files_removed, 1)

        mock_shutil_rmtree.assert_any_call(os.path.join(self.test_dir, "custom_cache"))
        mock_os_remove.assert_any_call(os.path.join(self.test_dir, "data.temp"))

        # Ensure default items were NOT removed
        self.assertNotIn(os.path.join(self.test_dir, "__pycache__"), [call.args[0] for call in mock_shutil_rmtree.call_args_list])
        self.assertNotIn(os.path.join(self.test_dir, "main.pyc"), [call.args[0] for call in mock_os_remove.call_args_list])

    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_clean_project_verbose_output(self, mock_os_remove, mock_shutil_rmtree):
        # Mock rationale: Verify that verbose output is generated when the flag is set.
        clean_project(self.test_dir, DEFAULT_CLEAN_CONFIG, dry_run=True, verbose=True)
        output = self.get_stdout()
        self.assertIn(get_cosmic_message("found_dir", os.path.join(self.test_dir, "__pycache__")), output)
        self.assertIn(get_cosmic_message("found_file", os.path.join(self.test_dir, "main.pyc")), output)
        self.assertIn(get_cosmic_message("dry_run_dir", os.path.join(self.test_dir, "__pycache__")), output)
        self.assertIn(get_cosmic_message("dry_run_file", os.path.join(self.test_dir, "main.pyc")), output)

    @patch('shutil.rmtree', side_effect=OSError("Permission denied"))
    @patch('os.remove', side_effect=OSError("Permission denied"))
    def test_clean_project_error_handling(self, mock_os_remove, mock_shutil_rmtree):
        # Mock rationale: Simulate OS errors during deletion to ensure graceful handling and reporting.
        dirs_removed, files_removed = clean_project(self.test_dir, DEFAULT_CLEAN_CONFIG, dry_run=False)

        # If errors occur, the counts should reflect 0 successful removals.
        self.assertEqual(dirs_removed, 0)
        self.assertEqual(files_removed, 0)

        output = self.get_stdout()
        self.assertIn("Failed to erase directory", output)
        self.assertIn("Failed to vaporize file", output)
        self.assertIn(get_cosmic_message("summary_dirs", "0"), output)
        self.assertIn(get_cosmic_message("summary_files", "0"), output)
        self.assertIn(get_cosmic_message("no_clutter", ""), output) # Because 0 items were successfully removed

if __name__ == '__main__':
    unittest.main()
