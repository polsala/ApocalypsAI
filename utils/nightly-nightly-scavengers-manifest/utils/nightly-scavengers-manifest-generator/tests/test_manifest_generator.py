import unittest
from unittest.mock import patch, mock_open
import os
from datetime import datetime
import sys

# Add the src directory to the path to allow importing manifest_generator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from manifest_generator import generate_manifest, format_size
sys.path.pop(0)

class TestManifestGenerator(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.join', side_effect=os.path.join) # Mock rationale: os.path.join is deterministic and pure, but mocking it allows control over paths without actual filesystem interaction. Using side_effect=os.path.join ensures it behaves normally for path construction within the mock environment.
    @patch('builtins.print') # Mock rationale: Capture print output for verification without polluting stdout during tests.
    @patch('datetime.datetime') # Mock rationale: Ensure deterministic 'Generated On' timestamp for consistent test results.
    def test_empty_directory(self, mock_datetime, mock_print, mock_join, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        mock_isdir.return_value = True # Mock rationale: Simulate that the target directory exists.
        mock_walk.return_value = [] # Mock rationale: Simulate an empty directory with no files or subdirectories.
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 30, 0) # Mock rationale: Fix the current time for deterministic output.

        generate_manifest('/test/empty_dir')

        expected_output_part = [
            "Scavenger's Manifest for: /test/empty_dir",
            "Generated On: 2023-10-27 10:30:00",
            "\nTotal Files Scanned: 0",
            "Total Size: 0 Bytes",
            "\n--- File Type Summary ---",
            "--- End Manifest ---"
        ]
        # Check if the relevant parts of the output are present
        called_args = [call_arg[0] for call_arg in mock_print.call_args_list]
        for line in expected_output_part:
            self.assertIn(line, called_args)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.join', side_effect=os.path.join) # Mock rationale: See above.
    @patch('builtins.print') # Mock rationale: See above.
    @patch('datetime.datetime') # Mock rationale: See above.
    def test_directory_with_files(self, mock_datetime, mock_print, mock_join, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        mock_isdir.return_value = True # Mock rationale: Simulate that the target directory exists.
        mock_walk.return_value = [
            ('/test/data', [], ['file1.txt', 'image.jpg']),
            ('/test/data/sub', [], ['log.log', 'report.pdf'])
        ] # Mock rationale: Simulate a directory structure with files in root and a subdirectory.
        mock_getsize.side_effect = {
            '/test/data/file1.txt': 1024,
            '/test/data/image.jpg': 512000,
            '/test/data/sub/log.log': 2048,
            '/test/data/sub/report.pdf': 1024000
        }.get # Mock rationale: Provide specific sizes for each mocked file path.
        mock_getmtime.side_effect = {
            '/test/data/file1.txt': datetime(2023, 1, 1, 10, 0, 0).timestamp(),
            '/test/data/image.jpg': datetime(2023, 2, 15, 11, 30, 0).timestamp(),
            '/test/data/sub/log.log': datetime(2023, 3, 10, 12, 0, 0).timestamp(),
            '/test/data/sub/report.pdf': datetime(2023, 4, 20, 13, 45, 0).timestamp()
        }.get # Mock rationale: Provide specific modification times for each mocked file path.
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 30, 0) # Mock rationale: Fix the current time for deterministic output.

        generate_manifest('/test/data')

        expected_output_part = [
            "Scavenger's Manifest for: /test/data",
            "Generated On: 2023-10-27 10:30:00",
            "\nTotal Files Scanned: 4",
            "Total Size: 1.47 MB", # 1024 + 512000 + 2048 + 1024000 = 1539072 bytes = 1.4677... MB, rounded to 1.47 MB
            "\n--- File Type Summary ---",
            ".jpg:",
            "  Count: 1",
            "  Total Size: 500.0 KB",
            "  Last Modified (oldest): 2023-02-15 11:30:00",
            "  Last Modified (newest): 2023-02-15 11:30:00",
            ".log:",
            "  Count: 1",
            "  Total Size: 2.0 KB",
            "  Last Modified (oldest): 2023-03-10 12:00:00",
            "  Last Modified (newest): 2023-03-10 12:00:00",
            ".pdf:",
            "  Count: 1",
            "  Total Size: 1000.0 KB",
            "  Last Modified (oldest): 2023-04-20 13:45:00",
            "  Last Modified (newest): 2023-04-20 13:45:00",
            ".txt:",
            "  Count: 1",
            "  Total Size: 1.0 KB",
            "  Last Modified (oldest): 2023-01-01 10:00:00",
            "  Last Modified (newest): 2023-01-01 10:00:00",
            "--- End Manifest ---"
        ]
        called_args = [call_arg[0] for call_arg in mock_print.call_args_list]
        for line in expected_output_part:
            self.assertIn(line, called_args)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.join', side_effect=os.path.join) # Mock rationale: See above.
    @patch('builtins.print') # Mock rationale: See above.
    @patch('datetime.datetime') # Mock rationale: See above.
    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Intercept file open calls to prevent actual file system writes and capture the content written.
    def test_output_to_file(self, mock_open_file, mock_datetime, mock_print, mock_join, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        mock_isdir.return_value = True # Mock rationale: Simulate that the target directory exists.
        mock_walk.return_value = [
            ('/test/data', [], ['doc.txt'])
        ] # Mock rationale: Simulate a directory with a single file.
        mock_getsize.return_value = 100 # Mock rationale: Provide a fixed size for the mocked file.
        mock_getmtime.return_value = datetime(2023, 5, 1, 9, 0, 0).timestamp() # Mock rationale: Provide a fixed modification time for the mocked file.
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 30, 0) # Mock rationale: Fix the current time for deterministic output.

        output_filename = 'manifest.txt'
        generate_manifest('/test/data', output_filename)

        mock_open_file.assert_called_once_with(output_filename, 'w') # Mock rationale: Verify that the output file was opened for writing.
        handle = mock_open_file()
        handle.write.assert_called_once() # Mock rationale: Verify that content was written to the file handle.

        written_content = handle.write.call_args[0][0]
        self.assertIn("Scavenger's Manifest for: /test/data", written_content)
        self.assertIn("Total Files Scanned: 1", written_content)
        self.assertIn(".txt:", written_content)
        self.assertIn("Manifest successfully written to 'manifest.txt'", mock_print.call_args[0][0]) # Mock rationale: Verify success message is printed.

    @patch('os.path.isdir')
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_directory_not_found(self, mock_print, mock_isdir):
        mock_isdir.return_value = False # Mock rationale: Simulate that the target directory does not exist.

        generate_manifest('/nonexistent/dir')

        mock_print.assert_called_once_with("Error: Directory not found at '/nonexistent/dir'") # Mock rationale: Verify error message is printed.

    def test_format_size(self):
        self.assertEqual(format_size(0), "0 Bytes")
        self.assertEqual(format_size(500), "500 Bytes")
        self.assertEqual(format_size(1024), "1.0 KB")
        self.assertEqual(format_size(1536), "1.5 KB")
        self.assertEqual(format_size(1024 * 1024), "1.0 MB")
        self.assertEqual(format_size(1024 * 1024 * 1.5), "1.5 MB")
        self.assertEqual(format_size(1024 * 1024 * 1024), "1.0 GB")
        self.assertEqual(format_size(1024 * 1024 * 1024 * 1024 * 1.23), "1.23 TB")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.join', side_effect=os.path.join) # Mock rationale: See above.
    @patch('builtins.print') # Mock rationale: See above.
    @patch('datetime.datetime') # Mock rationale: See above.
    def test_file_access_error_handling(self, mock_datetime, mock_print, mock_join, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        mock_isdir.return_value = True # Mock rationale: Simulate that the target directory exists.
        mock_walk.return_value = [
            ('/test/data', [], ['accessible.txt', 'inaccessible.txt'])
        ] # Mock rationale: Simulate a directory with one accessible and one inaccessible file.
        mock_getsize.side_effect = {
            '/test/data/accessible.txt': 100,
            '/test/data/inaccessible.txt': OSError("Permission denied")
        }.get # Mock rationale: Simulate an OSError for one file, and a normal size for another.
        mock_getmtime.side_effect = {
            '/test/data/accessible.txt': datetime(2023, 1, 1, 10, 0, 0).timestamp(),
            '/test/data/inaccessible.txt': datetime(2023, 1, 1, 10, 0, 0).timestamp() # This won't be called if getsize fails first
        }.get # Mock rationale: Provide modification time for the accessible file.
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 30, 0) # Mock rationale: Fix the current time for deterministic output.

        generate_manifest('/test/data')

        # Check for the warning message about inaccessible file
        called_args = [call_arg[0] for call_arg in mock_print.call_args_list]
        self.assertIn("Warning: Could not access '/test/data/inaccessible.txt': Permission denied", called_args)

        # Ensure the accessible file is still counted
        expected_output_part = [
            "Total Files Scanned: 1",
            "Total Size: 100 Bytes",
            ".txt:",
            "  Count: 1",
            "  Total Size: 100 Bytes",
            "  Last Modified (oldest): 2023-01-01 10:00:00",
            "  Last Modified (newest): 2023-01-01 10:00:00"
        ]
        for line in expected_output_part:
            self.assertIn(line, called_args)


if __name__ == '__main__':
    unittest.main()
