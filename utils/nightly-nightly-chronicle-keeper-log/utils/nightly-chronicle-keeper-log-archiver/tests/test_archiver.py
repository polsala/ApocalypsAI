import unittest
import os
import shutil
import tempfile
from unittest.mock import patch, MagicMock
from datetime import datetime

# Import the function to be tested
from src.archiver import archive_logs

class TestArchiveLogs(unittest.TestCase):

    def setUp(self):
        # Create temporary directories for source and archive
        self.source_dir = tempfile.mkdtemp()
        self.archive_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up temporary directories
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.archive_dir)

    @patch('src.archiver.datetime')
    def test_archive_multiple_files_no_delete(self, mock_datetime):
        # Mock rationale: Ensure deterministic timestamp for archive filename.
        # When datetime.now() is called, it will return this specific datetime object.
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 30, 0)

        # Create dummy log files in source directory
        with open(os.path.join(self.source_dir, "log_a.log"), "w") as f:
            f.write("Content of log A.\n")
        with open(os.path.join(self.source_dir, "log_b.txt"), "w") as f:
            f.write("Content of log B.\n")
        with open(os.path.join(self.source_dir, "other.md"), "w") as f: # Should be ignored
            f.write("This should be ignored.\n")

        # Run the archiver
        success = archive_logs(self.source_dir, self.archive_dir, delete_originals=False)
        self.assertTrue(success)

        # Check if archive file was created
        expected_archive_filename = "chronicle_archive_2023-10-27_10-30-00.log"
        archive_filepath = os.path.join(self.archive_dir, expected_archive_filename)
        self.assertTrue(os.path.exists(archive_filepath))

        # Check content of the archive file
        with open(archive_filepath, "r") as f:
            content = f.read()
            self.assertIn("--- Start of log_a.log ---", content)
            self.assertIn("Content of log A.", content)
            self.assertIn("--- End of log_a.log ---", content)
            self.assertIn("--- Start of log_b.txt ---", content)
            self.assertIn("Content of log B.", content)
            self.assertIn("--- End of log_b.txt ---", content)
            self.assertNotIn("other.md", content) # Ensure ignored file is not in archive

        # Check if original files still exist
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "log_a.log")))
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "log_b.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "other.md")))

    @patch('src.archiver.datetime')
    def test_archive_multiple_files_with_delete(self, mock_datetime):
        # Mock rationale: Ensure deterministic timestamp for archive filename.
        mock_datetime.now.return_value = datetime(2023, 10, 27, 11, 0, 0)

        # Create dummy log files in source directory
        with open(os.path.join(self.source_dir, "log_c.log"), "w") as f:
            f.write("Content of log C.\n")
        with open(os.path.join(self.source_dir, "log_d.txt"), "w") as f:
            f.write("Content of log D.\n")

        # Run the archiver with deletion
        success = archive_logs(self.source_dir, self.archive_dir, delete_originals=True)
        self.assertTrue(success)

        # Check if archive file was created
        expected_archive_filename = "chronicle_archive_2023-10-27_11-00-00.log"
        archive_filepath = os.path.join(self.archive_dir, expected_archive_filename)
        self.assertTrue(os.path.exists(archive_filepath))

        # Check content (briefly)
        with open(archive_filepath, "r") as f:
            content = f.read()
            self.assertIn("Content of log C.", content)
            self.assertIn("Content of log D.", content)

        # Check if original files were deleted
        self.assertFalse(os.path.exists(os.path.join(self.source_dir, "log_c.log")))
        self.assertFalse(os.path.exists(os.path.join(self.source_dir, "log_d.txt")))
        self.assertEqual(len(os.listdir(self.source_dir)), 0) # Source dir should be empty

    @patch('src.archiver.datetime')
    def test_archive_no_files(self, mock_datetime):
        # Mock rationale: Ensure deterministic timestamp for archive filename.
        mock_datetime.now.return_value = datetime(2023, 10, 27, 12, 0, 0)

        # Source directory is empty
        success = archive_logs(self.source_dir, self.archive_dir, delete_originals=False)
        self.assertFalse(success) # Should return False as no files were archived

        # No archive file should be created
        self.assertEqual(len(os.listdir(self.archive_dir)), 0)

    def test_source_directory_not_found(self):
        non_existent_dir = "/path/to/nonexistent/source"
        success = archive_logs(non_existent_dir, self.archive_dir)
        self.assertFalse(success)
        self.assertEqual(len(os.listdir(self.archive_dir)), 0) # No archive should be created

    @patch('src.archiver.datetime')
    @patch('builtins.open', new_callable=MagicMock)
    def test_archiving_error_cleanup(self, mock_open, mock_datetime):
        # Mock rationale: Simulate an IOError during file writing to test cleanup.
        mock_datetime.now.return_value = datetime(2023, 10, 27, 13, 0, 0)

        # Create a dummy log file
        with open(os.path.join(self.source_dir, "error_log.log"), "w") as f:
            f.write("Error prone content.\n")

        # Configure mock_open to raise an IOError when writing to the archive file
        # The first call (opening source file) should succeed, the second (opening archive) should fail
        mock_open.side_effect = [
            unittest.mock.mock_open(read_data="Error prone content.\n").return_value, # For reading source
            MagicMock(side_effect=IOError("Disk full error!")) # For writing archive
        ]

        success = archive_logs(self.source_dir, self.archive_dir)
        self.assertFalse(success)

        # Check that no archive file was left behind (cleanup)
        self.assertEqual(len(os.listdir(self.archive_dir)), 0)
        # Original file should still exist as archiving failed before deletion step
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "error_log.log")))

    @patch('src.archiver.datetime')
    def test_archive_with_mixed_files_and_deletion(self, mock_datetime):
        # Mock rationale: Ensure deterministic timestamp for archive filename.
        mock_datetime.now.return_value = datetime(2023, 10, 27, 14, 0, 0)

        # Create dummy files
        with open(os.path.join(self.source_dir, "important.log"), "w") as f:
            f.write("Important log entry.\n")
        with open(os.path.join(self.source_dir, "temp.txt"), "w") as f:
            f.write("Temporary data.\n")
        with open(os.path.join(self.source_dir, "config.ini"), "w") as f: # Should be ignored
            f.write("[settings]\nkey=value\n")

        success = archive_logs(self.source_dir, self.archive_dir, delete_originals=True)
        self.assertTrue(success)

        # Check archive content
        expected_archive_filename = "chronicle_archive_2023-10-27_14-00-00.log"
        archive_filepath = os.path.join(self.archive_dir, expected_archive_filename)
        self.assertTrue(os.path.exists(archive_filepath))
        with open(archive_filepath, "r") as f:
            content = f.read()
            self.assertIn("Important log entry.", content)
            self.assertIn("Temporary data.", content)
            self.assertNotIn("config.ini", content)

        # Check deletion: only .log and .txt should be gone
        self.assertFalse(os.path.exists(os.path.join(self.source_dir, "important.log")))
        self.assertFalse(os.path.exists(os.path.join(self.source_dir, "temp.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "config.ini")))

if __name__ == "__main__":
    unittest.main()
