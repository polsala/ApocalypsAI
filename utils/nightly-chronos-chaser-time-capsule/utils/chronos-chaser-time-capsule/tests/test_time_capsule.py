import unittest
import os
import shutil
import zipfile
import json
import hashlib
import datetime
from unittest.mock import patch, MagicMock
import tempfile

# Import the function to be tested
from src.time_capsule import create_time_capsule, calculate_md5

class TestTimeCapsule(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test artifacts
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()

        # Create dummy files and directories for testing
        self.file1_path = os.path.join(self.test_dir, "test_file1.txt")
        with open(self.file1_path, "w") as f:
            f.write("Content of test file 1.")

        self.file2_path = os.path.join(self.test_dir, "test_file2.log")
        with open(self.file2_path, "w") as f:
            f.write("Log entry 1\nLog entry 2")

        self.subdir_path = os.path.join(self.test_dir, "test_subdir")
        os.makedirs(self.subdir_path)
        self.subdir_file_path = os.path.join(self.subdir_path, "nested_file.md")
        with open(self.subdir_file_path, "w") as f:
            f.write("# Nested Markdown")

        # Mock datetime.datetime.now() to ensure deterministic timestamps
        # Mock rationale: Ensures consistent filenames and manifest timestamps across test runs.
        self.mock_datetime = datetime.datetime(2023, 10, 27, 14, 30, 0)
        self.patcher_datetime = patch('src.time_capsule.datetime.datetime')
        self.mock_dt_class = self.patcher_datetime.start()
        self.mock_dt_class.now.return_value = self.mock_datetime
        self.mock_dt_class.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

    def tearDown(self):
        # Clean up temporary directories
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.output_dir)
        self.patcher_datetime.stop()

    def test_calculate_md5(self):
        expected_md5 = hashlib.md5(b"Content of test file 1.").hexdigest()
        self.assertEqual(calculate_md5(self.file1_path), expected_md5)

    def test_create_single_file_capsule(self):
        zip_path = create_time_capsule(self.output_dir, self.file1_path)
        self.assertIsNotNone(zip_path)
        self.assertTrue(os.path.exists(zip_path))
        self.assertTrue(zip_path.endswith("time_capsule_20231027_143000.zip"))

        with zipfile.ZipFile(zip_path, 'r') as zf:
            file_list = zf.namelist()
            self.assertIn("manifest.json", file_list)
            self.assertIn("test_file1.txt", file_list)
            self.assertEqual(len(file_list), 2) # manifest + 1 file

            with zf.open("manifest.json") as f:
                manifest = json.load(f)
                self.assertEqual(manifest["creation_timestamp"], self.mock_datetime.isoformat())
                self.assertEqual(len(manifest["original_items"]), 1)
                item = manifest["original_items"][0]
                self.assertEqual(item["original_path"], os.path.abspath(self.file1_path))
                self.assertEqual(item["archived_name"], "test_file1.txt")
                self.assertEqual(item["type"], "file")
                self.assertEqual(item["size_bytes"], os.path.getsize(self.file1_path))
                self.assertEqual(item["md5_hash"], calculate_md5(self.file1_path))

    def test_create_multiple_items_capsule(self):
        zip_path = create_time_capsule(self.output_dir, self.file1_path, self.subdir_path)
        self.assertIsNotNone(zip_path)
        self.assertTrue(os.path.exists(zip_path))

        with zipfile.ZipFile(zip_path, 'r') as zf:
            file_list = zf.namelist()
            self.assertIn("manifest.json", file_list)
            self.assertIn("test_file1.txt", file_list)
            # Directories are included as entries, and their contents are also listed
            self.assertIn("test_subdir/", file_list) 
            self.assertIn("test_subdir/nested_file.md", file_list)
            # Expect manifest, test_file1.txt, test_subdir/, test_subdir/nested_file.md
            self.assertEqual(len(file_list), 4)

            with zf.open("manifest.json") as f:
                manifest = json.load(f)
                self.assertEqual(len(manifest["original_items"]), 2)
                file_item = next(item for item in manifest["original_items"] if item["type"] == "file")
                dir_item = next(item for item in manifest["original_items"] if item["type"] == "directory")

                self.assertEqual(file_item["original_path"], os.path.abspath(self.file1_path))
                self.assertEqual(file_item["archived_name"], "test_file1.txt")
                self.assertEqual(file_item["md5_hash"], calculate_md5(self.file1_path))

                self.assertEqual(dir_item["original_path"], os.path.abspath(self.subdir_path))
                self.assertEqual(dir_item["archived_name"], "test_subdir")
                self.assertEqual(dir_item["md5_hash"], "N/A") # As designed for directories

    def test_create_capsule_with_nonexistent_path(self):
        non_existent_path = os.path.join(self.test_dir, "non_existent.txt")
        # Expect a warning, but the capsule should still be created if other paths are valid
        zip_path = create_time_capsule(self.output_dir, self.file1_path, non_existent_path)
        self.assertIsNotNone(zip_path)
        self.assertTrue(os.path.exists(zip_path))

        with zipfile.ZipFile(zip_path, 'r') as zf:
            file_list = zf.namelist()
            self.assertIn("manifest.json", file_list)
            self.assertIn("test_file1.txt", file_list)
            self.assertEqual(len(file_list), 2) # Only the existing file + manifest

            with zf.open("manifest.json") as f:
                manifest = json.load(f)
                self.assertEqual(len(manifest["original_items"]), 1)
                self.assertEqual(manifest["original_items"][0]["archived_name"], "test_file1.txt")

    def test_create_capsule_no_valid_items(self):
        non_existent_path = os.path.join(self.test_dir, "non_existent.txt")
        zip_path = create_time_capsule(self.output_dir, non_existent_path)
        self.assertIsNone(zip_path)
        self.assertFalse(os.path.exists(os.path.join(self.output_dir, "time_capsule_20231027_143000.zip")))

    def test_duplicate_filenames_handled(self):
        # Create a file with the same base name in a different directory
        duplicate_file_dir = os.path.join(self.test_dir, "another_dir")
        os.makedirs(duplicate_file_dir)
        duplicate_file_path = os.path.join(duplicate_file_dir, "test_file1.txt")
        with open(duplicate_file_path, "w") as f:
            f.write("Content of duplicate file.")

        zip_path = create_time_capsule(self.output_dir, self.file1_path, duplicate_file_path)
        self.assertIsNotNone(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zf:
            file_list = zf.namelist()
            self.assertIn("test_file1.txt", file_list)
            self.assertIn("test_file1_1.txt", file_list) # Expect renaming
            self.assertEqual(len(file_list), 3) # manifest + 2 files

            with zf.open("manifest.json") as f:
                manifest = json.load(f)
                self.assertEqual(len(manifest["original_items"]), 2)
                item1 = next(item for item in manifest["original_items"] if item["original_path"] == os.path.abspath(self.file1_path))
                item2 = next(item for item in manifest["original_items"] if item["original_path"] == os.path.abspath(duplicate_file_path))

                self.assertEqual(item1["archived_name"], "test_file1.txt")
                self.assertEqual(item2["archived_name"], "test_file1_1.txt")

if __name__ == '__main__':
    unittest.main()
