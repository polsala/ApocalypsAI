import unittest
from unittest.mock import patch, mock_open
import json
import os
from datetime import datetime, timedelta

# Import the functions from the tracker script
# We need to adjust the import path for testing
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import tracker

class TestTracker(unittest.TestCase):

    def setUp(self):
        # Reset DATA_FILE path for testing to ensure it points to a mockable location
        # Mock rationale: Ensure that the tracker uses a controlled path for its data file during tests.
        self.mock_data_file_path = '/mock/path/resources.json'
        patcher = patch('tracker.get_data_file_path', return_value=self.mock_data_file_path)
        self.mock_get_data_file_path = patcher.start()
        self.addCleanup(patcher.stop)

        # Mock os.path.exists to control file existence
        # Mock rationale: Simulate whether the data file exists without actual file system checks.
        patcher = patch('os.path.exists', return_value=False)
        self.mock_exists = patcher.start()
        self.addCleanup(patcher.stop)

        # Mock datetime.now().date() for deterministic expiration checks
        # Mock rationale: Fix the 'current date' to ensure expiration logic is tested consistently.
        self.fixed_today = datetime(2024, 1, 15).date()
        patcher = patch('tracker.datetime')
        self.mock_datetime = patcher.start()
        self.mock_datetime.now.return_value.date.return_value = self.fixed_today
        self.addCleanup(patcher.stop)


    def mock_file_operations(self, initial_data=None):
        """Helper to mock file open/read/write operations."""
        mock_file_content = json.dumps(initial_data) if initial_data else '[]'
        
        # Mock rationale: Simulate file reading by providing a string buffer.
        m_open = mock_open(read_data=mock_file_content)
        
        # Mock rationale: Ensure os.path.exists returns True if initial_data is provided.
        self.mock_exists.return_value = bool(initial_data)

        # Patch builtins.open
        patcher = patch('builtins.open', m_open)
        self.mock_open = patcher.start()
        self.addCleanup(patcher.stop)

        # Patch json.dump to capture what's written
        # Mock rationale: Capture the data that would be written to the file for assertion.
        patcher = patch('json.dump')
        self.mock_json_dump = patcher.start()
        self.addCleanup(patcher.stop)

        # Patch json.load to control what's read
        # Mock rationale: Control the data that is 'loaded' from the file.
        patcher = patch('json.load', return_value=initial_data if initial_data else [])
        self.mock_json_load = patcher.start()
        self.addCleanup(patcher.stop)

        return m_open

    def test_add_new_item(self):
        self.mock_file_operations(initial_data=[])
        tracker.add_item("Canned Beans", 10, "2025-12-31", "Pantry")
        
        expected_data = [{
            'name': 'Canned Beans',
            'quantity': 10,
            'expires': '2025-12-31',
            'location': 'Pantry'
        }]
        self.mock_json_dump.assert_called_once_with(expected_data, unittest.mock.ANY, indent=2)
        self.mock_open.assert_called_with(self.mock_data_file_path, 'w')

    def test_add_to_existing_item(self):
        initial_data = [{
            'name': 'Canned Beans',
            'quantity': 5,
            'expires': '2025-12-31',
            'location': 'Pantry'
        }]
        self.mock_file_operations(initial_data=initial_data)
        tracker.add_item("Canned Beans", 3)

        expected_data = [{
            'name': 'Canned Beans',
            'quantity': 8,
            'expires': '2025-12-31',
            'location': 'Pantry'
        }]
        self.mock_json_dump.assert_called_once_with(expected_data, unittest.mock.ANY, indent=2)

    def test_add_to_existing_item_with_update_details(self):
        initial_data = [{
            'name': 'Canned Beans',
            'quantity': 5,
            'expires': '2025-12-31',
            'location': 'Pantry'
        }]
        self.mock_file_operations(initial_data=initial_data)
        tracker.add_item("Canned Beans", 3, expires="2026-01-01", location="New Shelf")

        expected_data = [{
            'name': 'Canned Beans',
            'quantity': 8,
            'expires': '2026-01-01',
            'location': 'New Shelf'
        }]
        self.mock_json_dump.assert_called_once_with(expected_data, unittest.mock.ANY, indent=2)

    def test_consume_existing_item(self):
        initial_data = [{
            'name': 'Canned Beans',
            'quantity': 10,
            'expires': '2025-12-31',
            'location': 'Pantry'
        }]
        self.mock_file_operations(initial_data=initial_data)
        tracker.consume_item("Canned Beans", 3)

        expected_data = [{
            'name': 'Canned Beans',
            'quantity': 7,
            'expires': '2025-12-31',
            'location': 'Pantry'
        }]
        self.mock_json_dump.assert_called_once_with(expected_data, unittest.mock.ANY, indent=2)

    def test_consume_item_not_found(self):
        self.mock_file_operations(initial_data=[])
        with patch('builtins.print') as mock_print:
            tracker.consume_item("Nonexistent Item", 1)
            mock_print.assert_called_with("Item 'Nonexistent Item' not found in inventory.")
        self.mock_json_dump.assert_not_called()

    def test_consume_more_than_available(self):
        initial_data = [{
            'name': 'Canned Beans',
            'quantity': 2,
            'expires': '2025-12-31',
            'location': 'Pantry'
        }]
        self.mock_file_operations(initial_data=initial_data)
        with patch('builtins.print') as mock_print:
            tracker.consume_item("Canned Beans", 3)
            mock_print.assert_called_with("Not enough Canned Beans to consume. Only 2 available.")
        self.mock_json_dump.assert_not_called()

    def test_consume_item_to_zero(self):
        initial_data = [{
            'name': 'Canned Beans',
            'quantity': 1,
            'expires': '2025-12-31',
            'location': 'Pantry'
        }]
        self.mock_file_operations(initial_data=initial_data)
        tracker.consume_item("Canned Beans", 1)

        expected_data = [] # Item should be removed
        self.mock_json_dump.assert_called_once_with(expected_data, unittest.mock.ANY, indent=2)

    def test_list_empty_inventory(self):
        self.mock_file_operations(initial_data=[])
        with patch('builtins.print') as mock_print:
            tracker.list_items()
            mock_print.assert_called_with("Your inventory is empty. Time to scavenge!")

    def test_list_items_with_various_statuses(self):
        # Set fixed_today to 2024-01-15
        expired_date = (self.fixed_today - timedelta(days=10)).strftime('%Y-%m-%d') # 2024-01-05
        expiring_soon_date = (self.fixed_today + timedelta(days=15)).strftime('%Y-%m-%d') # 2024-01-30
        future_date = (self.fixed_today + timedelta(days=100)).strftime('%Y-%m-%d') # 2024-04-24

        initial_data = [
            {'name': 'Expired Rations', 'quantity': 1, 'expires': expired_date, 'location': 'Box A'},
            {'name': 'Low Water', 'quantity': 3, 'expires': future_date, 'location': 'Box B'},
            {'name': 'Expiring Meds', 'quantity': 10, 'expires': expiring_soon_date, 'location': 'Box C'},
            {'name': 'Good Stuff', 'quantity': 20, 'expires': future_date, 'location': 'Box D'},
            {'name': 'No Date Item', 'quantity': 7, 'expires': None, 'location': None},
        ]
        self.mock_file_operations(initial_data=initial_data)

        with patch('builtins.print') as mock_print:
            tracker.list_items()
            output_calls = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(output_calls)

            self.assertIn("--- Current Inventory ---", output)
            self.assertIn(f"Expired Rations             1     {expired_date} (EXPIRED!) (LOW STOCK!)", output)
            self.assertIn(f"Expiring Meds              10     {expiring_soon_date} (Expiring soon!)", output)
            self.assertIn(f"Good Stuff                 20     {future_date}", output)
            self.assertIn(f"Low Water                  3      {future_date} (LOW STOCK!)", output)
            self.assertIn("No Date Item               7      N/A          N/A", output)

    def test_load_corrupted_json(self):
        # Mock rationale: Simulate a corrupted JSON file content.
        self_mock_open = mock_open(read_data='{ "items": [ }')
        self.mock_exists.return_value = True
        with patch('builtins.open', self_mock_open),
             patch('builtins.print') as mock_print:
            resources = tracker.load_resources()
            self.assertEqual(resources, [])
            mock_print.assert_called_with(f"Warning: {tracker.DATA_FILE} is corrupted. Starting with an empty inventory.")

    def test_add_item_zero_quantity(self):
        self.mock_file_operations(initial_data=[])
        with patch('builtins.print') as mock_print:
            tracker.add_item("Test Item", 0)
            mock_print.assert_called_with("Quantity must be positive.")
        self.mock_json_dump.assert_not_called()

    def test_consume_item_zero_quantity(self):
        initial_data = [{'name': 'Test Item', 'quantity': 5, 'expires': None, 'location': None}]
        self.mock_file_operations(initial_data=initial_data)
        with patch('builtins.print') as mock_print:
            tracker.consume_item("Test Item", 0)
            mock_print.assert_called_with("Quantity must be positive.")
        self.mock_json_dump.assert_not_called()


if __name__ == '__main__':
    unittest.main()
