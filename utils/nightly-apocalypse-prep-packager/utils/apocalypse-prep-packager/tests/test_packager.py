import unittest
import os
import tempfile
import shutil
import zipfile
from unittest.mock import patch
import datetime

# Mock rationale: We need to control the timestamp for deterministic testing
# of the archive filename. By patching datetime.datetime.now, we ensure the
# generated filename is always the same for a given test run, making tests
# repeatable and independent of the actual time of execution.

# Import the function to be tested
from src.packager import create_apocalypse_package

class TestApocalypsePrepPackager(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for source files
        self.source_dir = tempfile.mkdtemp()
        # Create a temporary directory for output archives
        self.output_dir = tempfile.mkdtemp()

        # Create dummy files and directories for testing
        self.file1_path = os.path.join(self.source_dir, "file1.txt")
        with open(self.file1_path, "w") as f:
            f.write("Content of file 1")

        self.subdir_path = os.path.join(self.source_dir, "subdir")
        os.makedirs(self.subdir_path)
        self.file2_path = os.path.join(self.subdir_path, "file2.log")
        with open(self.file2_path, "w") as f:
            f.write("Log entry 1\nLog entry 2")

        self.empty_file_path = os.path.join(self.source_dir, "empty.dat")
        open(self.empty_file_path, "a").close() # Create an empty file

        # Define a fixed timestamp for deterministic testing
        self.fixed_timestamp_str = "20231027_123456"
        self.expected_archive_name = f"apocalypse_prep_{self.fixed_timestamp_str}.zip"
        self.expected_archive_path = os.path.join(self.output_dir, self.expected_archive_name)

    def tearDown(self):
        # Clean up temporary directories
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.output_dir)

    @patch('datetime.datetime')
    def test_package_single_file(self, mock_datetime):
        # Mock datetime.datetime.now() to return a fixed time
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 12, 34, 56)
        # Ensure strftime works on the mock object returned by now()
        mock_datetime.strftime = datetime.datetime.strftime

        source_paths = [self.file1_path]
        created_archive = create_apocalypse_package(source_paths, self.output_dir)

        self.assertTrue(os.path.exists(created_archive))
        self.assertEqual(created_archive, self.expected_archive_path)

        with zipfile.ZipFile(created_archive, 'r') as zf:
            self.assertIn(os.path.basename(self.file1_path), zf.namelist())
            self.assertEqual(zf.read(os.path.basename(self.file1_path)).decode(), "Content of file 1")
            self.assertEqual(len(zf.namelist()), 1)

    @patch('datetime.datetime')
    def test_package_directory(self, mock_datetime):
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 12, 34, 56)
        mock_datetime.strftime = datetime.datetime.strftime

        source_paths = [self.source_dir]
        created_archive = create_apocalypse_package(source_paths, self.output_dir)

        self.assertTrue(os.path.exists(created_archive))
        self.assertEqual(created_archive, self.expected_archive_path)

        with zipfile.ZipFile(created_archive, 'r') as zf:
            # When packaging a directory, the archive should contain the directory's base name
            # as the top-level entry, then its contents.
            expected_members = [
                os.path.basename(self.source_dir) + '/' + os.path.basename(self.file1_path),
                os.path.basename(self.source_dir) + '/' + os.path.basename(self.empty_file_path),
                os.path.basename(self.source_dir) + '/' + os.path.basename(self.subdir_path) + '/' + os.path.basename(self.file2_path),
            ]
            # Zipfile might add directory entries (e.g., 'source_dir/', 'source_dir/subdir/'),
            # so we check for file entries specifically.
            actual_members = [m for m in zf.namelist() if not m.endswith('/')]
            self.assertCountEqual(actual_members, expected_members)

            # Verify content of one file
            self.assertEqual(zf.read(expected_members[0]).decode(), "Content of file 1")

    @patch('datetime.datetime')
    def test_package_multiple_sources(self, mock_datetime):
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 12, 34, 56)
        mock_datetime.strftime = datetime.datetime.strftime

        # Package file1.txt and the subdir separately
        source_paths = [self.file1_path, self.subdir_path]
        created_archive = create_apocalypse_package(source_paths, self.output_dir)

        self.assertTrue(os.path.exists(created_archive))
        self.assertEqual(created_archive, self.expected_archive_path)

        with zipfile.ZipFile(created_archive, 'r') as zf:
            # When packaging multiple sources, files are at the root, directories retain their name.
            expected_members = [
                os.path.basename(self.file1_path),
                os.path.basename(self.subdir_path) + '/' + os.path.basename(self.file2_path),
            ]
            actual_members = [m for m in zf.namelist() if not m.endswith('/')]
            self.assertCountEqual(actual_members, expected_members)

            self.assertEqual(zf.read(os.path.basename(self.file1_path)).decode(), "Content of file 1")
            self.assertEqual(zf.read(os.path.basename(self.subdir_path) + '/' + os.path.basename(self.file2_path)).decode(), "Log entry 1\nLog entry 2")

    @patch('datetime.datetime')
    def test_source_path_not_found(self, mock_datetime):
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 12, 34, 56)
        mock_datetime.strftime = datetime.datetime.strftime

        non_existent_path = os.path.join(self.source_dir, "non_existent_file.txt")
        source_paths = [self.file1_path, non_existent_path]

        with self.assertRaises(FileNotFoundError) as cm:
            create_apocalypse_package(source_paths, self.output_dir)
        self.assertIn("Source path not found", str(cm.exception))
        self.assertFalse(os.path.exists(self.expected_archive_path))

    @patch('datetime.datetime')
    def test_output_directory_creation(self, mock_datetime):
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 12, 34, 56)
        mock_datetime.strftime = datetime.datetime.strftime

        new_output_dir = os.path.join(self.output_dir, "new_sub_dir")
        source_paths = [self.file1_path]
        created_archive = create_apocalypse_package(source_paths, new_output_dir)

        self.assertTrue(os.path.exists(new_output_dir))
        self.assertTrue(os.path.exists(created_archive))
        self.assertEqual(os.path.dirname(created_archive), new_output_dir)

    @patch('datetime.datetime')
    def test_empty_source_list(self, mock_datetime):
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 12, 34, 56)
        mock_datetime.strftime = datetime.datetime.strftime

        source_paths = []
        created_archive = create_apocalypse_package(source_paths, self.output_dir)

        self.assertTrue(os.path.exists(created_archive))
        self.assertEqual(created_archive, self.expected_archive_path)

        with zipfile.ZipFile(created_archive, 'r') as zf:
            self.assertEqual(len(zf.namelist()), 0) # Should create an empty zip file


if __name__ == '__main__':
    unittest.main()
