import unittest
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

# Mock rationale: We need to test file system operations without actually
# modifying the user's file system. Using `tempfile` allows us to create
# an isolated, temporary directory structure for each test, ensuring
# determinism and preventing side effects. We don't need to mock `os.remove`
# or `shutil.rmtree` directly because `tempfile` provides a safe sandbox.
# The `print` statements are mocked to prevent test output clutter.

from src.sweeper import sweep_directory, DEFAULT_PATTERNS

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for each test
        self.test_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.test_dir) # Ensure cleanup after test

        # Mock print to suppress output during tests
        self.patcher = patch('builtins.print')
        self.mock_print = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def _create_test_structure(self, structure_map):
        """
        Helper to create files and directories based on a dictionary map.
        Keys are relative paths, values are 'dir' or 'file'.
        """
        for rel_path, item_type in structure_map.items():
            full_path = self.test_dir / rel_path
            if item_type == 'dir':
                full_path.mkdir(parents=True, exist_ok=True)
            elif item_type == 'file':
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.touch()

    def test_sweep_directory_deletes_default_patterns(self):
        # Create a test structure with default "dust bunnies"
        structure = {
            "project_root/src/main.py": "file",
            "project_root/__pycache__/cache.pyc": "file",
            "project_root/node_modules/package/index.js": "file",
            "project_root/dist/bundle.js": "file",
            "project_root/build/output.txt": "file",
            "project_root/target/classes/MyClass.class": "file",
            "project_root/.DS_Store": "file",
            "project_root/temp.log": "file",
            "project_root/backup.bak": "file",
            "project_root/.vscode/settings.json": "file",
            "project_root/.idea/workspace.xml": "file",
            "project_root/nested/temp.tmp": "file",
            "project_root/important_file.txt": "file",
            "project_root/another_dir/sub_dir/file.txt": "file",
        }
        self._create_test_structure(structure)

        # Run the sweeper
        root_to_sweep = self.test_dir / "project_root"
        deleted_paths = sweep_directory(root_to_sweep, DEFAULT_PATTERNS, dry_run=False)

        # Assertions: Check if expected items are deleted and others remain
        expected_deleted_names = {
            "__pycache__", "node_modules", "dist", "build", "target",
            ".DS_Store", "temp.log", "backup.bak", ".vscode", ".idea",
            "temp.tmp" # This is a file, so it will be deleted
        }
        
        # Check if the actual paths exist
        self.assertFalse((root_to_sweep / "__pycache__").exists())
        self.assertFalse((root_to_sweep / "node_modules").exists())
        self.assertFalse((root_to_sweep / "dist").exists())
        self.assertFalse((root_to_sweep / "build").exists())
        self.assertFalse((root_to_sweep / "target").exists())
        self.assertFalse((root_to_sweep / ".DS_Store").exists())
        self.assertFalse((root_to_sweep / "temp.log").exists())
        self.assertFalse((root_to_sweep / "backup.bak").exists())
        self.assertFalse((root_to_sweep / ".vscode").exists())
        self.assertFalse((root_to_sweep / ".idea").exists())
        self.assertFalse((root_to_sweep / "nested/temp.tmp").exists()) # Check nested file

        # Check if important files/dirs remain
        self.assertTrue((root_to_sweep / "src/main.py").exists())
        self.assertTrue((root_to_sweep / "important_file.txt").exists())
        self.assertTrue((root_to_sweep / "another_dir/sub_dir/file.txt").exists())

        # Check the returned list of deleted paths (approximate count)
        # The exact paths might vary due to rglob order and how sub-items are reported
        # if a parent dir is deleted. We'll check if the *names* of deleted items
        # are generally correct.
        deleted_names = {p.name for p in deleted_paths}
        self.assertTrue(expected_deleted_names.issubset(deleted_names))
        # Ensure no critical files were accidentally deleted
        self.assertNotIn("main.py", deleted_names)
        self.assertNotIn("important_file.txt", deleted_names)
        self.assertNotIn("file.txt", deleted_names)


    def test_sweep_directory_with_custom_patterns(self):
        # Create a test structure with custom "dust bunnies"
        structure = {
            "project_root/custom_temp_dir/file.txt": "file",
            "project_root/another_custom_file.junk": "file",
            "project_root/important_config.yaml": "file",
        }
        self._create_test_structure(structure)

        custom_patterns = ["custom_temp_dir", "*.junk"]
        root_to_sweep = self.test_dir / "project_root"
        deleted_paths = sweep_directory(root_to_sweep, custom_patterns, dry_run=False)

        # Assertions
        self.assertFalse((root_to_sweep / "custom_temp_dir").exists())
        self.assertFalse((root_to_sweep / "another_custom_file.junk").exists())
        self.assertTrue((root_to_sweep / "important_config.yaml").exists())

        deleted_names = {p.name for p in deleted_paths}
        self.assertIn("custom_temp_dir", deleted_names)
        self.assertIn("another_custom_file.junk", deleted_names)
        self.assertNotIn("important_config.yaml", deleted_names)

    def test_sweep_directory_dry_run_mode(self):
        # Create a test structure
        structure = {
            "project_root/__pycache__/cache.pyc": "file",
            "project_root/important_file.txt": "file",
        }
        self._create_test_structure(structure)

        root_to_sweep = self.test_dir / "project_root"
        deleted_paths = sweep_directory(root_to_sweep, DEFAULT_PATTERNS, dry_run=True)

        # Assertions: Nothing should be deleted in dry run
        self.assertTrue((root_to_sweep / "__pycache__").exists())
        self.assertTrue((root_to_sweep / "__pycache__/cache.pyc").exists())
        self.assertTrue((root_to_sweep / "important_file.txt").exists())

        # The dry run should still report what *would* be deleted
        self.assertGreater(len(deleted_paths), 0)
        deleted_names = {p.name for p in deleted_paths}
        self.assertIn("__pycache__", deleted_names)

    def test_sweep_directory_non_existent_path(self):
        non_existent_path = self.test_dir / "non_existent_dir"
        deleted_paths = sweep_directory(non_existent_path, DEFAULT_PATTERNS, dry_run=False)
        self.assertEqual(deleted_paths, [])
        # Check that an error message was printed
        self.mock_print.assert_called_with(f"Error: Path '{non_existent_path}' is not a valid directory.")

    def test_sweep_directory_empty_patterns(self):
        structure = {
            "project_root/file.txt": "file",
            "project_root/dir/file.txt": "file",
        }
        self._create_test_structure(structure)
        root_to_sweep = self.test_dir / "project_root"
        deleted_paths = sweep_directory(root_to_sweep, [], dry_run=False)
        self.assertEqual(deleted_paths, [])
        self.assertTrue((root_to_sweep / "file.txt").exists())
        self.assertTrue((root_to_sweep / "dir/file.txt").exists())
        self.mock_print.assert_any_call("No digital dust bunnies found. Your repository is sparkling clean!")

    def test_sweep_directory_file_pattern_only(self):
        structure = {
            "project_root/test.log": "file",
            "project_root/nested/another.log": "file",
            "project_root/important.txt": "file",
        }
        self._create_test_structure(structure)
        root_to_sweep = self.test_dir / "project_root"
        deleted_paths = sweep_directory(root_to_sweep, ["*.log"], dry_run=False)

        self.assertFalse((root_to_sweep / "test.log").exists())
        self.assertFalse((root_to_sweep / "nested/another.log").exists())
        self.assertTrue((root_to_sweep / "important.txt").exists())

        deleted_names = {p.name for p in deleted_paths}
        self.assertIn("test.log", deleted_names)
        self.assertIn("another.log", deleted_names)
        self.assertNotIn("important.txt", deleted_names)

    def test_sweep_directory_dir_pattern_only(self):
        structure = {
            "project_root/temp_dir/file.txt": "file",
            "project_root/another_dir/sub_temp_dir/file2.txt": "file",
            "project_root/important_dir/file3.txt": "file",
        }
        self._create_test_structure(structure)
        root_to_sweep = self.test_dir / "project_root"
        deleted_paths = sweep_directory(root_to_sweep, ["temp_dir", "sub_temp_dir"], dry_run=False)

        self.assertFalse((root_to_sweep / "temp_dir").exists())
        self.assertFalse((root_to_sweep / "another_dir/sub_temp_dir").exists())
        self.assertTrue((root_to_sweep / "important_dir/file3.txt").exists())

        deleted_names = {p.name for p in deleted_paths}
        self.assertIn("temp_dir", deleted_names)
        self.assertIn("sub_temp_dir", deleted_names)
        self.assertNotIn("important_dir", deleted_names)


if __name__ == "__main__":
    unittest.main()
