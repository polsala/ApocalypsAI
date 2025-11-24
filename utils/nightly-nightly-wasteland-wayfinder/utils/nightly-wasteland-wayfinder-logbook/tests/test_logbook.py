import unittest
from unittest.mock import patch, mock_open
import datetime
import os
import io
from src.logbook import add_entry, view_log, _ensure_log_header, DEFAULT_LOG_FILE, LOG_HEADER

class TestLogbook(unittest.TestCase):

    def setUp(self):
        # Mock datetime.datetime.now() to ensure deterministic timestamps
        self.mock_now = datetime.datetime(2023, 10, 27, 15, 30, 0)
        self.mock_strftime = self.mock_now.strftime("%Y-%m-%d %H:%M:%S")

    @patch('os.path.exists')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_ensure_log_header_creates_new_file(self, mock_file_open, mock_getsize, mock_exists):
        # Mock rationale: os.path.exists and os.path.getsize are mocked to simulate a non-existent or empty file.
        # builtins.open is mocked to capture file write operations without touching the filesystem.
        mock_exists.return_value = False
        mock_getsize.return_value = 0 # This won't be called if exists is False, but good practice.

        _ensure_log_header(DEFAULT_LOG_FILE)

        mock_exists.assert_called_once_with(DEFAULT_LOG_FILE)
        mock_file_open.assert_called_once_with(DEFAULT_LOG_FILE, 'w', encoding='utf-8')
        mock_file_open().write.assert_called_once_with(LOG_HEADER)

    @patch('os.path.exists')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_ensure_log_header_does_not_overwrite_existing_file(self, mock_file_open, mock_getsize, mock_exists):
        # Mock rationale: os.path.exists and os.path.getsize are mocked to simulate an existing, non-empty file.
        # builtins.open is mocked to ensure no write operations occur.
        mock_exists.return_value = True
        mock_getsize.return_value = 100 # Simulate existing content

        _ensure_log_header(DEFAULT_LOG_FILE)

        mock_exists.assert_called_once_with(DEFAULT_LOG_FILE)
        mock_getsize.assert_called_once_with(DEFAULT_LOG_FILE)
        mock_file_open.assert_not_called() # Should not open for writing

    @patch('datetime.datetime')
    @patch('os.path.exists')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_add_entry_appends_to_file(self, mock_print, mock_file_open, mock_getsize, mock_exists, mock_dt):
        # Mock rationale: datetime.datetime is mocked to control the timestamp.
        # os.path.exists and os.path.getsize are mocked to simulate an existing file with header.
        # builtins.open is mocked to capture file write operations.
        # builtins.print is mocked to prevent actual console output during test.
        mock_dt.now.return_value = self.mock_now
        mock_exists.return_value = True
        mock_getsize.return_value = len(LOG_HEADER) # Simulate file with only header

        test_entry = "Found a shiny bottlecap."
        expected_entry_content = f"## {self.mock_strftime}\n{test_entry}\n\n"

        add_entry(DEFAULT_LOG_FILE, test_entry)

        # Check that _ensure_log_header was called and didn't write header again
        mock_exists.assert_called_with(DEFAULT_LOG_FILE)
        mock_getsize.assert_called_with(DEFAULT_LOG_FILE)
        
        # Check that open was called in append mode for the entry
        mock_file_open.assert_called_with(DEFAULT_LOG_FILE, 'a', encoding='utf-8')
        mock_file_open().write.assert_called_once_with(expected_entry_content)
        mock_print.assert_called_once_with(f"Entry added to {DEFAULT_LOG_FILE}")

    @patch('datetime.datetime')
    @patch('os.path.exists')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_add_entry_creates_file_and_appends(self, mock_print, mock_file_open, mock_getsize, mock_exists, mock_dt):
        # Mock rationale: datetime.datetime is mocked to control the timestamp.
        # os.path.exists and os.path.getsize are mocked to simulate a non-existent file.
        # builtins.open is mocked to capture file write operations.
        # builtins.print is mocked to prevent actual console output during test.
        mock_dt.now.return_value = self.mock_now
        mock_exists.return_value = False # File does not exist initially

        test_entry = "First steps into the unknown."
        expected_entry_content = f"## {self.mock_strftime}\n{test_entry}\n\n"

        add_entry(DEFAULT_LOG_FILE, test_entry)

        # Check that _ensure_log_header was called and wrote the header
        # The mock_open will be called twice: once for 'w' (header), once for 'a' (entry)
        mock_file_open.assert_any_call(DEFAULT_LOG_FILE, 'w', encoding='utf-8')
        mock_file_open.assert_any_call(DEFAULT_LOG_FILE, 'a', encoding='utf-8')
        
        # Verify the header was written first, then the entry
        handle = mock_file_open()
        self.assertEqual(handle.write.call_count, 2)
        handle.write.assert_any_call(LOG_HEADER)
        handle.write.assert_any_call(expected_entry_content)
        mock_print.assert_called_once_with(f"Entry added to {DEFAULT_LOG_FILE}")


    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_view_log_prints_content(self, mock_stdout, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists is mocked to simulate an existing file.
        # builtins.open is mocked to return predefined content when read.
        # sys.stdout is mocked to capture printed output for assertion.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = "Log content here."

        view_log(DEFAULT_LOG_FILE)

        mock_exists.assert_called_once_with(DEFAULT_LOG_FILE)
        mock_file_open.assert_called_once_with(DEFAULT_LOG_FILE, 'r', encoding='utf-8')
        self.assertEqual(mock_stdout.getvalue(), "Log content here.\n")

    @patch('os.path.exists')
    @patch('builtins.print')
    def test_view_log_handles_non_existent_file(self, mock_print, mock_exists):
        # Mock rationale: os.path.exists is mocked to simulate a non-existent file.
        # builtins.print is mocked to capture error message.
        mock_exists.return_value = False

        view_log(DEFAULT_LOG_FILE)

        mock_exists.assert_called_once_with(DEFAULT_LOG_FILE)
        mock_print.assert_called_once_with(f"Log file '{DEFAULT_LOG_FILE}' not found. Start by adding an entry.")
