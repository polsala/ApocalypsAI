import unittest
from unittest.mock import patch, mock_open, MagicMock
import datetime
import os

# Import the functions to be tested
from src.chronicle_compiler import add_entry, compile_chronicle, view_log, LOGS_DIR, CHRONICLE_FILE

class TestChronicleCompiler(unittest.TestCase):

    @patch('os.makedirs')
    @patch('datetime.datetime')
    @patch('builtins.open', new_callable=mock_open)
    def test_add_entry(self, mock_file_open, mock_dt, mock_makedirs):
        # Mock rationale: Simulate file writing without touching the filesystem.
        # Mock rationale: Fix the current date and time for deterministic timestamps.
        # Mock rationale: Prevent actual directory creation during tests.

        mock_dt.now.return_value = datetime.datetime(2023, 10, 26, 14, 30, 0)
        mock_dt.date.today.return_value = datetime.date(2023, 10, 26)
        mock_dt.strptime = datetime.datetime.strptime # Keep original strptime for internal use if any

        entry_text = "Found a shiny bottlecap. Potential currency?"
        add_entry(entry_text)

        # Assert os.makedirs was called correctly
        mock_makedirs.assert_called_once_with(LOGS_DIR, exist_ok=True)

        # Assert open was called with the correct path and mode
        expected_log_filepath = os.path.join(LOGS_DIR, "2023-10-26.log")
        mock_file_open.assert_called_once_with(expected_log_filepath, "a", encoding="utf-8")

        # Assert the content written to the file
        mock_file_open().write.assert_called_once_with("[14:30:00] Found a shiny bottlecap. Potential currency?\n")

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    def test_compile_chronicle_success(self, mock_file_open, mock_isfile, mock_listdir, mock_exists):
        # Mock rationale: Simulate file system checks without actual files.
        # Mock rationale: Provide a list of 'existing' log files.
        # Mock rationale: Simulate file reading and writing without touching the filesystem.

        mock_exists.side_effect = lambda path: path == LOGS_DIR or path == CHRONICLE_FILE
        mock_listdir.return_value = ['2023-10-25.log', '2023-10-26.log']
        mock_isfile.return_value = True

        # Configure mock_open to return different content for different files
        mock_file_handle_25 = MagicMock()
        mock_file_handle_25.read.return_value = "[10:00:00] Day 1 entry.\n[11:00:00] Another Day 1 entry.\n"
        mock_file_handle_26 = MagicMock()
        mock_file_handle_26.read.return_value = "[12:00:00] Day 2 entry.\n"

        # Use a dictionary to map file paths to mock file handles
        file_contents = {
            os.path.join(LOGS_DIR, '2023-10-25.log'): mock_file_handle_25,
            os.path.join(LOGS_DIR, '2023-10-26.log'): mock_file_handle_26,
        }

        def open_side_effect(file_path, mode, encoding):
            if mode == 'r':
                return file_contents[file_path]
            elif mode == 'w':
                return mock_file_open.return_value # Return the mock_open's file handle for writing
            raise ValueError("Unexpected mode")

        mock_file_open.side_effect = open_side_effect

        compile_chronicle()

        # Assert that the chronicle file was opened for writing
        mock_file_open.assert_any_call(CHRONICLE_FILE, "w", encoding="utf-8")

        # Assert the content written to the chronicle file
        expected_chronicle_content = (
            "# Chronicle of Chaos\n\n"
            "## 2023-10-25\n\n"
            "[10:00:00] Day 1 entry.\n[11:00:00] Another Day 1 entry.\n\n\n"
            "## 2023-10-26\n\n"
            "[12:00:00] Day 2 entry.\n\n\n"
        )
        mock_file_open.return_value.write.assert_called_once_with(expected_chronicle_content)

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    def test_compile_chronicle_no_logs_dir(self, mock_file_open, mock_isfile, mock_listdir, mock_exists):
        # Mock rationale: Simulate the absence of the logs directory.
        mock_exists.return_value = False
        
        with patch('builtins.print') as mock_print:
            compile_chronicle()
            mock_print.assert_called_once_with(f"No '{LOGS_DIR}' directory found. Nothing to compile.")
        mock_file_open.assert_not_called()

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    def test_compile_chronicle_no_log_files(self, mock_file_open, mock_isfile, mock_listdir, mock_exists):
        # Mock rationale: Simulate an empty logs directory.
        mock_exists.return_value = True # LOGS_DIR exists
        mock_listdir.return_value = ['not_a_log.txt'] # No .log files
        mock_isfile.return_value = True

        with patch('builtins.print') as mock_print:
            compile_chronicle()
            mock_print.assert_called_once_with(f"No log files found in '{LOGS_DIR}'. Nothing to compile.")
        mock_file_open.assert_not_called()

    @patch('os.path.exists')
    @patch('datetime.date')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_log_daily_success(self, mock_file_open, mock_date, mock_exists):
        # Mock rationale: Simulate file existence and content for reading.
        # Mock rationale: Fix the current date for deterministic log file path.

        mock_date.today.return_value = datetime.date(2023, 10, 26)
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = "[14:30:00] Today's entry.\n"

        with patch('builtins.print') as mock_print:
            view_log("daily")
            mock_print.assert_any_call("\n--- Daily Log (2023-10-26) ---\n")
            mock_print.assert_any_call("[14:30:00] Today's entry.\n")
            mock_file_open.assert_called_once_with(os.path.join(LOGS_DIR, "2023-10-26.log"), "r", encoding="utf-8")

    @patch('os.path.exists')
    @patch('datetime.date')
    def test_view_log_daily_no_file(self, mock_date, mock_exists):
        # Mock rationale: Simulate the absence of today's log file.
        mock_date.today.return_value = datetime.date(2023, 10, 26)
        mock_exists.return_value = False

        with patch('builtins.print') as mock_print:
            view_log("daily")
            mock_print.assert_called_once_with("No log entries for today (2023-10-26).")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_view_log_chronicle_success(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate file existence and content for reading.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = "# Chronicle of Chaos\n## 2023-10-25\nEntry 1\n"

        with patch('builtins.print') as mock_print:
            view_log("chronicle")
            mock_print.assert_any_call("\n--- Compiled Chronicle ---\n")
            mock_print.assert_any_call("# Chronicle of Chaos\n## 2023-10-25\nEntry 1\n")
            mock_file_open.assert_called_once_with(CHRONICLE_FILE, "r", encoding="utf-8")

    @patch('os.path.exists')
    def test_view_log_chronicle_no_file(self, mock_exists):
        # Mock rationale: Simulate the absence of the compiled chronicle file.
        mock_exists.return_value = False

        with patch('builtins.print') as mock_print:
            view_log("chronicle")
            mock_print.assert_called_once_with("No compiled chronicle found. Run 'compile' first.")

    def test_view_log_invalid_type(self):
        # Mock rationale: Test input validation without file system interaction.
        with patch('builtins.print') as mock_print:
            view_log("invalid_type")
            mock_print.assert_called_once_with("Invalid view type. Use 'daily' or 'chronicle'.")

if __name__ == '__main__':
    unittest.main()
