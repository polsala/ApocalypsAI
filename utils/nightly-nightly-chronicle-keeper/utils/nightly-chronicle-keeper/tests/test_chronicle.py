import unittest
from unittest.mock import patch, mock_open, call
from datetime import datetime
import os
import sys

# Add src directory to path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import chronicle # The module to test

class TestChronicle(unittest.TestCase):
    CHRONICLE_FILE = ".chronicle.log"
    MOCKED_TIMESTAMP = "2023-10-27 10:00:00"

    @patch('datetime.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True) # Mock rationale: Assume file exists for most tests to focus on content.
    @patch('os.getcwd', return_value='/mock/path') # Mock rationale: Ensure deterministic file path for chronicle.
    def test_add_entry(self, mock_getcwd, mock_exists, mock_file, mock_dt):
        # Mock rationale: Ensure deterministic timestamps for entries.
        mock_dt.now.return_value = datetime(2023, 10, 27, 10, 0, 0)

        # Mock rationale: Prevent actual file I/O and capture written content.
        chronicle.ChronicleManager().add_entry("First entry")

        mock_file.assert_called_once_with(os.path.join('/mock/path', self.CHRONICLE_FILE), 'a', encoding='utf-8')
        mock_file().write.assert_called_once_with(f"[{self.MOCKED_TIMESTAMP}] First entry\n")

    @patch('datetime.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate file not existing initially.
    @patch('os.getcwd', return_value='/mock/path') # Mock rationale: Ensure deterministic file path for chronicle.
    def test_add_entry_creates_file_if_not_exists(self, mock_getcwd, mock_exists, mock_file, mock_dt):
        mock_dt.now.return_value = datetime(2023, 10, 27, 10, 0, 0) # Mock rationale: Deterministic timestamp.

        manager = chronicle.ChronicleManager()
        manager.add_entry("New entry, new file")

        # Expect two calls to open: one for 'w' (init), one for 'a' (add)
        expected_path = os.path.join('/mock/path', self.CHRONICLE_FILE)
        mock_file.assert_has_calls([
            call(expected_path, 'w', encoding='utf-8'), # init_chronicle call
            call().write(""),
            call(expected_path, 'a', encoding='utf-8'), # add_entry call
            call().write(f"[{self.MOCKED_TIMESTAMP}] New entry, new file\n")
        ])
        # Ensure os.path.exists was checked twice (once by add_entry, once by init_chronicle)
        self.assertEqual(mock_exists.call_count, 2)

    @patch('datetime.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.getcwd', return_value='/mock/path') # Mock rationale: Ensure deterministic file path for chronicle.
    def test_list_entries(self, mock_getcwd, mock_exists, mock_file, mock_dt):
        mock_dt.now.return_value = datetime(2023, 10, 27, 10, 0, 0) # Mock rationale: Deterministic timestamp.
        
        # Mock rationale: Simulate file content for reading.
        mock_file.return_value.read.return_value = (
            f"[{self.MOCKED_TIMESTAMP}] Entry 1\n"
            f"[{self.MOCKED_TIMESTAMP}] Entry 2\n"
            f"[{self.MOCKED_TIMESTAMP}] Entry 3\n"
        )

        manager = chronicle.ChronicleManager()
        entries = manager.list_entries(all_entries=True) # Test --all
        self.assertEqual(len(entries), 3)
        self.assertEqual(entries[0], f"[{self.MOCKED_TIMESTAMP}] Entry 1")
        self.assertEqual(entries[2], f"[{self.MOCKED_TIMESTAMP}] Entry 3")
        mock_file.assert_called_once_with(os.path.join('/mock/path', self.CHRONICLE_FILE), 'r', encoding='utf-8')

        # Test listing last N entries
        mock_file.reset_mock() # Reset mock calls for the next assertion
        mock_file.return_value.read.return_value = (
            f"[{self.MOCKED_TIMESTAMP}] Entry A\n"
            f"[{self.MOCKED_TIMESTAMP}] Entry B\n"
            f"[{self.MOCKED_TIMESTAMP}] Entry C\n"
        )
        entries_last_2 = manager.list_entries(count=2) # Test --count 2
        self.assertEqual(len(entries_last_2), 2)
        self.assertEqual(entries_last_2[0], f"[{self.MOCKED_TIMESTAMP}] Entry B")
        self.assertEqual(entries_last_2[1], f"[{self.MOCKED_TIMESTAMP}] Entry C")

    @patch('datetime.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.getcwd', return_value='/mock/path') # Mock rationale: Ensure deterministic file path for chronicle.
    def test_search_entries(self, mock_getcwd, mock_exists, mock_file, mock_dt):
        mock_dt.now.return_value = datetime(2023, 10, 27, 10, 0, 0) # Mock rationale: Deterministic timestamp.

        # Mock rationale: Simulate file content for searching.
        mock_file.return_value.read.return_value = (
            f"[{self.MOCKED_TIMESTAMP}] Today I saw a cat.\n"
            f"[{self.MOCKED_TIMESTAMP}] The sky was clear.\n"
            f"[{self.MOCKED_TIMESTAMP}] Another cat sighting!\n"
        )

        manager = chronicle.ChronicleManager()
        results = manager.search_entries("cat")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], f"[{self.MOCKED_TIMESTAMP}] Today I saw a cat.")
        self.assertEqual(results[1], f"[{self.MOCKED_TIMESTAMP}] Another cat sighting!")
        mock_file.assert_called_once_with(os.path.join('/mock/path', self.CHRONICLE_FILE), 'r', encoding='utf-8')

        results_no_match = manager.search_entries("dog")
        self.assertEqual(len(results_no_match), 0)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate file not existing initially.
    @patch('os.getcwd', return_value='/mock/path') # Mock rationale: Ensure deterministic file path for chronicle.
    def test_init_chronicle(self, mock_getcwd, mock_exists, mock_file):
        manager = chronicle.ChronicleManager()
        manager.init_chronicle()
        mock_exists.assert_called_once_with(os.path.join('/mock/path', self.CHRONICLE_FILE))
        mock_file.assert_called_once_with(os.path.join('/mock/path', self.CHRONICLE_FILE), 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with("") # Ensure it creates an empty file

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate file existing.
    @patch('os.getcwd', return_value='/mock/path') # Mock rationale: Ensure deterministic file path for chronicle.
    def test_init_chronicle_already_exists(self, mock_getcwd, mock_exists, mock_file):
        manager = chronicle.ChronicleManager()
        manager.init_chronicle()
        mock_exists.assert_called_once_with(os.path.join('/mock/path', self.CHRONICLE_FILE))
        mock_file.assert_not_called() # No file operations if it already exists

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate no file for reading.
    @patch('os.getcwd', return_value='/mock/path') # Mock rationale: Ensure deterministic file path for chronicle.
    def test_list_entries_empty_file(self, mock_getcwd, mock_exists, mock_file):
        manager = chronicle.ChronicleManager()
        entries = manager.list_entries(all_entries=True)
        self.assertEqual(entries, [])
        mock_file.assert_not_called() # No file opened if it doesn't exist

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate no file for reading.
    @patch('os.getcwd', return_value='/mock/path') # Mock rationale: Ensure deterministic file path for chronicle.
    def test_search_entries_empty_file(self, mock_getcwd, mock_exists, mock_file):
        manager = chronicle.ChronicleManager()
        results = manager.search_entries("anything")
        self.assertEqual(results, [])
        mock_file.assert_not_called() # No file opened if it doesn't exist
