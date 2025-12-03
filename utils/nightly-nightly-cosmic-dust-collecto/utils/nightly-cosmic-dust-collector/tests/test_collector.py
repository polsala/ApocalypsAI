import unittest
import os
import tempfile
import shutil
from unittest.mock import patch
from src.collector import collect_dust

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_dir = tempfile.mkdtemp()
        self.setup_test_structure()

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def setup_test_structure(self):
        # Create directories
        os.makedirs(os.path.join(self.test_dir, "empty_dir"))
        os.makedirs(os.path.join(self.test_dir, "dir_with_small_file"))
        os.makedirs(os.path.join(self.test_dir, "dir_with_large_file"))
        os.makedirs(os.path.join(self.test_dir, "nested_empty_dir", "sub_empty"))
        os.makedirs(os.path.join(self.test_dir, "nested_with_small_file", "sub_dir"))

        # Create files
        # Empty file
        with open(os.path.join(self.test_dir, "empty_file.txt"), "w") as f:
            pass
        # Small file (1 byte)
        with open(os.path.join(self.test_dir, "small_file.log"), "w") as f:
            f.write("a")
        # Another small file in a directory
        with open(os.path.join(self.test_dir, "dir_with_small_file", "tiny.dat"), "w") as f:
            f.write("b")
        # Large file (100 bytes)
        with open(os.path.join(self.test_dir, "dir_with_large_file", "important.txt"), "w") as f:
            f.write("x" * 100)
        # File in nested directory
        with open(os.path.join(self.test_dir, "nested_with_small_file", "sub_dir", "nested_tiny.tmp"), "w") as f:
            f.write("c")
        # File that should not be touched
        with open(os.path.join(self.test_dir, "keep_me.md"), "w") as f:
            f.write("This file is important and large enough.")

    def test_dry_run_identifies_empty_files_and_dirs(self):
        # Mock rationale: os.path.getsize is mocked to ensure deterministic file sizes
        # without relying on actual disk writes for specific byte counts, 
        # though tempfile already provides good isolation. This mock is more for
        # demonstrating the mocking principle for external interactions.
        with patch('os.path.getsize', side_effect=lambda p: {
            os.path.join(self.test_dir, "empty_file.txt"): 0,
            os.path.join(self.test_dir, "small_file.log"): 1,
            os.path.join(self.test_dir, "dir_with_small_file", "tiny.dat"): 1,
            os.path.join(self.test_dir, "dir_with_large_file", "important.txt"): 100,
            os.path.join(self.test_dir, "nested_with_small_file", "sub_dir", "nested_tiny.tmp"): 1,
            os.path.join(self.test_dir, "keep_me.md"): 50 # Ensure this is > min_file_size
        }.get(p, os.path.getsize(p))): # Fallback to actual getsize for unmocked paths
            report = collect_dust(self.test_dir, min_file_size_bytes=2, dry_run=True)

            self.assertTrue(report['dry_run'])
            self.assertEqual(report['total_files_removed'], 4) # empty_file, small_file, tiny.dat, nested_tiny.tmp
            self.assertEqual(report['total_dirs_removed'], 6) # empty_dir, dir_with_small_file, nested_empty_dir/sub_empty, nested_empty_dir, nested_with_small_file/sub_dir, nested_with_small_file

            # Check specific identified files (order might vary based on os.walk)
            expected_files = [
                f"[DRY RUN] {os.path.join(self.test_dir, 'empty_file.txt')} (0 bytes)",
                f"[DRY RUN] {os.path.join(self.test_dir, 'small_file.log')} (1 bytes)",
                f"[DRY RUN] {os.path.join(self.test_dir, 'dir_with_small_file', 'tiny.dat')} (1 bytes)",
                f"[DRY RUN] {os.path.join(self.test_dir, 'nested_with_small_file', 'sub_dir', 'nested_tiny.tmp')} (1 bytes)",
            ]
            for f in expected_files:
                self.assertIn(f, report['removed_files'])

            # Check specific identified directories (order might vary)
            expected_dirs = [
                f"[DRY RUN] {os.path.join(self.test_dir, 'empty_dir')}",
                f"[DRY RUN] {os.path.join(self.test_dir, 'dir_with_small_file')}",
                f"[DRY RUN] {os.path.join(self.test_dir, 'nested_empty_dir', 'sub_empty')}",
                f"[DRY RUN] {os.path.join(self.test_dir, 'nested_empty_dir')}",
                f"[DRY RUN] {os.path.join(self.test_dir, 'nested_with_small_file', 'sub_dir')}",
                f"[DRY RUN] {os.path.join(self.test_dir, 'nested_with_small_file')}"
            ]
            for d in expected_dirs:
                self.assertIn(d, report['removed_dirs'])

            # Ensure important files/dirs are still there
            self.assertTrue(os.path.exists(os.path.join(self.test_dir, "dir_with_large_file", "important.txt")))
            self.assertTrue(os.path.exists(os.path.join(self.test_dir, "keep_me.md")))
            self.assertTrue(os.path.exists(os.path.join(self.test_dir, "dir_with_large_file")))

    def test_actual_run_removes_files_and_dirs(self):
        # Mock rationale: os.path.getsize is mocked to ensure deterministic file sizes
        # without relying on actual disk writes for specific byte counts.
        with patch('os.path.getsize', side_effect=lambda p: {
            os.path.join(self.test_dir, "empty_file.txt"): 0,
            os.path.join(self.test_dir, "small_file.log"): 1,
            os.path.join(self.test_dir, "dir_with_small_file", "tiny.dat"): 1,
            os.path.join(self.test_dir, "dir_with_large_file", "important.txt"): 100,
            os.path.join(self.test_dir, "nested_with_small_file", "sub_dir", "nested_tiny.tmp"): 1,
            os.path.join(self.test_dir, "keep_me.md"): 50
        }.get(p, os.path.getsize(p))):
            report = collect_dust(self.test_dir, min_file_size_bytes=2, dry_run=False)

            self.assertFalse(report['dry_run'])
            self.assertEqual(report['total_files_removed'], 4)
            self.assertEqual(report['total_dirs_removed'], 6)
            self.assertEqual(report['total_space_freed_bytes'], 3) # 0 + 1 + 1 + 1 bytes

            # Verify actual removal
            self.assertFalse(os.path.exists(os.path.join(self.test_dir, "empty_file.txt")))
            self.assertFalse(os.path.exists(os.path.join(self.test_dir, "small_file.log")))
            self.assertFalse(os.path.exists(os.path.join(self.test_dir, "dir_with_small_file", "tiny.dat")))
            self.assertFalse(os.path.exists(os.path.join(self.test_dir, "nested_with_small_file", "sub_dir", "nested_tiny.tmp")))

            self.assertFalse(os.path.exists(os.path.join(self.test_dir, "empty_dir")))
            self.assertFalse(os.path.exists(os.path.join(self.test_dir, "dir_with_small_file")))
            self.assertFalse(os.path.exists(os.path.join(self.test_dir, "nested_empty_dir", "sub_empty")))
            self.assertFalse(os.path.exists(os.path.join(self.test_dir, "nested_empty_dir")))
            self.assertFalse(os.path.exists(os.path.join(self.test_dir, "nested_with_small_file", "sub_dir")))
            self.assertFalse(os.path.exists(os.path.join(self.test_dir, "nested_with_small_file")))

            # Ensure important files/dirs are still there
            self.assertTrue(os.path.exists(os.path.join(self.test_dir, "dir_with_large_file", "important.txt")))
            self.assertTrue(os.path.exists(os.path.join(self.test_dir, "keep_me.md")))
            self.assertTrue(os.path.exists(os.path.join(self.test_dir, "dir_with_large_file")))

    def test_invalid_path(self):
        report = collect_dust("/non/existent/path", dry_run=True)
        self.assertIn("error", report)
        self.assertIn("not a valid directory", report["error"])

    def test_min_file_size_zero(self):
        # If min_file_size_bytes is 0, it should only remove truly empty files (0 bytes)
        # Mock rationale: os.path.getsize is mocked to ensure deterministic file sizes.
        with patch('os.path.getsize', side_effect=lambda p: {
            os.path.join(self.test_dir, "empty_file.txt"): 0,
            os.path.join(self.test_dir, "small_file.log"): 1,
            os.path.join(self.test_dir, "dir_with_small_file", "tiny.dat"): 1,
            os.path.join(self.test_dir, "dir_with_large_file", "important.txt"): 100,
            os.path.join(self.test_dir, "nested_with_small_file", "sub_dir", "nested_tiny.tmp"): 1,
            os.path.join(self.test_dir, "keep_me.md"): 50
        }.get(p, os.path.getsize(p))):
            report = collect_dust(self.test_dir, min_file_size_bytes=0, dry_run=True)
            self.assertEqual(report['total_files_removed'], 1) # Only empty_file.txt (0 bytes)
            self.assertIn(f"[DRY RUN] {os.path.join(self.test_dir, 'empty_file.txt')} (0 bytes)", report['removed_files'])
            self.assertEqual(report['total_dirs_removed'], 3) # empty_dir, nested_empty_dir/sub_empty, nested_empty_dir (as they are truly empty)

    def test_min_file_size_large(self):
        # If min_file_size_bytes is large, it should remove more files
        # Mock rationale: os.path.getsize is mocked to ensure deterministic file sizes.
        with patch('os.path.getsize', side_effect=lambda p: {
            os.path.join(self.test_dir, "empty_file.txt"): 0,
            os.path.join(self.test_dir, "small_file.log"): 1,
            os.path.join(self.test_dir, "dir_with_small_file", "tiny.dat"): 1,
            os.path.join(self.test_dir, "dir_with_large_file", "important.txt"): 100,
            os.path.join(self.test_dir, "nested_with_small_file", "sub_dir", "nested_tiny.tmp"): 1,
            os.path.join(self.test_dir, "keep_me.md"): 50
        }.get(p, os.path.getsize(p))):
            report = collect_dust(self.test_dir, min_file_size_bytes=60, dry_run=True) # Files < 60 bytes

            # Files to remove: empty_file (0), small_file (1), tiny.dat (1), nested_tiny.tmp (1), keep_me.md (50)
            self.assertEqual(report['total_files_removed'], 5)
            self.assertIn(f"[DRY RUN] {os.path.join(self.test_dir, 'keep_me.md')} (50 bytes)", report['removed_files'])

            # Dirs to remove: empty_dir, dir_with_small_file, nested_empty_dir/sub_empty, nested_empty_dir, nested_with_small_file/sub_dir, nested_with_small_file
            self.assertEqual(report['total_dirs_removed'], 6)
