import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

# Import the functions from the indexer script
from src.indexer import scan_directory, get_file_metadata, format_as_markdown, format_as_json, main

class TestIndexer(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.mock_now = datetime(2023, 10, 27, 10, 30, 0, tzinfo=timezone.utc)
        
        # Mock datetime.now for deterministic output
        # Mock rationale: Ensures that the "Scan Date" in the output is consistent across test runs,
        # preventing test failures due to changing timestamps.
        self.patch_datetime = patch('src.indexer.datetime')
        self.mock_datetime = self.patch_datetime.start()
        self.mock_datetime.now.return_value = self.mock_now
        self.mock_datetime.fromtimestamp = datetime.fromtimestamp # Keep original for file mtime
        self.mock_datetime.fromisoformat = datetime.fromisoformat # Keep original for parsing
        self.mock_datetime.strptime = datetime.strptime # Keep original for parsing
        self.mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime.datetime(...) calls

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)
        self.patch_datetime.stop()

    def _create_test_file(self, filename, content, mtime_timestamp):
        """Helper to create a file with specific content and modification time."""
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)
        os.utime(filepath, (mtime_timestamp, mtime_timestamp)) # Set access and modification times
        return filepath

    def test_scan_empty_directory(self):
        """Test scanning a directory with no files."""
        files_data = scan_directory(self.test_dir)
        self.assertEqual(len(files_data), 0)

    def test_scan_directory_with_files(self):
        """Test scanning a directory with multiple files."""
        file1_mtime = datetime(2023, 1, 15, 8, 0, 0).timestamp()
        file2_mtime = datetime(2023, 3, 20, 14, 15, 30).timestamp()

        self._create_test_file("document.txt", "hello world", file1_mtime)
        self._create_test_file("image.jpg", "binary data", file2_mtime)

        files_data = scan_directory(self.test_dir)
        self.assertEqual(len(files_data), 2)

        # Sort by name for deterministic comparison
        files_data.sort(key=lambda x: x['name'])

        self.assertEqual(files_data[0]['name'], "document.txt")
        self.assertEqual(files_data[0]['size_bytes'], 11)
        self.assertEqual(files_data[0]['last_modified'], "2023-01-15T08:00:00")

        self.assertEqual(files_data[1]['name'], "image.jpg")
        self.assertEqual(files_data[1]['size_bytes'], 11)
        self.assertEqual(files_data[1]['last_modified'], "2023-03-20T14:15:30")

    def test_scan_directory_with_subdirectories(self):
        """Test scanning a directory with files in subdirectories."""
        subdir_path = os.path.join(self.test_dir, "subdir")
        os.makedirs(subdir_path)

        file1_mtime = datetime(2023, 1, 15, 8, 0, 0).timestamp()
        file2_mtime = datetime(2023, 3, 20, 14, 15, 30).timestamp()

        self._create_test_file("document.txt", "root file", file1_mtime)
        self._create_test_file(os.path.join("subdir", "nested.log"), "nested content", file2_mtime)

        files_data = scan_directory(self.test_dir)
        self.assertEqual(len(files_data), 2)
        
        # Sort by name for deterministic comparison
        files_data.sort(key=lambda x: x['name'])

        self.assertEqual(files_data[0]['name'], "document.txt")
        self.assertEqual(files_data[1]['name'], "nested.log")

    def test_scan_non_existent_directory(self):
        """Test scanning a directory that does not exist."""
        with self.assertRaises(FileNotFoundError):
            scan_directory("/non/existent/path")

    def test_format_as_markdown(self):
        """Test Markdown output format."""
        files_data = [
            {
                "name": "document.txt",
                "size_bytes": 1024,
                "last_modified": "2023-01-15T08:00:00"
            },
            {
                "name": "image.jpg",
                "size_bytes": 51200,
                "last_modified": "2023-03-20T14:15:30"
            }
        ]
        markdown_output = format_as_markdown(self.test_dir, files_data)
        
        expected_output = f"""# Chronoscroll Archive Index - {self.test_dir}

**Scan Date:** 2023-10-27 10:30:00

## Files Found: 2

- **document.txt**
  - Size: 1024 bytes
  - Last Modified: 2023-01-15 08:00:00
- **image.jpg**
  - Size: 51200 bytes
  - Last Modified: 2023-03-20 14:15:30"""
        self.assertEqual(markdown_output, expected_output)

    def test_format_as_json(self):
        """Test JSON output format."""
        files_data = [
            {
                "name": "document.txt",
                "size_bytes": 1024,
                "last_modified": "2023-01-15T08:00:00"
            },
            {
                "name": "image.jpg",
                "size_bytes": 51200,
                "last_modified": "2023-03-20T14:15:30"
            }
        ]
        json_output = format_as_json(self.test_dir, files_data)
        
        expected_data = {
            "scan_date": "2023-10-27T10:30:00+00:00", # Mocked datetime is UTC
            "scanned_path": self.test_dir,
            "files_count": 2,
            "files": [
                {
                    "name": "document.txt",
                    "size_bytes": 1024,
                    "last_modified": "2023-01-15T08:00:00"
                },
                {
                    "name": "image.jpg",
                    "size_bytes": 51200,
                    "last_modified": "2023-03-20T14:15:30"
                }
            ]
        }
        self.assertEqual(json.loads(json_output), expected_data)

    @patch('builtins.print')
    @patch('src.indexer.scan_directory')
    @patch('src.indexer.format_as_markdown')
    @patch('src.indexer.format_as_json')
    def test_main_markdown_stdout(self, mock_format_json, mock_format_markdown, mock_scan_directory, mock_print):
        """Test main function with markdown output to stdout."""
        mock_scan_directory.return_value = []
        mock_format_markdown.return_value = "Mock Markdown Output"

        # Mock rationale: argparse.ArgumentParser.parse_args() reads from sys.argv.
        # Patching sys.argv directly is brittle. Instead, we mock the ArgumentParser
        # to return a MagicMock object with the desired attributes, simulating CLI args.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=self.test_dir,
            output_format="markdown",
            output_file=None
        )):
            main()
            mock_print.assert_called_once_with("Mock Markdown Output")
            mock_format_markdown.assert_called_once()
            mock_format_json.assert_not_called()

    @patch('builtins.print')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('src.indexer.scan_directory')
    @patch('src.indexer.format_as_json')
    def test_main_json_to_file(self, mock_format_json, mock_scan_directory, mock_open, mock_print):
        """Test main function with json output to a file."""
        mock_scan_directory.return_value = []
        mock_format_json.return_value = '{"test": "json"}'
        output_filename = "output.json"

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=self.test_dir,
            output_format="json",
            output_file=output_filename
        )):
            main()
            mock_open.assert_called_once_with(output_filename, "w", encoding="utf-8")
            mock_open().write.assert_called_once_with('{"test": "json"}')
            mock_print.assert_called_once_with(f"Index successfully written to {output_filename}")
            mock_format_json.assert_called_once()

    @patch('builtins.print')
    @patch('sys.exit')
    @patch('src.indexer.scan_directory', side_effect=FileNotFoundError("Test error"))
    def test_main_file_not_found_error(self, mock_scan_directory, mock_exit, mock_print):
        """Test main function handles FileNotFoundError."""
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path="/non/existent",
            output_format="markdown",
            output_file=None
        )):
            main()
            mock_print.assert_called_once_with("Error: Test error")
            mock_exit.assert_called_once_with(1)

    @patch('builtins.print')
    @patch('sys.exit')
    @patch('src.indexer.scan_directory', side_effect=Exception("Generic error"))
    def test_main_generic_error(self, mock_scan_directory, mock_exit, mock_print):
        """Test main function handles generic exceptions."""
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=self.test_dir,
            output_format="markdown",
            output_file=None
        )):
            main()
            mock_print.assert_called_once_with("An unexpected error occurred: Generic error")
            mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
