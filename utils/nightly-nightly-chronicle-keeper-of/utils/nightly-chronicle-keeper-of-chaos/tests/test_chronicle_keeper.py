import unittest
import os
import tempfile
import shutil

# Mock rationale: The utility interacts with the file system. To ensure deterministic and offline tests,
# we create a temporary directory structure with known files and sizes. This avoids relying on the
# actual host file system state and makes tests repeatable. We don't need to mock os.walk or os.path.getsize
# directly because we are operating on a controlled, temporary, real file system.

from src.chronicle_keeper import generate_chronicle, format_size

class TestChronicleKeeper(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.base_path = self.test_dir

        # Create a sample directory structure and files
        os.makedirs(os.path.join(self.base_path, 'subdir1'))
        os.makedirs(os.path.join(self.base_path, 'subdir2', 'nested'))

        # Create files with specific sizes
        self._create_file(os.path.join(self.base_path, 'file_small.txt'), 100)
        self._create_file(os.path.join(self.base_path, 'subdir1', 'file_medium.log'), 5000)
        self._create_file(os.path.join(self.base_path, 'subdir2', 'data.json'), 15000)
        self._create_file(os.path.join(self.base_path, 'subdir2', 'nested', 'config.yml'), 200)
        self._create_file(os.path.join(self.base_path, 'large_asset.bin'), 100000)
        self._create_file(os.path.join(self.base_path, 'another_large.img'), 75000)
        self._create_file(os.path.join(self.base_path, 'empty.txt'), 0)

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def _create_file(self, path, size):
        """Helper to create a file with a specific size."""
        with open(path, 'wb') as f:
            f.write(os.urandom(size))

    def test_format_size(self):
        self.assertEqual(format_size(0), "0 Bytes")
        self.assertEqual(format_size(100), "100.0 Bytes")
        self.assertEqual(format_size(1024), "1.0 KB")
        self.assertEqual(format_size(1536), "1.5 KB")
        self.assertEqual(format_size(1024 * 1024), "1.0 MB")
        self.assertEqual(format_size(1024 * 1024 * 1.5), "1.5 MB")
        self.assertEqual(format_size(1024 * 1024 * 1024), "1.0 GB")

    def test_generate_chronicle_basic(self):
        output = generate_chronicle(self.base_path)
        
        # Expected values based on setUp
        expected_total_dirs = 3 # subdir1, subdir2, nested
        expected_total_files = 7 # file_small.txt, file_medium.log, data.json, config.yml, large_asset.bin, another_large.img, empty.txt
        expected_total_size = 100 + 5000 + 15000 + 200 + 100000 + 75000 + 0 # 195300 bytes

        self.assertIn(f"# Chronicle of {self.base_path}", output)
        self.assertIn(f"- **Total Directories:** {expected_total_dirs}", output)
        self.assertIn(f"- **Total Files:** {expected_total_files}", output)
        self.assertIn(f"- **Total Size:** {format_size(expected_total_size)}", output)

        # Check largest files (top 5)
        self.assertIn("## Largest Files (Top 5)", output)
        self.assertIn("`large_asset.bin`: 97.66 KB", output) # 100000 bytes
        self.assertIn("`another_large.img`: 73.24 KB", output) # 75000 bytes
        self.assertIn("`subdir2/data.json`: 14.65 KB", output) # 15000 bytes
        self.assertIn("`subdir1/file_medium.log`: 4.88 KB", output) # 5000 bytes
        self.assertIn("`subdir2/nested/config.yml`: 200.0 Bytes", output) # 200 bytes

    def test_generate_chronicle_empty_directory(self):
        empty_dir = os.path.join(self.base_path, 'empty_test_dir')
        os.makedirs(empty_dir)
        output = generate_chronicle(empty_dir)

        self.assertIn(f"# Chronicle of {empty_dir}", output)
        self.assertIn("- **Total Directories:** 0", output)
        self.assertIn("- **Total Files:** 0", output)
        self.assertIn("- **Total Size:** 0 Bytes", output)
        self.assertIn("No files found in this directory.", output)

    def test_generate_chronicle_non_existent_directory(self):
        non_existent_dir = os.path.join(self.base_path, 'non_existent')
        output = generate_chronicle(non_existent_dir)
        self.assertIn(f"# Error: Directory not found at {non_existent_dir}", output)

    def test_generate_chronicle_top_n_less_than_total(self):
        # Test with top_n=2
        output = generate_chronicle(self.base_path, top_n=2)
        self.assertIn("## Largest Files (Top 2)", output)
        self.assertIn("`large_asset.bin`: 97.66 KB", output)
        self.assertIn("`another_large.img`: 73.24 KB", output)
        self.assertNotIn("`subdir2/data.json`: 14.65 KB", output)

    def test_generate_chronicle_top_n_more_than_total(self):
        # Test with top_n=10 (more than 7 files)
        output = generate_chronicle(self.base_path, top_n=10)
        self.assertIn("## Largest Files (Top 10)", output)
        # All 7 files should be listed
        self.assertIn("`large_asset.bin`: 97.66 KB", output)
        self.assertIn("`another_large.img`: 73.24 KB", output)
        self.assertIn("`subdir2/data.json`: 14.65 KB", output)
        self.assertIn("`subdir1/file_medium.log`: 4.88 KB", output)
        self.assertIn("`subdir2/nested/config.yml`: 200.0 Bytes", output)
        self.assertIn("`file_small.txt`: 100.0 Bytes", output)
        self.assertIn("`empty.txt`: 0 Bytes", output)

if __name__ == '__main__':
    unittest.main()
