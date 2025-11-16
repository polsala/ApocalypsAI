import unittest
import os
import sys
import datetime
import zipfile
from unittest.mock import patch, MagicMock, mock_open

# Add the src directory to the Python path to allow importing echo_chamber
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import echo_chamber

class TestEchoChamber(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.makedirs')
    @patch('datetime.datetime')
    @patch('zipfile.ZipFile')
    @patch('os.walk')
    @patch('os.path.relpath')
    def test_create_archive_success(self, mock_relpath, mock_os_walk, mock_zipfile, mock_datetime, mock_makedirs, mock_isdir):
        # Mock rationale: Simulate a valid source directory existing.
        mock_isdir.return_value = True
        # Mock rationale: Prevent actual directory creation during test.
        mock_makedirs.return_value = None

        # Mock rationale: Control the timestamp for deterministic archive naming.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 14, 35, 1)
        mock_datetime.strftime.return_value = "20231027_143501"

        # Mock rationale: Simulate files within the source directory for zipping.
        source_dir = "/mock/source"
        output_dir = "/mock/output"
        archive_prefix = "test-snapshot"
        expected_archive_path = os.path.join(output_dir, f"{archive_prefix}_20231027_143501.zip")

        mock_os_walk.return_value = [
            (source_dir, [], ["file1.txt", "file2.log"]),
            (os.path.join(source_dir, "subdir"), [], ["nested.md"])
        ]

        # Mock rationale: Simulate relative paths for files within the archive.
        mock_relpath.side_effect = lambda path, start: path.replace(start + os.sep, '')

        # Mock rationale: Capture the ZipFile instance to check its calls.
        mock_zip_file_instance = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip_file_instance

        result_path = echo_chamber.create_archive(source_dir, output_dir, archive_prefix)

        mock_isdir.assert_called_once_with(source_dir)
        mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)
        mock_zipfile.assert_called_once_with(expected_archive_path, 'w', zipfile.ZIP_DEFLATED)
        
        # Assert that write was called for each file
        self.assertEqual(mock_zip_file_instance.write.call_count, 3)
        mock_zip_file_instance.write.assert_any_call(os.path.join(source_dir, "file1.txt"), "file1.txt")
        mock_zip_file_instance.write.assert_any_call(os.path.join(source_dir, "file2.log"), "file2.log")
        mock_zip_file_instance.write.assert_any_call(os.path.join(source_dir, "subdir", "nested.md"), os.path.join("subdir", "nested.md"))

        self.assertEqual(result_path, expected_archive_path)

    @patch('os.path.isdir')
    def test_create_archive_source_not_found(self, mock_isdir):
        # Mock rationale: Simulate the source directory not existing.
        mock_isdir.return_value = False

        source_dir = "/nonexistent/source"
        output_dir = "/mock/output"

        with self.assertRaisesRegex(FileNotFoundError, f"Source directory not found: {source_dir}"):
            echo_chamber.create_archive(source_dir, output_dir)
        
        mock_isdir.assert_called_once_with(source_dir)

    @patch('os.path.isdir', return_value=True)
    @patch('os.makedirs')
    @patch('datetime.datetime')
    @patch('zipfile.ZipFile')
    @patch('os.walk', return_value=[])
    def test_create_archive_io_error_on_zip(self, mock_os_walk, mock_zipfile, mock_datetime, mock_makedirs, mock_isdir):
        # Mock rationale: Simulate an IOError during zip file creation.
        mock_zipfile.side_effect = IOError("Disk full or permission denied")
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 14, 35, 1)
        mock_datetime.strftime.return_value = "20231027_143501"

        source_dir = "/mock/source"
        output_dir = "/mock/output"
        archive_prefix = "test-snapshot"
        expected_archive_path = os.path.join(output_dir, f"{archive_prefix}_20231027_143501.zip")

        with self.assertRaisesRegex(IOError, f"Failed to create archive '{expected_archive_path}': Disk full or permission denied"):
            echo_chamber.create_archive(source_dir, output_dir, archive_prefix)
        
        mock_zipfile.assert_called_once_with(expected_archive_path, 'w', zipfile.ZIP_DEFLATED)

    @patch('os.path.isdir', return_value=True)
    @patch('os.makedirs', side_effect=OSError("Permission denied"))
    def test_create_archive_io_error_on_makedirs(self, mock_makedirs, mock_isdir):
        # Mock rationale: Simulate an OSError when creating the output directory.
        source_dir = "/mock/source"
        output_dir = "/mock/output"

        with self.assertRaisesRegex(IOError, "Failed to create archive '.*': Permission denied"):
            echo_chamber.create_archive(source_dir, output_dir)
        
        mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('echo_chamber.create_archive')
    def test_main_success(self, mock_create_archive, mock_parse_args, mock_sys_exit, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments.
        mock_parse_args.return_value = MagicMock(
            source="/mock/source",
            output="/mock/output",
            prefix="test-prefix"
        )
        # Mock rationale: Simulate successful archive creation.
        mock_create_archive.return_value = "/mock/output/test-prefix_timestamp.zip"

        echo_chamber.main()

        mock_create_archive.assert_called_once_with("/mock/source", "/mock/output", "test-prefix")
        mock_stdout.write.assert_any_call("Successfully created archive: /mock/output/test-prefix_timestamp.zip\n")
        mock_sys_exit.assert_called_once_with(0)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('echo_chamber.create_archive', side_effect=FileNotFoundError("Source not found"))
    def test_main_file_not_found_error(self, mock_create_archive, mock_parse_args, mock_sys_exit, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments.
        mock_parse_args.return_value = MagicMock(
            source="/mock/source",
            output="/mock/output",
            prefix="test-prefix"
        )

        echo_chamber.main()

        mock_stderr.write.assert_any_call("Error: Source not found\n")
        mock_sys_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('echo_chamber.create_archive', side_effect=IOError("Permission denied"))
    def test_main_io_error(self, mock_create_archive, mock_parse_args, mock_sys_exit, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments.
        mock_parse_args.return_value = MagicMock(
            source="/mock/source",
            output="/mock/output",
            prefix="test-prefix"
        )

        echo_chamber.main()

        mock_stderr.write.assert_any_call("Error: Permission denied\n")
        mock_sys_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
