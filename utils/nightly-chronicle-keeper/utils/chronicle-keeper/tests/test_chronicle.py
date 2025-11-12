import unittest
from unittest import mock
from datetime import datetime, date
import os
import sys
from io import StringIO
from pathlib import Path

# Adjust path to import chronicle.py from src directory
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
import chronicle

class TestChronicleKeeper(unittest.TestCase):

    def setUp(self):
        # Use temporary files for testing within the tests directory
        self.test_log_file = Path(__file__).parent / 'test_chronicle.log'
        self.test_config_file = Path(__file__).parent / 'test_chronicle.config'
        
        # Override constants in chronicle module for testing to point to test files
        chronicle.LOG_FILE = self.test_log_file
        chronicle.CONFIG_FILE = self.test_config_file

        # Ensure files are clean before each test
        if self.test_log_file.exists():
            self.test_log_file.unlink()
        if self.test_config_file.exists():
            self.test_config_file.unlink()

        # Capture stdout for testing print statements
        self._original_stdout = sys.stdout
        sys.stdout = self._captured_stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self._original_stdout

        # Clean up test files
        if self.test_log_file.exists():
            self.test_log_file.unlink()
        if self.test_config_file.exists():
            self.test_config_file.unlink()

    def get_captured_output(self):
        return self._captured_stdout.getvalue()

    @mock.patch('datetime.datetime')
    def test_add_entry_pre_apocalypse(self, mock_dt):
        # Mock rationale: Ensure deterministic timestamp for entry and category determination.
        mock_dt.now.return_value = datetime(2024, 7, 10, 10, 0, 0)
        mock_dt.date.return_value = date(2024, 7, 10)
        # Allow other datetime operations to work normally if needed by the module under test
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw) 

        # Set a doom date in the future
        chronicle.config_doom_date('2024-07-15')
        self.assertEqual(self.test_config_file.read_text().strip(), '2024-07-15')

        chronicle.add_entry("Test message before doom")

        expected_log = "[2024-07-10 10:00:00] [PRE-APOCALYPSE] Test message before doom\n"
        self.assertEqual(self.test_log_file.read_text(), expected_log)
        self.assertIn("Entry added", self.get_captured_output())

    @mock.patch('datetime.datetime')
    def test_add_entry_post_apocalypse(self, mock_dt):
        # Mock rationale: Ensure deterministic timestamp for entry and category determination.
        mock_dt.now.return_value = datetime(2024, 7, 20, 14, 30, 0)
        mock_dt.date.return_value = date(2024, 7, 20)
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Set a doom date in the past
        chronicle.config_doom_date('2024-07-15')
        self.assertEqual(self.test_config_file.read_text().strip(), '2024-07-15')

        chronicle.add_entry("Test message after doom")

        expected_log = "[2024-07-20 14:30:00] [POST-APOCALYPSE] Test message after doom\n"
        self.assertEqual(self.test_log_file.read_text(), expected_log)
        self.assertIn("Entry added", self.get_captured_output())

    def test_list_entries(self):
        # Mock rationale: Directly write to the log file to control its content for listing.
        self.test_log_file.write_text(
            "[2024-01-01 12:00:00] [PRE-APOCALYPSE] First entry\n"
            "[2024-01-02 13:00:00] [POST-APOCALYPSE] Second entry\n"
        )
        chronicle.list_entries()
        output = self.get_captured_output()
        self.assertIn("First entry", output)
        self.assertIn("Second entry", output)
        self.assertIn("--- Chronicle Entries ---", output)

    def test_list_entries_filtered_pre(self):
        # Mock rationale: Directly write to the log file to control its content for listing.
        self.test_log_file.write_text(
            "[2024-01-01 12:00:00] [PRE-APOCALYPSE] Pre-entry 1\n"
            "[2024-01-02 13:00:00] [POST-APOCALYPSE] Post-entry 1\n"
            "[2024-01-03 14:00:00] [PRE-APOCALYPSE] Pre-entry 2\n"
        )
        chronicle.list_entries('pre')
        output = self.get_captured_output()
        self.assertIn("Pre-entry 1", output)
        self.assertNotIn("Post-entry 1", output)
        self.assertIn("Pre-entry 2", output)

    def test_list_entries_filtered_post(self):
        # Mock rationale: Directly write to the log file to control its content for listing.
        self.test_log_file.write_text(
            "[2024-01-01 12:00:00] [PRE-APOCALYPSE] Pre-entry 1\n"
            "[2024-01-02 13:00:00] [POST-APOCALYPSE] Post-entry 1\n"
            "[2024-01-03 14:00:00] [PRE-APOCALYPSE] Pre-entry 2\n"
        )
        chronicle.list_entries('post')
        output = self.get_captured_output()
        self.assertNotIn("Pre-entry 1", output)
        self.assertIn("Post-entry 1", output)
        self.assertNotIn("Pre-entry 2", output)

    def test_config_doom_date_set_and_get(self):
        chronicle.config_doom_date('2025-01-01')
        self.assertEqual(self.test_config_file.read_text().strip(), '2025-01-01')
        self.assertIn("Doom Date set to: 2025-01-01", self.get_captured_output())
        
        # Clear captured output for next check
        sys.stdout = StringIO()

        chronicle.config_doom_date()
        self.assertIn("Current Doom Date: 2025-01-01", self.get_captured_output())

    def test_config_doom_date_invalid_format(self):
        chronicle.config_doom_date('invalid-date')
        self.assertFalse(self.test_config_file.exists())
        self.assertIn("Error: Invalid date format", self.get_captured_output())

    def test_default_doom_date_when_no_config(self):
        # Mock rationale: Ensure _get_doom_date returns the default when no config file exists.
        self.assertFalse(self.test_config_file.exists())
        doom_date = chronicle._get_doom_date()
        self.assertEqual(doom_date, chronicle.DEFAULT_DOOM_DATE)

    def test_default_doom_date_when_empty_config(self):
        # Mock rationale: Ensure _get_doom_date returns the default when config file is empty.
        self.test_config_file.write_text('')
        doom_date = chronicle._get_doom_date()
        self.assertEqual(doom_date, chronicle.DEFAULT_DOOM_DATE)

    def test_no_log_file_on_list(self):
        # Mock rationale: Ensure the correct message is printed when no log file exists.
        self.assertFalse(self.test_log_file.exists())
        chronicle.list_entries()
        self.assertIn("No chronicle entries found", self.get_captured_output())
