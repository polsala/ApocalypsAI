import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from pathlib import Path
from src.sweeper import DigitalDustBunnySweeper, main

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_root = Path("./temp_test_repo")
        self.test_root.mkdir(exist_ok=True)

        # Create various "dust bunnies"
        (self.test_root / "__pycache__").mkdir(exist_ok=True)
        (self.test_root / "__pycache__" / "foo.pyc").touch()

        (self.test_root / ".pytest_cache").mkdir(exist_ok=True)
        (self.test_root / ".pytest_cache" / "v").touch()

        (self.test_root / "src").mkdir(exist_ok=True)
        (self.test_root / "src" / "main.py").touch()
        (self.test_root / "src" / "__pycache__").mkdir(exist_ok=True)
        (self.test_root / "src" / "__pycache__" / "bar.pyc").touch()

        (self.test_root / "node_modules").mkdir(exist_ok=True)
        (self.test_root / "node_modules" / "some_lib").touch()

        (self.test_root / "target").mkdir(exist_ok=True)
        (self.test_root / "target" / "debug").touch()

        (self.test_root / "build").mkdir(exist_ok=True)
        (self.test_root / "build" / "temp.zip").touch()

        # A file that should NOT be deleted
        (self.test_root / "important_file.txt").touch()

    def tearDown(self):
        # Clean up the temporary directory
        if self.test_root.exists():
            shutil.rmtree(self.test_root)

    @patch('src.sweeper.shutil.rmtree')
    @patch('src.sweeper.os.remove')
    @patch('builtins.print')
    def test_dry_run_finds_items_but_does_not_delete(self, mock_print, mock_os_remove, mock_shutil_rmtree):
        # Mock rationale: We want to ensure the sweeper identifies the correct paths
        # without actually performing file system deletions during a dry run.
        # `shutil.rmtree` and `os.remove` are mocked to verify they are NOT called.
        # `builtins.print` is mocked to capture output for verification.

        sweeper = DigitalDustBunnySweeper(self.test_root, dry_run=True)
        sweeper.sweep()

        # Verify that deletion functions were NOT called
        mock_shutil_rmtree.assert_not_called()
        mock_os_remove.assert_not_called()

        # Verify that the sweeper found the expected items
        expected_found_items = [
            self.test_root / "__pycache__",
            self.test_root / ".pytest_cache",
            self.test_root / "src" / "__pycache__",
            self.test_root / "node_modules",
            self.test_root / "target",
            self.test_root / "build",
        ]
        # Convert to strings for easier comparison, as order might vary slightly due to os.walk
        found_item_strings = sorted([str(p) for p in sweeper.found_items])
        expected_item_strings = sorted([str(p) for p in expected_found_items])
        self.assertEqual(found_item_strings, expected_item_strings)

        # Verify print output indicates dry run and found items
        mock_print.assert_any_call(f"Scanning '{self.test_root.resolve()}' for digital dust bunnies...")
        mock_print.assert_any_call("DRY RUN: No files will be deleted.")
        mock_print.assert_any_call(f"  Would delete directory: {self.test_root / '__pycache__'}")
        mock_print.assert_any_call(f"  Would delete directory: {self.test_root / 'node_modules'}")
        self.assertTrue((self.test_root / "important_file.txt").exists()) # Ensure non-target files are untouched

    @patch('src.sweeper.shutil.rmtree')
    @patch('src.sweeper.os.remove')
    @patch('builtins.print')
    def test_sweep_deletes_items(self, mock_print, mock_os_remove, mock_shutil_rmtree):
        # Mock rationale: We want to ensure the sweeper calls the correct deletion
        # functions for the identified paths when not in dry-run mode.
        # `shutil.rmtree` and `os.remove` are mocked to verify they ARE called with correct arguments.
        # `builtins.print` is mocked to capture output for verification.

        sweeper = DigitalDustBunnySweeper(self.test_root, dry_run=False)
        sweeper.sweep()

        # Verify that deletion functions were called for directories
        mock_shutil_rmtree.assert_any_call(self.test_root / "__pycache__")
        mock_shutil_rmtree.assert_any_call(self.test_root / ".pytest_cache")
        mock_shutil_rmtree.assert_any_call(self.test_root / "src" / "__pycache__")
        mock_shutil_rmtree.assert_any_call(self.test_root / "node_modules")
        mock_shutil_rmtree.assert_any_call(self.test_root / "target")
        mock_shutil_rmtree.assert_any_call(self.test_root / "build")

        # Verify that os.remove was NOT called for directories (rmtree handles them)
        mock_os_remove.assert_not_called()

        # Verify print output indicates deletion
        mock_print.assert_any_call("DELETING files...")
        mock_print.assert_any_call(f"  Deleted directory: {self.test_root / '__pycache__'}")
        self.assertTrue((self.test_root / "important_file.txt").exists()) # Ensure non-target files are untouched

    @patch('src.sweeper.os.walk')
    @patch('src.sweeper.shutil.rmtree')
    @patch('src.sweeper.os.remove')
    @patch('builtins.print')
    def test_no_items_found(self, mock_print, mock_os_remove, mock_shutil_rmtree, mock_os_walk):
        # Mock rationale: Simulate a scenario where no "dust bunnies" exist
        # to ensure the utility handles this gracefully and doesn't attempt deletions.
        # `os.walk` is mocked to return an empty set of directories and files.
        # `shutil.rmtree` and `os.remove` are mocked to verify they are NOT called.
        # `builtins.print` is mocked to capture output for verification.

        # Configure os.walk to return no relevant directories/files
        mock_os_walk.return_value = [
            (str(self.test_root), [], ["important_file.txt"]),
            (str(self.test_root / "subdir"), [], ["another_file.txt"])
        ]

        sweeper = DigitalDustBunnySweeper(self.test_root, dry_run=False)
        sweeper.sweep()

        mock_shutil_rmtree.assert_not_called()
        mock_os_remove.assert_not_called()
        mock_print.assert_any_call("No digital dust bunnies found. Your repository is sparkling clean!")
        self.assertEqual(len(sweeper.found_items), 0)

    @patch('src.sweeper.shutil.rmtree')
    @patch('src.sweeper.os.remove')
    @patch('builtins.print')
    def test_error_during_deletion(self, mock_print, mock_os_remove, mock_shutil_rmtree):
        # Mock rationale: Simulate an OSError during deletion to ensure the utility
        # logs the error gracefully and continues processing other items.
        # `shutil.rmtree` is configured to raise an OSError for a specific path.
        # `builtins.print` is mocked to capture output for verification.

        # Make rmtree raise an error for the first call
        mock_shutil_rmtree.side_effect = [OSError("Permission denied"), None, None, None, None, None]

        sweeper = DigitalDustBunnySweeper(self.test_root, dry_run=False)
        sweeper.sweep()

        mock_print.assert_any_call(unittest.mock.ANY) # Scan message
        mock_print.assert_any_call("DELETING files...")
        mock_print.assert_any_call(f"  Error deleting: {self.test_root / '__pycache__'} - Permission denied")
        mock_print.assert_any_call(f"  Deleted directory: {self.test_root / '.pytest_cache'}") # Should still try to delete others
        self.assertEqual(mock_shutil_rmtree.call_count, 6) # Should attempt to delete all 6 items

    @patch('src.sweeper.DigitalDustBunnySweeper')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_calls_sweeper_correctly(self, mock_parse_args, MockDigitalDustBunnySweeper):
        # Mock rationale: Test the `main` function's integration with `argparse`
        # and `DigitalDustBunnySweeper` without actually running the full sweep logic.
        # `argparse.ArgumentParser.parse_args` is mocked to control CLI arguments.
        # `DigitalDustBunnySweeper` is mocked to verify its instantiation and `sweep` method call.

        # Configure mock_parse_args to return specific arguments
        mock_parse_args.return_value = MagicMock(path="/some/path", dry_run=True)

        # Call the main function
        main()

        # Verify that DigitalDustBunnySweeper was instantiated with correct arguments
        MockDigitalDustBunnySweeper.assert_called_once_with(Path("/some/path"), True)
        # Verify that the sweep method was called on the instantiated object
        MockDigitalDustBunnySweeper.return_value.sweep.assert_called_once()


if __name__ == '__main__':
    unittest.main()
