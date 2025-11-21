import unittest
import os
import json
import shutil
import tempfile
from unittest import mock
from datetime import datetime

# Mock rationale: We need to isolate file system operations and time-based functions
# to ensure deterministic and fast tests. `tempfile` creates a safe sandbox, and
# `mock.patch` allows us to control file content, hashes, modification times, and
# the current timestamp without actual disk I/O or waiting for real time.

# Import the class to be tested
from src.collector import CosmicDustCollector

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Create temporary directories for source and dustbin
        self.temp_source_dir = tempfile.mkdtemp()
        self.temp_dustbin_dir = tempfile.mkdtemp()
        self.manifest_path = os.path.join(self.temp_dustbin_dir, '_dust_manifest.json')

        # Mock datetime.now() to ensure consistent timestamps in archived filenames
        self.mock_datetime_now = mock.patch('src.collector.datetime')
        self.mock_dt = self.mock_datetime_now.start()
        self.mock_dt.now.return_value = datetime(2023, 10, 27, 12, 0, 0)
        self.mock_dt.strftime.return_value = '20231027120000'

        # Mock hashlib.md5 for deterministic hash generation
        self.mock_hashlib_md5 = mock.patch('src.collector.hashlib.md5')
        self.mock_md5 = self.mock_hashlib_md5.start()
        self.mock_md5_instance = mock.Mock()
        self.mock_md5.return_value = self.mock_md5_instance

        # Mock os.path.getmtime for deterministic modification times
        self.mock_getmtime = mock.patch('src.collector.os.path.getmtime')
        self.mock_getmtime_func = self.mock_getmtime.start()

    def tearDown(self):
        # Clean up temporary directories
        shutil.rmtree(self.temp_source_dir)
        shutil.rmtree(self.temp_dustbin_dir)

        # Stop all mocks
        self.mock_datetime_now.stop()
        self.mock_hashlib_md5.stop()
        self.mock_getmtime.stop()

    def _create_file(self, directory, filename, content, mtime_timestamp=None):
        filepath = os.path.join(directory, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        if mtime_timestamp is not None:
            os.utime(filepath, (mtime_timestamp, mtime_timestamp))
        return filepath

    def _set_mock_hash_and_mtime(self, content, hash_val, mtime_val):
        # Mock the md5 instance's hexdigest method
        self.mock_md5_instance.hexdigest.return_value = hash_val
        # Mock the os.path.getmtime function
        self.mock_getmtime_func.return_value = mtime_val

    def test_initial_collection_new_file(self):
        collector = CosmicDustCollector(self.temp_source_dir, self.temp_dustbin_dir)

        file_content = "initial content"
        file_hash = "hash1"
        file_mtime = 1678886400.0 # Example timestamp
        self._set_mock_hash_and_mtime(file_content, file_hash, file_mtime)

        self._create_file(self.temp_source_dir, "test_file.txt", file_content, file_mtime)

        collector.collect_dust()

        # Check if manifest is created and contains the file
        self.assertTrue(os.path.exists(self.manifest_path))
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
            self.assertIn("test_file.txt", manifest)
            self.assertEqual(manifest["test_file.txt"]['hash'], file_hash)
            self.assertEqual(manifest["test_file.txt"]['mtime'], file_mtime)

        # Check if file is archived
        archived_filename = "test_file.txt.20231027120000.bak"
        self.assertTrue(os.path.exists(os.path.join(self.temp_dustbin_dir, archived_filename)))

    def test_file_modification_archives_new_version(self):
        collector = CosmicDustCollector(self.temp_source_dir, self.temp_dustbin_dir)

        # First run: initial file
        file_content_1 = "initial content"
        file_hash_1 = "hash1"
        file_mtime_1 = 1678886400.0
        self._set_mock_hash_and_mtime(file_content_1, file_hash_1, file_mtime_1)
        self._create_file(self.temp_source_dir, "test_file.txt", file_content_1, file_mtime_1)
        collector.collect_dust()

        # Advance time for the next archive
        self.mock_dt.now.return_value = datetime(2023, 10, 27, 12, 1, 0)
        self.mock_dt.strftime.return_value = '20231027120100'

        # Second run: modified file
        file_content_2 = "modified content"
        file_hash_2 = "hash2"
        file_mtime_2 = 1678886460.0 # Different mtime
        self._set_mock_hash_and_mtime(file_content_2, file_hash_2, file_mtime_2)
        self._create_file(self.temp_source_dir, "test_file.txt", file_content_2, file_mtime_2)
        collector.collect_dust()

        # Check manifest update
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
            self.assertEqual(manifest["test_file.txt"]['hash'], file_hash_2)
            self.assertEqual(manifest["test_file.txt"]['mtime'], file_mtime_2)

        # Check if both versions are archived
        archived_filename_1 = "test_file.txt.20231027120000.bak"
        archived_filename_2 = "test_file.txt.20231027120100.bak"
        self.assertTrue(os.path.exists(os.path.join(self.temp_dustbin_dir, archived_filename_1)))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dustbin_dir, archived_filename_2)))

    def test_no_change_no_new_archive(self):
        collector = CosmicDustCollector(self.temp_source_dir, self.temp_dustbin_dir)

        file_content = "unchanged content"
        file_hash = "hash_unchanged"
        file_mtime = 1678886500.0
        self._set_mock_hash_and_mtime(file_content, file_hash, file_mtime)
        self._create_file(self.temp_source_dir, "test_file.txt", file_content, file_mtime)
        collector.collect_dust()

        # Reset mock_dt.now to ensure no new archive is created if time passes but content doesn't change
        self.mock_dt.now.return_value = datetime(2023, 10, 27, 12, 2, 0)
        self.mock_dt.strftime.return_value = '20231027120200'

        # Re-run collection without changing file content or mtime
        # We need to ensure the mock returns the *same* hash and mtime
        self._set_mock_hash_and_mtime(file_content, file_hash, file_mtime)
        collector.collect_dust()

        # Only one archived file should exist
        archived_files = [f for f in os.listdir(self.temp_dustbin_dir) if f.startswith("test_file.txt") and f.endswith(".bak")]
        self.assertEqual(len(archived_files), 1)
        self.assertIn("test_file.txt.20231027120000.bak", archived_files)

    def test_deleted_file_removed_from_manifest(self):
        collector = CosmicDustCollector(self.temp_source_dir, self.temp_dustbin_dir)

        file_content = "content to be deleted"
        file_hash = "hash_delete"
        file_mtime = 1678886600.0
        self._set_mock_hash_and_mtime(file_content, file_hash, file_mtime)
        filepath = self._create_file(self.temp_source_dir, "delete_me.txt", file_content, file_mtime)
        collector.collect_dust()

        # Verify it's in the manifest initially
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
            self.assertIn("delete_me.txt", manifest)

        # Delete the file from source
        os.remove(filepath)

        # Re-run collection
        collector.collect_dust()

        # Verify it's removed from the manifest
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
            self.assertNotIn("delete_me.txt", manifest)

    def test_subdirectory_handling(self):
        collector = CosmicDustCollector(self.temp_source_dir, self.temp_dustbin_dir)

        subdir = os.path.join(self.temp_source_dir, "sub", "dir")
        file_content = "subdir content"
        file_hash = "hash_subdir"
        file_mtime = 1678886700.0
        self._set_mock_hash_and_mtime(file_content, file_hash, file_mtime)
        self._create_file(subdir, "sub_file.txt", file_content, file_mtime)

        collector.collect_dust()

        # Check manifest entry for relative path
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
            self.assertIn(os.path.join("sub", "dir", "sub_file.txt"), manifest)

        # Check if archived file is in correct dustbin subdirectory
        archived_filename = "sub_file.txt.20231027120000.bak"
        expected_dustbin_path = os.path.join(self.temp_dustbin_dir, "sub", "dir", archived_filename)
        self.assertTrue(os.path.exists(expected_dustbin_path))

    def test_non_existent_source_directory_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            CosmicDustCollector("/non/existent/path", self.temp_dustbin_dir)

    def test_manifest_corruption_handled(self):
        # Create a corrupted manifest file
        with open(self.manifest_path, 'w') as f:
            f.write("{{{{invalid json")

        # Collector should initialize without error, manifest should be empty
        collector = CosmicDustCollector(self.temp_source_dir, self.temp_dustbin_dir)
        self.assertEqual(collector.manifest, {})

        # Add a file and collect dust to ensure it works after corruption
        file_content = "new content after corruption"
        file_hash = "hash_after_corruption"
        file_mtime = 1678886800.0
        self._set_mock_hash_and_mtime(file_content, file_hash, file_mtime)
        self._create_file(self.temp_source_dir, "corrupt_test.txt", file_content, file_mtime)
        collector.collect_dust()

        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
            self.assertIn("corrupt_test.txt", manifest)
            self.assertEqual(manifest["corrupt_test.txt"]['hash'], file_hash)

if __name__ == '__main__':
    unittest.main()
