import unittest
import json
import os
from unittest.mock import patch, mock_open
from datetime import datetime

# Import the functions from the main script
# For self-contained execution, we'll adjust sys.path to find the module.
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scrutiny_log

class TestScrutinyLog(unittest.TestCase):

    def setUp(self):
        # Ensure a clean state for each test
        self.mock_log_file_content = []
        self.mock_datetime_str = "2023-10-27 12:34:56"
        # Mock datetime.now() to return a fixed time for deterministic timestamps
        self.mock_datetime_patcher = patch('scrutiny_log.datetime')
        self.mock_datetime = self.mock_datetime_patcher.start()
        self.mock_datetime.now.return_value = datetime.strptime(self.mock_datetime_str, "%Y-%m-%d %H:%M:%S")
        self.mock_datetime.strftime = datetime.strftime # Keep original strftime behavior

    def tearDown(self):
        self.mock_datetime_patcher.stop()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('sys.stdout') # Mock rationale: Capture print statements to avoid polluting test output.
    def test_add_entry_new_file(self, mock_stdout, mock_json_dump, mock_file_open, mock_exists):
        # Mock rationale: Simulate a scenario where the log file does not exist initially.
        # `os.path.exists` is mocked to return False.
        # `builtins.open` is mocked to capture write operations.
        # `json.dump` is mocked to verify the data being written.
        mock_exists.return_value = False
        
        scrutiny_log.add_entry("Shiny Rock", "Mineral", "Pristine", "Cave Entrance")

        mock_exists.assert_called_once_with(scrutiny_log.LOG_FILE)
        mock_file_open.assert_called_once_with(scrutiny_log.LOG_FILE, 'w', encoding='utf-8')
        
        expected_log_data = [{
            "timestamp": self.mock_datetime_str,
            "item": "Shiny Rock",
            "category": "Mineral",
            "condition": "Pristine",
            "location": "Cave Entrance"
        }]
        mock_json_dump.assert_called_once_with(expected_log_data, mock_file_open(), indent=4, ensure_ascii=False)
        mock_stdout.write.assert_any_call("Logged: 'Shiny Rock' successfully.\n")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('sys.stdout') # Mock rationale: Capture print statements to avoid polluting test output.
    def test_add_entry_existing_file(self, mock_stdout, mock_json_dump, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Simulate adding an entry to an existing log file.
        # `os.path.exists` returns True.
        # `json.load` provides initial content.
        # `json.dump` captures the updated content.
        mock_exists.return_value = True
        initial_log = [{
            "timestamp": "2023-10-26 09:00:00",
            "item": "Old Boot",
            "category": "Clothing",
            "condition": "Damaged",
            "location": "River Bank"
        }]
        mock_json_load.return_value = initial_log
        
        scrutiny_log.add_entry("Rusty Can", "Junk", "Broken", "Dump Site")

        mock_exists.assert_called_once_with(scrutiny_log.LOG_FILE)
        mock_file_open.assert_any_call(scrutiny_log.LOG_FILE, 'r', encoding='utf-8') # For load
        mock_file_open.assert_any_call(scrutiny_log.LOG_FILE, 'w', encoding='utf-8') # For save

        expected_log_data = initial_log + [{
            "timestamp": self.mock_datetime_str,
            "item": "Rusty Can",
            "category": "Junk",
            "condition": "Broken",
            "location": "Dump Site"
        }]
        mock_json_dump.assert_called_once_with(expected_log_data, mock_file_open(), indent=4, ensure_ascii=False)
        mock_stdout.write.assert_any_call("Logged: 'Rusty Can' successfully.\n")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout')
    def test_list_entries_empty(self, mock_stdout, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Test listing when the log file is empty or non-existent.
        # `os.path.exists` returns False.
        # `sys.stdout` is mocked to capture printed output.
        mock_exists.return_value = False
        
        scrutiny_log.list_entries()
        
        mock_stdout.write.assert_any_call("The Scavenger's Scrutiny Log is empty. Go forth and scavenge!\n")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout')
    def test_list_entries_with_data(self, mock_stdout, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Test listing entries when the log file contains data.
        # `os.path.exists` returns True.
        # `json.load` provides sample log data.
        # `sys.stdout` captures printed output for verification.
        mock_exists.return_value = True
        sample_log = [
            {"timestamp": "2023-10-26 09:00:00", "item": "Old Boot", "category": "Clothing", "condition": "Damaged", "location": "River Bank"},
            {"timestamp": "2023-10-27 10:00:00", "item": "Shiny Rock", "category": "Mineral", "condition": "Pristine", "location": "Cave Entrance"}
        ]
        mock_json_load.return_value = sample_log
        
        scrutiny_log.list_entries()
        
        mock_stdout.write.assert_any_call("\n--- Scavenger's Scrutiny Log ---\n")
        mock_stdout.write.assert_any_call("[2023-10-26 09:00:00] Item: Old Boot, Category: Clothing, Condition: Damaged, Location: River Bank\n")
        mock_stdout.write.assert_any_call("[2023-10-27 10:00:00] Item: Shiny Rock, Category: Mineral, Condition: Pristine, Location: Cave Entrance\n")
        mock_stdout.write.assert_any_call("----------------------------------\n\n")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout')
    def test_search_by_query(self, mock_stdout, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Test searching by item name query.
        # `os.path.exists` returns True.
        # `json.load` provides sample log data.
        # `sys.stdout` captures printed output.
        mock_exists.return_value = True
        sample_log = [
            {"timestamp": "2023-10-26 09:00:00", "item": "Old Boot", "category": "Clothing", "condition": "Damaged", "location": "River Bank"},
            {"timestamp": "2023-10-27 10:00:00", "item": "Shiny Rock", "category": "Mineral", "condition": "Pristine", "location": "Cave Entrance"},
            {"timestamp": "2023-10-27 11:00:00", "item": "Rusty Spoon", "category": "Tool", "condition": "Broken", "location": "Kitchen"}
        ]
        mock_json_load.return_value = sample_log
        
        scrutiny_log.search_entries(query="rock")
        
        mock_stdout.write.assert_any_call("\n--- Scavenger's Scrutiny Search Results ---\n")
        mock_stdout.write.assert_any_call("[2023-10-27 10:00:00] Item: Shiny Rock, Category: Mineral, Condition: Pristine, Location: Cave Entrance\n")
        self.assertNotIn("[2023-10-26 09:00:00] Item: Old Boot, Category: Clothing, Condition: Damaged, Location: River Bank\n", [call.args[0] for call in mock_stdout.write.call_args_list])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout')
    def test_search_by_category(self, mock_stdout, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Test searching by item category.
        # `os.path.exists` returns True.
        # `json.load` provides sample log data.
        # `sys.stdout` captures printed output.
        mock_exists.return_value = True
        sample_log = [
            {"timestamp": "2023-10-26 09:00:00", "item": "Old Boot", "category": "Clothing", "condition": "Damaged", "location": "River Bank"},
            {"timestamp": "2023-10-27 10:00:00", "item": "Shiny Rock", "category": "Mineral", "condition": "Pristine", "location": "Cave Entrance"},
            {"timestamp": "2023-10-27 11:00:00", "item": "Rusty Spoon", "category": "Tool", "condition": "Broken", "location": "Kitchen"}
        ]
        mock_json_load.return_value = sample_log
        
        scrutiny_log.search_entries(category="tool")
        
        mock_stdout.write.assert_any_call("\n--- Scavenger's Scrutiny Search Results ---\n")
        mock_stdout.write.assert_any_call("[2023-10-27 11:00:00] Item: Rusty Spoon, Category: Tool, Condition: Broken, Location: Kitchen\n")
        self.assertNotIn("[2023-10-26 09:00:00] Item: Old Boot, Category: Clothing, Condition: Damaged, Location: River Bank\n", [call.args[0] for call in mock_stdout.write.call_args_list])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout')
    def test_search_by_location(self, mock_stdout, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Test searching by item location.
        # `os.path.exists` returns True.
        # `json.load` provides sample log data.
        # `sys.stdout` captures printed output.
        mock_exists.return_value = True
        sample_log = [
            {"timestamp": "2023-10-26 09:00:00", "item": "Old Boot", "category": "Clothing", "condition": "Damaged", "location": "River Bank"},
            {"timestamp": "2023-10-27 10:00:00", "item": "Shiny Rock", "category": "Mineral", "condition": "Pristine", "location": "Cave Entrance"},
            {"timestamp": "2023-10-27 11:00:00", "item": "Rusty Spoon", "category": "Tool", "condition": "Broken", "location": "Kitchen"}
        ]
        mock_json_load.return_value = sample_log
        
        scrutiny_log.search_entries(location="river")
        
        mock_stdout.write.assert_any_call("\n--- Scavenger's Scrutiny Search Results ---\n")
        mock_stdout.write.assert_any_call("[2023-10-26 09:00:00] Item: Old Boot, Category: Clothing, Condition: Damaged, Location: River Bank\n")
        self.assertNotIn("[2023-10-27 10:00:00] Item: Shiny Rock, Category: Mineral, Condition: Pristine, Location: Cave Entrance\n", [call.args[0] for call in mock_stdout.write.call_args_list])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout')
    def test_search_no_results(self, mock_stdout, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Test searching when no matching entries are found.
        # `os.path.exists` returns True.
        # `json.load` provides sample log data.
        # `sys.stdout` captures printed output.
        mock_exists.return_value = True
        sample_log = [
            {"timestamp": "2023-10-26 09:00:00", "item": "Old Boot", "category": "Clothing", "condition": "Damaged", "location": "River Bank"}
        ]
        mock_json_load.return_value = sample_log
        
        scrutiny_log.search_entries(query="nonexistent")
        
        mock_stdout.write.assert_any_call("No matching entries found.\n")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout')
    def test_search_empty_log(self, mock_stdout, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Test searching when the log is empty.
        # `os.path.exists` returns False.
        # `sys.stdout` captures printed output.
        mock_exists.return_value = False
        
        scrutiny_log.search_entries(query="anything")
        
        mock_stdout.write.assert_any_call("The Scavenger's Scrutiny Log is empty. Nothing to search.\n")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "", 0))
    @patch('sys.stdout')
    def test_load_log_corrupted_file(self, mock_stdout, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: Simulate a corrupted JSON log file.
        # `os.path.exists` returns True.
        # `json.load` is mocked to raise a JSONDecodeError.
        # `sys.stdout` captures the warning message.
        mock_exists.return_value = True
        
        result = scrutiny_log.load_log()
        
        self.assertEqual(result, [])
        mock_stdout.write.assert_any_call(f"Warning: {scrutiny_log.LOG_FILE} is corrupted or empty. Starting with an empty log.\n")


if __name__ == '__main__':
    unittest.main()
