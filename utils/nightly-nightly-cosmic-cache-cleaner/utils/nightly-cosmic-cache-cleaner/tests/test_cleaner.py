import unittest
import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Import the functions from the cleaner module
# Assuming the test file is in tests/ and cleaner.py is in src/
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from cleaner import clean_caches, get_directory_size, format_bytes

class TestCosmicCacheCleaner(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_root = Path("temp_test_root")
        self.test_root.mkdir(exist_ok=True)

        # Create some dummy files and directories
        # Project 1 with __pycache__ and node_modules
        (self.test_root / "project1").mkdir()
        (self.test_root / "project1" / "src").mkdir()
        (self.test_root / "project1" / "src" / "__pycache__").mkdir()
        (self.test_root / "project1" / "src" / "__pycache__" / "file1.pyc").touch()
        (self.test_root / "project1" / "node_modules").mkdir()
        (self.test_root / "project1" / "node_modules" / "packageA").mkdir()
        (self.test_root / "project1" / "node_modules" / "packageA" / "index.js").touch()
        (self.test_root / "project1" / "file.txt").touch()

        # Project 2 with .pytest_cache
        (self.test_root / "project2").mkdir()
        (self.test_root / "project2" / ".pytest_cache").mkdir()
        (self.test_root / "project2" / ".pytest_cache" / "v").mkdir()
        (self.test_root / "project2" / ".pytest_cache" / "v" / "cache.json").touch()

        # Project 3 with no caches
        (self.test_root / "project3").mkdir()
        (self.test_root / "project3" / "main.py").touch()

        # Nested cache
        (self.test_root / "nested_project").mkdir()
        (self.test_root / "nested_project" / "sub_dir").mkdir()
        (self.test_root / "nested_project" / "sub_dir" / "__pycache__").mkdir()
        (self.test_root / "nested_project" / "sub_dir" / "__pycache__" / "nested.pyc").touch()

        # Mock os.path.getsize for deterministic size calculation
        # Mock rationale: `os.path.getsize` depends on actual file content,
        # which can vary. Mocking it ensures deterministic test results
        # by returning a fixed size for any file, simplifying size calculations.
        self.mock_getsize_patch = patch('os.path.getsize', return_value=100)
        self.mock_getsize = self.mock_getsize_patch.start()

        # Mock Path.stat().st_size for pathlib.Path.stat().st_size
        # Mock rationale: Similar to os.path.getsize, Path.stat().st_size
        # returns actual file sizes. Mocking it ensures deterministic
        # size calculations for files created in tests.
        self.mock_stat_patch = patch('pathlib.Path.stat')
        self.mock_stat = self.mock_stat_patch.start()
        self.mock_stat.return_value = MagicMock(st_size=100)


    def tearDown(self):
        # Clean up the temporary directory
        if self.test_root.exists():
            shutil.rmtree(self.test_root)
        self.mock_getsize_patch.stop()
        self.mock_stat_patch.stop()

    def test_get_directory_size(self):
        # Test with a known directory structure and mocked file sizes
        # project1/src/__pycache__/file1.pyc (100B)
        # project1/node_modules/packageA/index.js (100B)
        # project1/file.txt (100B)
        # Total files in project1: 3 * 100B = 300B
        expected_size = 300 # 3 files * 100 bytes/file
        actual_size = get_directory_size(self.test_root / "project1")
        self.assertEqual(actual_size, expected_size)

        # Test with an empty directory
        (self.test_root / "empty_dir").mkdir()
        self.assertEqual(get_directory_size(self.test_root / "empty_dir"), 0)

    def test_format_bytes(self):
        self.assertEqual(format_bytes(0), "0.00 B")
        self.assertEqual(format_bytes(100), "100.00 B")
        self.assertEqual(format_bytes(1024), "1.00 KB")
        self.assertEqual(format_bytes(1024 * 1024), "1.00 MB")
        self.assertEqual(format_bytes(1.5 * 1024 * 1024 * 1024), "1.50 GB")

    @patch('sys.stdout', new_callable=StringIO)
    def test_dry_run_default_patterns(self, mock_stdout):
        # Default patterns: __pycache__, node_modules, .pytest_cache, .mypy_cache
        # Expected: project1/__pycache__, project1/node_modules, project2/.pytest_cache, nested_project/sub_dir/__pycache__
        # Each cache dir contains 1 file (100B) or 2 files (200B for .pytest_cache)
        # project1/__pycache__ (1 file = 100B)
        # project1/node_modules (1 file = 100B)
        # project2/.pytest_cache (1 file = 100B)
        # nested_project/sub_dir/__pycache__ (1 file = 100B)
        # Total: 4 files * 100B = 400B
        expected_total_size = 400

        returned_size = clean_caches(self.test_root, ["__pycache__", "node_modules", ".pytest_cache"], dry_run=True, verbose=True)

        self.assertEqual(returned_size, expected_total_size)
        output = mock_stdout.getvalue()
        self.assertIn("Mode: Dry Run", output)
        self.assertIn("Would delete: temp_test_root/project1/src/__pycache__ (100.00 B)", output)
        self.assertIn("Would delete: temp_test_root/project1/node_modules (100.00 B)", output)
        self.assertIn("Would delete: temp_test_root/project2/.pytest_cache (100.00 B)", output)
        self.assertIn("Would delete: temp_test_root/nested_project/sub_dir/__pycache__ (100.00 B)", output)
        self.assertIn("Summary: 400.00 B would have been reclaimed.", output)

        # Assert that directories still exist after dry run
        self.assertTrue((self.test_root / "project1" / "src" / "__pycache__").exists())
        self.assertTrue((self.test_root / "project1" / "node_modules").exists())
        self.assertTrue((self.test_root / "project2" / ".pytest_cache").exists())
        self.assertTrue((self.test_root / "nested_project" / "sub_dir" / "__pycache__").exists())

    @patch('sys.stdout', new_callable=StringIO)
    def test_actual_deletion_specific_pattern(self, mock_stdout):
        # Only target node_modules
        expected_total_size = 100 # project1/node_modules has 1 file (100B)

        returned_size = clean_caches(self.test_root, ["node_modules"], dry_run=False, verbose=True)

        self.assertEqual(returned_size, expected_total_size)
        output = mock_stdout.getvalue()
        self.assertIn("Mode: Actual Deletion", output)
        self.assertIn("Deleting: temp_test_root/project1/node_modules (100.00 B)", output)
        self.assertIn("Summary: 100.00 B reclaimed.", output)

        # Assert that node_modules is deleted
        self.assertFalse((self.test_root / "project1" / "node_modules").exists())
        # Assert other caches still exist
        self.assertTrue((self.test_root / "project1" / "src" / "__pycache__").exists())
        self.assertTrue((self.test_root / "project2" / ".pytest_cache").exists())

    @patch('sys.stdout', new_callable=StringIO)
    def test_no_matching_directories(self, mock_stdout):
        returned_size = clean_caches(self.test_root, ["non_existent_cache"], dry_run=True)
        self.assertEqual(returned_size, 0)
        output = mock_stdout.getvalue()
        self.assertIn("No matching cache directories found.", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_root_path(self, mock_stdout):
        invalid_path = Path("non_existent_root")
        returned_size = clean_caches(invalid_path, ["__pycache__"], dry_run=True)
        self.assertEqual(returned_size, 0)
        output = mock_stdout.getvalue()
        self.assertIn("Error: Root path 'non_existent_root' is not a valid directory.", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_actual_deletion_multiple_patterns(self, mock_stdout):
        # Target __pycache__ and .pytest_cache
        # project1/src/__pycache__ (1 file = 100B)
        # project2/.pytest_cache (1 file = 100B)
        # nested_project/sub_dir/__pycache__ (1 file = 100B)
        # Total: 3 files * 100B = 300B
        expected_total_size = 300

        returned_size = clean_caches(self.test_root, ["__pycache__", ".pytest_cache"], dry_run=False, verbose=True)

        self.assertEqual(returned_size, expected_total_size)
        output = mock_stdout.getvalue()
        self.assertIn("Mode: Actual Deletion", output)
        self.assertIn("Deleting: temp_test_root/project1/src/__pycache__ (100.00 B)", output)
        self.assertIn("Deleting: temp_test_root/project2/.pytest_cache (100.00 B)", output)
        self.assertIn("Deleting: temp_test_root/nested_project/sub_dir/__pycache__ (100.00 B)", output)
        self.assertIn("Summary: 300.00 B reclaimed.", output)

        # Assert targeted directories are deleted
        self.assertFalse((self.test_root / "project1" / "src" / "__pycache__").exists())
        self.assertFalse((self.test_root / "project2" / ".pytest_cache").exists())
        self.assertFalse((self.test_root / "nested_project" / "sub_dir" / "__pycache__").exists())
        # Assert non-targeted directories still exist
        self.assertTrue((self.test_root / "project1" / "node_modules").exists())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('shutil.rmtree')
    def test_deletion_error_handling(self, mock_rmtree, mock_stdout):
        # Mock rmtree to raise an error for a specific path
        mock_rmtree.side_effect = lambda path: \
            os.error("Permission denied") if "project1" in str(path) else None

        # Target __pycache__ and .pytest_cache
        # project1/src/__pycache__ (error expected)
        # project2/.pytest_cache (should be deleted)
        # nested_project/sub_dir/__pycache__ (should be deleted)
        # Total expected size from successful deletions: 200B (2 * 100B)
        expected_total_size = 200

        returned_size = clean_caches(self.test_root, ["__pycache__", ".pytest_cache"], dry_run=False, verbose=True)

        self.assertEqual(returned_size, expected_total_size)
        output = mock_stdout.getvalue()
        self.assertIn("Error processing", output)
        self.assertIn("Permission denied", output)
        self.assertIn("Deleting: temp_test_root/project2/.pytest_cache", output)
        self.assertIn("Deleting: temp_test_root/nested_project/sub_dir/__pycache__", output)
        self.assertIn("Summary: 200.00 B reclaimed.", output)

        # Assert that the directory that caused an error still exists
        self.assertTrue((self.test_root / "project1" / "src" / "__pycache__").exists())
        # Assert others were deleted
        self.assertFalse((self.test_root / "project2" / ".pytest_cache").exists())
        self.assertFalse((self.test_root / "nested_project" / "sub_dir" / "__pycache__").exists())


if __name__ == "__main__":
    unittest.main()
