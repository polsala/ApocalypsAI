import unittest
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the functions to be tested
from src.cleaner import find_and_clean_caches, get_size_of_path, DEFAULT_INCLUDE_PATTERNS, DEFAULT_EXCLUDE_PATTERNS

class TestCosmicCacheCleaner(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing file system operations
        self.test_dir = Path(tempfile.mkdtemp())

        # Mock src.cleaner.get_size_of_path to return a fixed size for determinism
        # Mock rationale: Prevents actual file system size calculations, ensuring tests are fast and deterministic.
        self.mock_get_size = patch('src.cleaner.get_size_of_path', side_effect=lambda p: 1024 if p.is_file() else 2048)
        self.mock_get_size.start()

        # Mock shutil.rmtree and os.remove to prevent actual file deletion
        # Mock rationale: Prevents accidental deletion of real files and makes tests safe and isolated.
        self.mock_rmtree = patch('shutil.rmtree', MagicMock())
        self.mock_rmtree.start()
        self.mock_os_remove = patch('os.remove', MagicMock())
        self.mock_os_remove.start()

        # Keep track of what would be deleted by the mocks
        self.deleted_paths = []
        self.mock_rmtree.new.side_effect = lambda p, ignore_errors=False: self.deleted_paths.append(Path(p))
        self.mock_os_remove.new.side_effect = lambda p: self.deleted_paths.append(Path(p))

    def tearDown(self):
        # Stop all mocks
        self.mock_get_size.stop()
        self.mock_rmtree.stop()
        self.mock_os_remove.stop()

        # Clean up the temporary directory
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def _create_test_files(self, structure):
        """Helper to create a nested file/directory structure."""
        for path_str, is_dir in structure.items():
            path = self.test_dir / path_str
            if is_dir:
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()

    def test_find_and_clean_caches_dry_run(self):
        structure = {
            "project/src/main.py": False,
            "project/__pycache__/cache.pyc": False,
            "project/node_modules/package/index.js": False,
            "project/.venv/bin/python": False,
            "project/build/app.exe": False,
            "project/dist/lib.zip": False,
            "project/.git/config": False, # Should be excluded
            "project/docs/report.pdf": False,
            "project/temp.tmp": False,
            "project/another_dir/temp.tmp": False,
        }
        self._create_test_files(structure)

        # Run dry run with default patterns
        reclaimed_size = find_and_clean_caches(
            self.test_dir / "project",
            DEFAULT_INCLUDE_PATTERNS,
            DEFAULT_EXCLUDE_PATTERNS,
            dry_run=True
        )

        # Assertions for dry run
        self.assertGreater(reclaimed_size, 0)
        self.mock_rmtree.new.assert_not_called() # No actual deletion
        self.mock_os_remove.new.assert_not_called()

        # Check if the expected paths were identified (based on mock_get_size)
        # The mock_get_size returns 1024 for files, 2048 for directories.
        # __pycache__ (dir), node_modules (dir), .venv (dir), build (dir), dist (dir), temp.tmp (file), another_dir/temp.tmp (file)
        # Total 7 items. 5 dirs * 2048 + 2 files * 1024 = 10240 + 2048 = 12288
        self.assertEqual(reclaimed_size, 12288)

    def test_find_and_clean_caches_execute(self):
        structure = {
            "project/__pycache__/cache.pyc": False,
            "project/node_modules/package/index.js": False,
            "project/.git/config": False, # Should be excluded
        }
        self._create_test_files(structure)

        # Run execute with default patterns
        reclaimed_size = find_and_clean_caches(
            self.test_dir / "project",
            DEFAULT_INCLUDE_PATTERNS,
            DEFAULT_EXCLUDE_PATTERNS,
            dry_run=False
        )

        # Assertions for execute run
        self.assertGreater(reclaimed_size, 0)

        # Check if deletion mocks were called for expected paths
        expected_deleted_paths = [
            self.test_dir / "project" / "__pycache__",
            self.test_dir / "project" / "node_modules",
        ]
        # Convert to sets for order-independent comparison
        self.assertSetEqual(set(self.deleted_paths), set(expected_deleted_paths))

        # .git/config should NOT be deleted
        self.assertNotIn(self.test_dir / "project" / ".git", self.deleted_paths)
        self.assertNotIn(self.test_dir / "project" / ".git" / "config", self.deleted_paths)

    def test_custom_include_patterns(self):
        structure = {
            "repo/my_cache/data.txt": False,
            "repo/other_cache/temp.log": False,
            "repo/src/main.py": False,
        }
        self._create_test_files(structure)

        custom_includes = ["**/my_cache", "**/*.log"]
        reclaimed_size = find_and_clean_caches(
            self.test_dir / "repo",
            custom_includes,
            [], # No excludes
            dry_run=False
        )

        expected_deleted_paths = [
            self.test_dir / "repo" / "my_cache",
            self.test_dir / "repo" / "other_cache" / "temp.log",
        ]
        self.assertSetEqual(set(self.deleted_paths), set(expected_deleted_paths))
        self.assertEqual(reclaimed_size, 2048 + 1024) # my_cache (dir) + temp.log (file)

    def test_custom_exclude_patterns(self):
        structure = {
            "project/__pycache__/cache.pyc": False,
            "project/node_modules/package/index.js": False,
            "project/important_cache/data.bin": False,
        }
        self._create_test_files(structure)

        custom_excludes = ["**/important_cache"]
        reclaimed_size = find_and_clean_caches(
            self.test_dir / "project",
            DEFAULT_INCLUDE_PATTERNS,
            custom_excludes,
            dry_run=False
        )

        expected_deleted_paths = [
            self.test_dir / "project" / "__pycache__",
            self.test_dir / "project" / "node_modules",
        ]
        self.assertSetEqual(set(self.deleted_paths), set(expected_deleted_paths))
        self.assertNotIn(self.test_dir / "project" / "important_cache", self.deleted_paths)
        self.assertEqual(reclaimed_size, 2048 + 2048) # __pycache__ (dir) + node_modules (dir)

    def test_no_caches_found(self):
        structure = {
            "project/src/main.py": False,
            "project/docs/README.md": False,
        }
        self._create_test_files(structure)

        reclaimed_size = find_and_clean_caches(
            self.test_dir / "project",
            DEFAULT_INCLUDE_PATTERNS,
            DEFAULT_EXCLUDE_PATTERNS,
            dry_run=True
        )

        self.assertEqual(reclaimed_size, 0)
        self.mock_rmtree.new.assert_not_called()
        self.mock_os_remove.new.assert_not_called()

    def test_get_size_of_path_actual_implementation(self):
        # Temporarily stop the global mock for get_size_of_path to test its actual implementation
        self.mock_get_size.stop()
        try:
            # Test file size
            file_path = self.test_dir / "test_file.txt"
            file_path.touch()
            file_path.write_text("a" * 100)
            self.assertEqual(get_size_of_path(file_path), 100)

            # Test directory size
            dir_path = self.test_dir / "test_dir"
            dir_path.mkdir()
            (dir_path / "file1.txt").write_text("b" * 50)
            (dir_path / "subdir").mkdir()
            (dir_path / "subdir" / "file2.txt").write_text("c" * 75)
            self.assertEqual(get_size_of_path(dir_path), 50 + 75)

            # Test non-existent path
            self.assertEqual(get_size_of_path(self.test_dir / "non_existent"), 0)
        finally:
            # Re-start the global mock for subsequent tests
            self.mock_get_size.start()

if __name__ == '__main__':
    unittest.main()
