import unittest
import os
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime

# Import the function to test
from src.archiver import create_archive

class TestArchiver(unittest.TestCase):

    @patch('src.archiver.datetime')
    @patch('src.archiver.os.makedirs')
    @patch('src.archiver.os.path.exists')
    @patch('src.archiver.os.path.isfile')
    @patch('src.archiver.os.path.isdir')
    @patch('src.archiver.shutil.copy2')
    @patch('src.archiver.shutil.copytree')
    def test_create_archive_files_and_dirs(self, mock_copytree, mock_copy2, mock_isdir, mock_isfile, mock_exists, mock_makedirs, mock_datetime):
        # Mock rationale: We don't want to actually create files/directories on the filesystem.
        # We mock os.makedirs, os.path.exists, os.path.isfile, os.path.isdir, shutil.copy2, and shutil.copytree
        # to simulate filesystem operations and verify they are called correctly.
        # datetime is mocked to ensure deterministic timestamp generation.

        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 30, 0)
        output_dir = "./test_archives"
        files_to_archive = ["README.md", "agents/"]

        # Mock exists for all paths
        mock_exists.side_effect = lambda path: path in ["README.md", "agents/"]

        # Mock isfile and isdir
        mock_isfile.side_effect = lambda path: path == "README.md"
        mock_isdir.side_effect = lambda path: path == "agents/"

        expected_archive_path = os.path.join(output_dir, "archive_20231027_103000")

        # Run the function
        result_path = create_archive(output_dir, files_to_archive)

        # Assertions
        mock_makedirs.assert_called_once_with(expected_archive_path, exist_ok=True)
        mock_copy2.assert_called_once_with("README.md", os.path.join(expected_archive_path, "README.md"))
        mock_copytree.assert_called_once_with("agents/", os.path.join(expected_archive_path, "agents/"), dirs_exist_ok=True)
        self.assertEqual(result_path, expected_archive_path)

    @patch('src.archiver.datetime')
    @patch('src.archiver.os.makedirs')
    @patch('src.archiver.os.path.exists')
    @patch('src.archiver.os.path.isfile')
    @patch('src.archiver.os.path.isdir')
    @patch('src.archiver.shutil.copy2')
    @patch('src.archiver.shutil.copytree')
    def test_create_archive_non_existent_item(self, mock_copytree, mock_copy2, mock_isdir, mock_isfile, mock_exists, mock_makedirs, mock_datetime):
        # Mock rationale: Test the behavior when an item to archive does not exist.
        # We mock os.path.exists to return False for the non-existent item.

        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 30, 0)
        output_dir = "./test_archives"
        files_to_archive = ["non_existent_file.txt"]

        mock_exists.return_value = False # Simulate file not existing

        expected_archive_path = os.path.join(output_dir, "archive_20231027_103000")

        # Run the function
        result_path = create_archive(output_dir, files_to_archive)

        # Assertions
        mock_makedirs.assert_called_once_with(expected_archive_path, exist_ok=True)
        mock_copy2.assert_not_called()
        mock_copytree.assert_not_called()
        self.assertEqual(result_path, expected_archive_path)

    @patch('src.archiver.datetime')
    @patch('src.archiver.os.makedirs')
    @patch('src.archiver.os.path.exists')
    @patch('src.archiver.os.path.isfile')
    @patch('src.archiver.os.path.isdir')
    @patch('src.archiver.shutil.copy2')
    @patch('src.archiver.shutil.copytree')
    def test_create_archive_empty_list(self, mock_copytree, mock_copy2, mock_isdir, mock_isfile, mock_exists, mock_makedirs, mock_datetime):
        # Mock rationale: Test the behavior when no files are specified for archiving.

        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 30, 0)
        output_dir = "./test_archives"
        files_to_archive = []

        expected_archive_path = os.path.join(output_dir, "archive_20231027_103000")

        # Run the function
        result_path = create_archive(output_dir, files_to_archive)

        # Assertions
        mock_makedirs.assert_called_once_with(expected_archive_path, exist_ok=True)
        mock_exists.assert_not_called() # No files to check existence for
        mock_copy2.assert_not_called()
        mock_copytree.assert_not_called()
        self.assertEqual(result_path, expected_archive_path)

    @patch('src.archiver.main') # Mock main to prevent argparse from exiting
    @patch('src.archiver.create_archive')
    @patch('sys.argv', ['archiver.py', '--output-dir', './test_output', '--files', 'file1.txt', 'dir1/'])
    def test_main_function_call(self, mock_create_archive, mock_main):
        # Mock rationale: Test that the main function correctly parses arguments and calls create_archive.
        # sys.argv is patched to simulate command-line arguments.
        # main is patched to prevent it from running its original code and potentially causing issues with argparse.

        from src.archiver import main # Re-import main after patching sys.argv

        main() # Call the main function

        mock_create_archive.assert_called_once_with('./test_output', ['file1.txt', 'dir1/'])

if __name__ == '__main__':
    unittest.main()
