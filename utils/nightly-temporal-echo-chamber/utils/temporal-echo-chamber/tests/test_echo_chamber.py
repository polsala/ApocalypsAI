import unittest
import os
import zipfile
import datetime
from unittest.mock import patch, MagicMock, mock_open
import shutil # For cleanup in actual test runs if needed, but mostly mocked

# Import the functions to be tested
from src.echo_chamber import create_echo, list_echoes, retrieve_echo, _get_timestamp

class TestTemporalEchoChamber(unittest.TestCase):

    def setUp(self):
        # Ensure a clean state for tests that might interact with the filesystem
        self.test_output_dir = "test_echoes"
        self.test_extract_dir = "test_extracted"
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
        if os.path.exists(self.test_extract_dir):
            shutil.rmtree(self.test_extract_dir)
        os.makedirs(self.test_output_dir, exist_ok=True)

    def tearDown(self):
        # Clean up after tests
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
        if os.path.exists(self.test_extract_dir):
            shutil.rmtree(self.test_extract_dir)

    @patch('src.echo_chamber.datetime')
    @patch('src.echo_chamber.os.path.exists')
    @patch('src.echo_chamber.os.makedirs')
    @patch('src.echo_chamber.os.path.isfile')
    @patch('src.echo_chamber.os.path.isdir')
    @patch('src.echo_chamber.zipfile.ZipFile')
    def test_create_echo_file_with_message(self, mock_zipfile, mock_isdir, mock_isfile, mock_makedirs, mock_exists, mock_datetime):
        # Mock rationale:
        # - datetime: To ensure deterministic timestamps for archive names.
        # - os.path.exists: To simulate the existence of the source file.
        # - os.makedirs: To prevent actual directory creation.
        # - os.path.isfile/isdir: To control whether the source is treated as a file or directory.
        # - zipfile.ZipFile: To mock the actual zip archive creation and content writing.

        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 0, 0)
        mock_exists.return_value = True # Source file exists
        mock_isfile.return_value = True # Source is a file
        mock_isdir.return_value = False # Source is not a directory

        mock_zip_instance = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

        source_path = "my_script.py"
        output_dir = "test_echoes"
        message = "Initial version."
        expected_archive_name = os.path.join(output_dir, "echo-20231027-100000-my_script.py.zip")

        create_echo(source_path, output_dir, message)

        mock_exists.assert_called_with(source_path)
        mock_makedirs.assert_called_with(output_dir, exist_ok=True)
        mock_zipfile.assert_called_with(expected_archive_name, 'w', zipfile.ZIP_DEFLATED)
        mock_zip_instance.write.assert_any_call(source_path, os.path.basename(source_path))
        mock_zip_instance.writestr.assert_called_with('message.txt', message)

    @patch('src.echo_chamber.datetime')
    @patch('src.echo_chamber.os.path.exists')
    @patch('src.echo_chamber.os.makedirs')
    @patch('src.echo_chamber.os.path.isfile')
    @patch('src.echo_chamber.os.path.isdir')
    @patch('src.echo_chamber.os.walk')
    @patch('src.echo_chamber.zipfile.ZipFile')
    def test_create_echo_directory_without_message(self, mock_zipfile, mock_walk, mock_isdir, mock_isfile, mock_makedirs, mock_exists, mock_datetime):
        # Mock rationale:
        # - os.walk: To simulate iterating through a directory structure.

        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 27, 11, 0, 0)
        mock_exists.return_value = True # Source directory exists
        mock_isfile.return_value = False # Source is not a file
        mock_isdir.return_value = True # Source is a directory

        mock_walk.return_value = [
            ("my_project", [], ["file1.txt", "file2.py"]),
            ("my_project/sub_dir", [], ["sub_file.md"])
        ]

        mock_zip_instance = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

        source_path = "my_project"
        output_dir = "test_echoes"
        expected_archive_name = os.path.join(output_dir, "echo-20231027-110000-my_project.zip")

        create_echo(source_path, output_dir)

        mock_zipfile.assert_called_with(expected_archive_name, 'w', zipfile.ZIP_DEFLATED)
        mock_zip_instance.write.assert_any_call(os.path.join("my_project", "file1.txt"), "file1.txt")
        mock_zip_instance.write.assert_any_call(os.path.join("my_project", "file2.py"), "file2.py")
        mock_zip_instance.write.assert_any_call(os.path.join("my_project/sub_dir", "sub_file.md"), os.path.join("sub_dir", "sub_file.md"))
        mock_zip_instance.writestr.assert_not_called() # No message provided

    @patch('src.echo_chamber.os.path.exists')
    @patch('src.echo_chamber.os.listdir')
    def test_list_echoes_found(self, mock_listdir, mock_exists):
        # Mock rationale:
        # - os.path.exists: To simulate the existence of the echoes directory.
        # - os.listdir: To simulate files present in the directory.

        mock_exists.return_value = True
        mock_listdir.return_value = [
            "echo-20231027-100000-script.py.zip",
            "not_an_echo.txt",
            "echo-20231027-110000-project.zip"
        ]

        with patch('builtins.print') as mock_print:
            list_echoes(self.test_output_dir)
            mock_print.assert_any_call(f"Echoes in '{self.test_output_dir}':")
            mock_print.assert_any_call("- echo-20231027-100000-script.py.zip")
            mock_print.assert_any_call("- echo-20231027-110000-project.zip")

    @patch('src.echo_chamber.os.path.exists')
    @patch('src.echo_chamber.os.listdir')
    def test_list_echoes_no_dir(self, mock_listdir, mock_exists):
        mock_exists.return_value = False
        with patch('builtins.print') as mock_print:
            list_echoes(self.test_output_dir)
            mock_print.assert_called_with(f"No echoes directory found at '{self.test_output_dir}'.")
        mock_listdir.assert_not_called()

    @patch('src.echo_chamber.os.path.exists')
    @patch('src.echo_chamber.os.listdir')
    def test_list_echoes_empty_dir(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ["not_an_echo.txt"]
        with patch('builtins.print') as mock_print:
            list_echoes(self.test_output_dir)
            mock_print.assert_called_with(f"No echoes found in '{self.test_output_dir}'.")

    @patch('src.echo_chamber.os.path.exists')
    @patch('src.echo_chamber.zipfile.is_zipfile')
    @patch('src.echo_chamber.os.makedirs')
    @patch('src.echo_chamber.zipfile.ZipFile')
    def test_retrieve_echo_success(self, mock_zipfile, mock_makedirs, mock_is_zipfile, mock_exists):
        # Mock rationale:
        # - zipfile.is_zipfile: To confirm the file is a valid zip.
        # - zipfile.ZipFile: To mock the extraction process.

        mock_exists.return_value = True
        mock_is_zipfile.return_value = True

        mock_zip_instance = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

        echo_path = "test_echoes/echo-20231027-100000-script.py.zip"
        expected_extract_dir = "echo-20231027-100000-script.py" # Default behavior

        with patch('builtins.print') as mock_print:
            retrieve_echo(echo_path)
            mock_exists.assert_called_with(echo_path)
            mock_is_zipfile.assert_called_with(echo_path)
            mock_makedirs.assert_called_with(expected_extract_dir, exist_ok=True)
            mock_zipfile.assert_called_with(echo_path, 'r')
            mock_zip_instance.extractall.assert_called_with(expected_extract_dir)
            mock_print.assert_any_call(f"Retrieving echo from '{echo_path}' to '{expected_extract_dir}'...")
            mock_print.assert_any_call(f"Echo retrieved successfully to '{expected_extract_dir}'.")

    @patch('src.echo_chamber.os.path.exists')
    @patch('src.echo_chamber.zipfile.is_zipfile')
    def test_retrieve_echo_not_found(self, mock_is_zipfile, mock_exists):
        mock_exists.return_value = False
        with patch('builtins.print') as mock_print:
            retrieve_echo("non_existent.zip")
            mock_print.assert_called_with("Error: Echo archive 'non_existent.zip' not found.")
        mock_is_zipfile.assert_not_called()

    @patch('src.echo_chamber.os.path.exists')
    @patch('src.echo_chamber.zipfile.is_zipfile')
    def test_retrieve_echo_not_zip(self, mock_is_zipfile, mock_exists):
        mock_exists.return_value = True
        mock_is_zipfile.return_value = False
        with patch('builtins.print') as mock_print:
            retrieve_echo("not_a_zip.txt")
            mock_print.assert_called_with("Error: 'not_a_zip.txt' is not a valid zip file.")

    @patch('src.echo_chamber.datetime')
    def test_get_timestamp(self, mock_datetime):
        # Mock rationale:
        # - datetime: To ensure deterministic output for the timestamp.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 1, 1, 12, 30, 45)
        self.assertEqual(_get_timestamp(), "20230101-123045")

if __name__ == '__main__':
    unittest.main()
