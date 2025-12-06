import unittest
from unittest.mock import patch, mock_open
import datetime
import os
from src.chronicle_keeper import add_entry, main

class TestChronicleKeeper(unittest.TestCase):

    @patch('datetime.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_add_entry_to_new_file(self, mock_makedirs, mock_file_open, mock_dt):
        # Mock rationale: Ensure deterministic timestamp for testing.
        mock_dt.now.return_value = datetime.datetime(2023, 10, 27, 10, 30, 0)
        
        test_message = "Discovered a new cache of canned beans."
        test_file = "test_chronicle.md"
        
        add_entry(test_message, test_file)
        
        # Mock rationale: Verify file operations without actual disk I/O.
        mock_makedirs.assert_called_once_with('.', exist_ok=True) # Default path, so '.'
        mock_file_open.assert_called_once_with(test_file, 'a', encoding='utf-8')
        
        expected_content = "## 2023-10-27 10:30:00\n- Discovered a new cache of canned beans.\n\n"
        mock_file_open().write.assert_called_once_with(expected_content)

    @patch('datetime.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_add_entry_to_existing_file(self, mock_makedirs, mock_file_open, mock_dt):
        # Mock rationale: Ensure deterministic timestamp for testing.
        mock_dt.now.return_value = datetime.datetime(2023, 10, 27, 11, 0, 0)
        
        test_message = "Repaired the water purifier."
        test_file = "existing_chronicle.md"
        
        add_entry(test_message, test_file)
        
        # Mock rationale: Verify file operations without actual disk I/O.
        mock_makedirs.assert_called_once_with('.', exist_ok=True)
        mock_file_open.assert_called_once_with(test_file, 'a', encoding='utf-8')
        
        expected_content = "## 2023-10-27 11:00:00\n- Repaired the water purifier.\n\n"
        mock_file_open().write.assert_called_once_with(expected_content)

    @patch('datetime.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_add_entry_with_custom_path(self, mock_makedirs, mock_file_open, mock_dt):
        # Mock rationale: Ensure deterministic timestamp for testing.
        mock_dt.now.return_value = datetime.datetime(2023, 10, 27, 12, 0, 0)
        
        test_message = "Found a new route through the ruins."
        test_dir = "logs"
        test_file = os.path.join(test_dir, "daily_log.md")
        
        add_entry(test_message, test_file)
        
        # Mock rationale: Verify file operations without actual disk I/O.
        mock_makedirs.assert_called_once_with(test_dir, exist_ok=True)
        mock_file_open.assert_called_once_with(test_file, 'a', encoding='utf-8')
        
        expected_content = "## 2023-10-27 12:00:00\n- Found a new route through the ruins.\n\n"
        mock_file_open().write.assert_called_once_with(expected_content)

    @patch('src.chronicle_keeper.add_entry')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function(self, mock_parse_args, mock_add_entry):
        # Mock rationale: Simulate command-line arguments without actual parsing.
        mock_parse_args.return_value.message = "Testing main function."
        mock_parse_args.return_value.file = "main_test.md"

        main()
        
        # Mock rationale: Verify that add_entry is called with correct arguments from CLI.
        mock_add_entry.assert_called_once_with("Testing main function.", "main_test.md")
