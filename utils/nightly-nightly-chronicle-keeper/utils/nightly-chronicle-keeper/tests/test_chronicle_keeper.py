import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timezone

# Add the src directory to the path to allow importing chronicle_keeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import chronicle_keeper

class TestChronicleKeeper(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture prints
    def test_empty_input_directory(self, mock_stdout, mock_file_open, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Simulate an empty directory to test the no-files-found scenario.
        mock_isdir.return_value = True
        mock_listdir.return_value = []
        mock_isfile.return_value = False # No files exist

        chronicle_keeper.create_chronicle("empty_dir", "output.md")

        mock_file_open.assert_not_called()
        self.assertIn("No markdown files found", mock_stdout.write.call_args[0][0])

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_non_existent_input_directory(self, mock_stdout, mock_file_open, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Simulate a non-existent directory to test error handling.
        mock_isdir.return_value = False

        chronicle_keeper.create_chronicle("non_existent_dir", "output.md")

        mock_file_open.assert_not_called()
        self.assertIn("Error: Input directory 'non_existent_dir' does not exist.", mock_stdout.write.call_args[0][0])

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_mixed_files_and_chronological_order(self, mock_stdout, mock_file_open, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Simulate a directory with various files, some markdown, some not,
        # and with different date sources (filename vs. modification time) to test sorting and filtering.
        mock_isdir.return_value = True
        mock_listdir.return_value = [
            "2023-10-26-log.md",
            "report-2023-10-25.md",
            "image.png",
            "notes.txt",
            "misc-entry.md", # Will use modification time
            "another-log-2023-10-27.md"
        ]

        # Mock os.path.isfile for all listed files
        def mock_isfile_side_effect(path):
            return os.path.basename(path) in mock_listdir.return_value
        mock_isfile.side_effect = mock_isfile_side_effect

        # Mock modification times for files without explicit dates in name
        # Using UTC timestamps for consistency
        mod_time_misc_entry = datetime(2023, 10, 28, 10, 0, 0, tzinfo=timezone.utc).timestamp()
        mod_time_other_file = datetime(2023, 10, 24, 10, 0, 0, tzinfo=timezone.utc).timestamp()

        def mock_getmtime_side_effect(path):
            filename = os.path.basename(path)
            if filename == "misc-entry.md":
                return mod_time_misc_entry
            elif filename == "report-2023-10-25.md": # Ensure files with dates in name don't use mod time
                return mod_time_other_file # This should be ignored by get_file_date
            return datetime(2023, 1, 1, tzinfo=timezone.utc).timestamp() # Default for others, should be overridden by filename date

        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Mock file content
        file_contents = {
            "2023-10-26-log.md": "Content for Oct 26.",
            "report-2023-10-25.md": "Report for Oct 25.",
            "misc-entry.md": "Miscellaneous thoughts.",
            "another-log-2023-10-27.md": "Another log for Oct 27."
        }

        # Configure mock_open to return specific content for each file
        mock_file_handle = mock_file_open.return_value
        mock_file_handle.__enter__.return_value.read.side_effect = lambda: file_contents.pop(
            os.path.basename(mock_file_open.call_args[0][0])
        )

        chronicle_keeper.create_chronicle("test_dir", "output.md")

        # Verify output file was opened for writing
        mock_file_open.assert_called_with("output.md", 'w', encoding='utf-8')

        # Verify the written content and order
        expected_output = [
            "# ApocalypsAI Chronicle\n\n",
            "## Chronicle Entry: 2023-10-25\n",
            "Report for Oct 25.\n\n",
            "## Chronicle Entry: 2023-10-26\n",
            "Content for Oct 26.\n\n",
            "## Chronicle Entry: 2023-10-27\n",
            "Another log for Oct 27.\n\n",
            "## Chronicle Entry: 2023-10-28 (modified)\n", # This is from misc-entry.md
            "Miscellaneous thoughts.\n\n"
        ]

        # Get all calls to write and join them
        written_content = "".join([call.args[0] for call in mock_file_handle.write.call_args_list])
        self.assertEqual(written_content, "".join(expected_output))

        # Verify print statements
        self.assertIn("Creating chronicle from 4 markdown files...", mock_stdout.write.call_args_list[0][0][0])
        self.assertIn("Chronicle successfully created at 'output.md'.", mock_stdout.write.call_args[-1][0])

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open) # This mocks builtins.open
    @patch('sys.stdout', new_callable=MagicMock)
    def test_file_read_error_handling(self, mock_stdout, mock_open_func, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Simulate a scenario where one markdown file cannot be read
        # to ensure the utility handles the error gracefully and continues processing others.
        mock_isdir.return_value = True
        mock_listdir.return_value = [
            "2023-10-26-good.md",
            "2023-10-25-bad.md",
        ]

        def mock_isfile_side_effect(path):
            return os.path.basename(path) in mock_listdir.return_value
        mock_isfile.side_effect = mock_isfile_side_effect

        mock_getmtime.return_value = datetime(2023, 1, 1, tzinfo=timezone.utc).timestamp()

        # Create mock file handles for input files
        mock_bad_file_handle = MagicMock()
        mock_bad_file_handle.__enter__.side_effect = IOError("Permission denied") # Error on __enter__
        mock_good_file_handle = mock_open(read_data="Good content.").return_value

        # Define a side effect for the patched `builtins.open`
        def open_side_effect(file_path, mode, encoding):
            if file_path == "output.md":
                # This is the output file, return the main mock_open's return_value
                return mock_open_func.return_value
            elif "2023-10-25-bad.md" in file_path:
                # This is the bad input file, return its specific mock handle
                return mock_bad_file_handle
            elif "2023-10-26-good.md" in file_path:
                # This is the good input file, return its specific mock handle
                return mock_good_file_handle
            return mock_open()() # Fallback for any other unexpected open

        mock_open_func.side_effect = open_side_effect

        chronicle_keeper.create_chronicle("test_dir", "output.md")

        # Verify output file was opened for writing
        # The first call to mock_open_func is for the output file
        self.assertEqual(mock_open_func.call_args_list[0].args[0], "output.md")
        self.assertEqual(mock_open_func.call_args_list[0].args[1], 'w')

        # Verify the written content
        expected_output = [
            "# ApocalypsAI Chronicle\n\n",
            "## Chronicle Entry: 2023-10-25\n",
            "**Error reading file '2023-10-25-bad.md': Permission denied**\n\n",
            "## Chronicle Entry: 2023-10-26\n",
            "Good content.\n\n"
        ]

        # Get all calls to write on the output file handle (which is mock_open_func.return_value)
        written_content = "".join([call.args[0] for call in mock_open_func.return_value.write.call_args_list])
        self.assertEqual(written_content, "".join(expected_output))

        # Verify print statements
        self.assertIn("Error reading file '2023-10-25-bad.md'", written_content)
        self.assertIn("Chronicle successfully created at 'output.md'.", mock_stdout.write.call_args[-1][0])


    def test_extract_date_from_filename(self):
        # Mock rationale: Test the date extraction logic in isolation.
        self.assertEqual(chronicle_keeper.extract_date_from_filename("2023-01-15-report.md"), datetime(2023, 1, 15))
        self.assertEqual(chronicle_keeper.extract_date_from_filename("report-2024-02-29.md"), datetime(2024, 2, 29))
        self.assertIsNone(chronicle_keeper.extract_date_from_filename("no-date-file.md"))
        self.assertIsNone(chronicle_keeper.extract_date_from_filename("invalid-date-2023-13-01.md"))
        self.assertEqual(chronicle_keeper.extract_date_from_filename("prefix-2023-04-05-suffix.md"), datetime(2023, 4, 5))
        self.assertEqual(chronicle_keeper.extract_date_from_filename("2023-04-05.md"), datetime(2023, 4, 5))
        self.assertEqual(chronicle_keeper.extract_date_from_filename("file_2023-04-05_log.md"), datetime(2023, 4, 5))

    @patch('os.path.getmtime')
    def test_get_file_date_filename_priority(self, mock_getmtime):
        # Mock rationale: Test that filename date takes precedence over modification time.
        mock_getmtime.return_value = datetime(2022, 1, 1, tzinfo=timezone.utc).timestamp() # A much older date

        date_obj, date_str = chronicle_keeper.get_file_date("/path/to/2023-01-15-report.md")
        self.assertEqual(date_obj, datetime(2023, 1, 15))
        self.assertEqual(date_str, "2023-01-15")
        mock_getmtime.assert_not_called() # Should not be called if date is in filename

    @patch('os.path.getmtime')
    def test_get_file_date_modification_fallback(self, mock_getmtime):
        # Mock rationale: Test that modification time is used when no date is in the filename.
        mod_timestamp = datetime(2023, 5, 10, 14, 30, 0, tzinfo=timezone.utc).timestamp()
        mock_getmtime.return_value = mod_timestamp

        date_obj, date_str = chronicle_keeper.get_file_date("/path/to/no-date-file.md")
        self.assertEqual(date_obj, datetime(2023, 5, 10, 14, 30, 0))
        self.assertEqual(date_str, "2023-05-10 (modified)")
        mock_getmtime.assert_called_once()


if __name__ == '__main__':
    unittest.main()
