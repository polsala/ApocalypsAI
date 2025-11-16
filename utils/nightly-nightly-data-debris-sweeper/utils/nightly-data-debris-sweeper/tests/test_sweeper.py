import unittest
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the functions to be tested
from src.sweeper import find_debris, sweep_debris, DEFAULT_PATTERNS

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = Path.cwd()
        os.chdir(self.test_dir) # Change CWD for relative path testing

        # Create some test files and directories
        (self.test_dir / "__pycache__").mkdir()
        (self.test_dir / ".pytest_cache").mkdir()
        (self.test_dir / "build").mkdir()
        (self.test_dir / "dist").mkdir()
        (self.test_dir / "node_modules").mkdir()
        (self.test_dir / "target").mkdir() # For Rust/Java
        (self.test_dir / "temp.log").touch()
        (self.test_dir / "another.tmp").touch()
        (self.test_dir / "important_file.txt").touch()
        (self.test_dir / "subdir").mkdir()
        (self.test_dir / "subdir" / "sub_log.log").touch()
        (self.test_dir / "subdir" / "sub_pycache").mkdir() # This should be found as a directory
        (self.test_dir / "subdir" / "important_sub_file.md").touch()

    def tearDown(self):
        # Clean up the temporary directory
        os.chdir(self.original_cwd) # Restore CWD
        shutil.rmtree(self.test_dir)

    def test_find_debris_default_patterns(self):
        # Test finding debris with default patterns
        debris = find_debris(self.test_dir, DEFAULT_PATTERNS)
        found_paths = sorted([p.relative_to(self.test_dir) for p in debris])

        expected_paths = sorted([
            Path("__pycache__"),
            Path(".pytest_cache"),
            Path("build"),
            Path("dist"),
            Path("node_modules"),
            Path("target"),
            Path("temp.log"),
            Path("another.tmp"),
            Path("subdir/sub_log.log"),
            Path("subdir/sub_pycache")
        ])
        self.assertListEqual(found_paths, expected_paths)

    def test_find_debris_custom_patterns(self):
        # Test finding debris with custom patterns
        custom_patterns = ["*.txt", "subdir/"] # subdir/ should match the directory
        debris = find_debris(self.test_dir, custom_patterns)
        found_paths = sorted([p.relative_to(self.test_dir) for p in debris])

        expected_paths = sorted([
            Path("important_file.txt"),
            Path("subdir")
        ])
        self.assertListEqual(found_paths, expected_paths)

    def test_find_debris_no_match(self):
        # Test when no debris matches the patterns
        debris = find_debris(self.test_dir, ["*.xyz"])
        self.assertEqual(len(debris), 0)

    @patch('src.sweeper.shutil.rmtree')
    @patch('src.sweeper.os.remove')
    @patch('builtins.print') # Mock rationale: Capture print output for verification without actual console output.
    def test_sweep_debris_dry_run(self, mock_print, mock_os_remove, mock_shutil_rmtree):
        # Test dry run mode
        sweep_debris(self.test_dir, DEFAULT_PATTERNS, dry_run=True)

        mock_os_remove.assert_not_called()
        mock_shutil_rmtree.assert_not_called()
        mock_print.assert_any_call(unittest.mock.ANY) # Check that print was called
        mock_print.assert_any_call("[DRY RUN] No files or directories were deleted. To perform actual deletion, remove --dry-run.")

        # Verify files still exist
        self.assertTrue((self.test_dir / "__pycache__").is_dir())
        self.assertTrue((self.test_dir / "temp.log").is_file())

    @patch('builtins.print') # Mock rationale: Capture print output for verification without actual console output.
    def test_sweep_debris_actual_deletion(self, mock_print):
        # Test actual deletion mode
        # We don't mock os.remove or shutil.rmtree here to test actual file system interaction
        # within the temporary directory. This is safe because it's a temp directory.
        initial_debris_count = len(find_debris(self.test_dir, DEFAULT_PATTERNS))
        self.assertGreater(initial_debris_count, 0)

        sweep_debris(self.test_dir, DEFAULT_PATTERNS, dry_run=False)

        # Verify that the debris is actually gone
        self.assertFalse((self.test_dir / "__pycache__").exists())
        self.assertFalse((self.test_dir / ".pytest_cache").exists())
        self.assertFalse((self.test_dir / "build").exists())
        self.assertFalse((self.test_dir / "dist").exists())
        self.assertFalse((self.test_dir / "node_modules").exists())
        self.assertFalse((self.test_dir / "target").exists())
        self.assertFalse((self.test_dir / "temp.log").exists())
        self.assertFalse((self.test_dir / "another.tmp").exists())
        self.assertFalse((self.test_dir / "subdir" / "sub_log.log").exists())
        self.assertFalse((self.test_dir / "subdir" / "sub_pycache").exists())

        # Verify important files are still there
        self.assertTrue((self.test_dir / "important_file.txt").is_file())
        self.assertTrue((self.test_dir / "subdir" / "important_sub_file.md").is_file())

        # Verify print output indicates deletion
        mock_print.assert_any_call("✅ Sweep complete! 10 items of debris purged.") # Based on setUp items

    @patch('builtins.print') # Mock rationale: Capture print output for verification without actual console output.
    def test_sweep_debris_no_debris(self, mock_print):
        # Create a clean directory with no debris
        clean_dir = Path(tempfile.mkdtemp())
        (clean_dir / "safe_file.txt").touch()

        sweep_debris(clean_dir, DEFAULT_PATTERNS, dry_run=False)

        mock_print.assert_any_call("✨ No data debris found. Your repository is pristine!")
        self.assertTrue((clean_dir / "safe_file.txt").is_file()) # Ensure safe file is untouched
        shutil.rmtree(clean_dir) # Clean up

    @patch('src.sweeper.shutil.rmtree', side_effect=OSError("Permission denied"))
    @patch('builtins.print') # Mock rationale: Capture print output for verification without actual console output.
    def test_sweep_debris_error_handling(self, mock_print, mock_rmtree):
        # Test error handling during deletion
        # We'll only test directory deletion error for simplicity, file deletion would be similar
        # Need to ensure the directory actually exists for the mock to be called with it
        (self.test_dir / "__pycache__").mkdir(exist_ok=True)
        sweep_debris(self.test_dir, ["__pycache__"], dry_run=False)

        mock_rmtree.assert_called_once_with(self.test_dir / "__pycache__")
        mock_print.assert_any_call(unittest.mock.ANY)
        mock_print.assert_any_call(f"❌ Failed to sweep __pycache__: Permission denied")
        # Ensure other files are still there if only __pycache__ was targeted and failed
        self.assertTrue((self.test_dir / "temp.log").is_file())


if __name__ == '__main__':
    unittest.main()
