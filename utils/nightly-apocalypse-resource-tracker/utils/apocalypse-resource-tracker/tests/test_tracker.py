import unittest
import os
import json
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
import sys
from io import StringIO

# Adjust path to import tracker.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tracker import ResourceTracker, DATA_FILE, DATE_FORMAT

class TestResourceTracker(unittest.TestCase):

    def setUp(self):
        # Ensure a clean state for each test
        self.test_data_file = 'test_resources.json'
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        self.tracker = ResourceTracker(data_file=self.test_data_file)
        self.mock_stdout = StringIO()
        self.real_stdout = sys.stdout
        sys.stdout = self.mock_stdout

    def tearDown(self):
        # Clean up after each test
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        sys.stdout = self.real_stdout # Restore stdout

    def _get_printed_output(self):
        return self.mock_stdout.getvalue()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_resources_empty_file(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate an empty or non-existent data file.
        mock_exists.return_value = False
        tracker = ResourceTracker(data_file=self.test_data_file)
        self.assertEqual(tracker.resources, {})
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = "" # Empty file content
        tracker = ResourceTracker(data_file=self.test_data_file)
        self.assertEqual(tracker.resources, {})
        self.assertIn("Warning: Could not decode", self._get_printed_output())

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_load_resources_existing_data(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate loading existing resource data from a file.
        mock_data = {
            "water": {"name": "water", "quantity": 10, "expiry_date": "2025-01-01", "notes": ""},
        }
        mock_file_open.return_value.read.return_value = json.dumps(mock_data)
        tracker = ResourceTracker(data_file=self.test_data_file)
        self.assertEqual(tracker.resources, mock_data)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_add_resource(self, mock_exists, mock_file_open):
        # Mock rationale: Prevent actual file I/O during resource addition.
        self.tracker.add_resource("Canned Beans", 10, "2025-12-31", "Protein source")
        self.assertIn("canned beans", self.tracker.resources)
        self.assertEqual(self.tracker.resources["canned beans"]["quantity"], 10)
        self.assertEqual(self.tracker.resources["canned beans"]["expiry_date"], "2025-12-31")
        self.assertEqual(self.tracker.resources["canned beans"]["notes"], "Protein source")
        self.assertIn("Added resource: canned beans", self._get_printed_output())
        mock_file_open().write.assert_called_once() # Ensure save was called

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_add_resource_invalid_expiry(self, mock_exists, mock_file_open):
        # Mock rationale: Prevent actual file I/O during resource addition.
        result = self.tracker.add_resource("Canned Beans", 10, "31-12-2025", "Protein source")
        self.assertFalse(result)
        self.assertNotIn("canned beans", self.tracker.resources)
        self.assertIn("Error: Invalid expiry date format", self._get_printed_output())
        mock_file_open().write.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_update_resource(self, mock_exists, mock_file_open):
        # Mock rationale: Prevent actual file I/O during resource update.
        self.tracker.add_resource("Water", 5, "2026-01-01")
        self.tracker.update_resource("Water", quantity=7, notes="Updated notes")
        self.assertEqual(self.tracker.resources["water"]["quantity"], 7)
        self.assertEqual(self.tracker.resources["water"]["notes"], "Updated notes")
        self.assertIn("Updated resource: water", self._get_printed_output())
        self.assertEqual(mock_file_open().write.call_count, 2) # Add + Update

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_update_resource_not_found(self, mock_exists, mock_file_open):
        # Mock rationale: Prevent actual file I/O during resource update.
        result = self.tracker.update_resource("NonExistent", quantity=10)
        self.assertFalse(result)
        self.assertIn("Resource 'nonexistent' not found.", self._get_printed_output())
        mock_file_open().write.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_remove_resource(self, mock_exists, mock_file_open):
        # Mock rationale: Prevent actual file I/O during resource removal.
        self.tracker.add_resource("First Aid Kit", 1, "2028-06-01")
        self.assertIn("first aid kit", self.tracker.resources)
        self.tracker.remove_resource("First Aid Kit")
        self.assertNotIn("first aid kit", self.tracker.resources)
        self.assertIn("Removed resource: first aid kit", self._get_printed_output())
        self.assertEqual(mock_file_open().write.call_count, 2) # Add + Remove

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_remove_resource_not_found(self, mock_exists, mock_file_open):
        # Mock rationale: Prevent actual file I/O during resource removal.
        result = self.tracker.remove_resource("NonExistent")
        self.assertFalse(result)
        self.assertIn("Resource 'nonexistent' not found.", self._get_printed_output())
        mock_file_open().write.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_list_resources(self, mock_exists, mock_file_open):
        # Mock rationale: Prevent actual file I/O during resource listing.
        self.tracker.add_resource("Batteries", 20, "2027-03-01")
        self.tracker.add_resource("Matches", 5)
        output = self.tracker.list_resources()
        self.assertEqual(len(output), 2)
        self.assertIn("Batteries: Qty 20, Expires: 2027-03-01", self._get_printed_output())
        self.assertIn("Matches: Qty 5, No Expiry", self._get_printed_output())

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('tracker.datetime') # Mock rationale: Control the current date for expiry checks.
    def test_get_expiring_resources(self, mock_datetime, mock_exists, mock_file_open):
        today = datetime(2024, 1, 1).date()
        mock_datetime.now.return_value = datetime(2024, 1, 1)
        mock_datetime.strptime = datetime.strptime # Keep original strptime
        mock_datetime.timedelta = timedelta # Keep original timedelta
        mock_datetime.date = today # For comparison

        self.tracker.add_resource("Food Rations", 5, (today + timedelta(days=10)).strftime(DATE_FORMAT))
        self.tracker.add_resource("Water Purifier", 1, (today + timedelta(days=60)).strftime(DATE_FORMAT))
        self.tracker.add_resource("Long Term Storage", 10, (today + timedelta(days=365)).strftime(DATE_FORMAT))

        expiring = self.tracker.get_expiring_resources(days=30)
        self.assertEqual(len(expiring), 1)
        self.assertEqual(expiring[0]['name'], "food rations")
        self.assertIn("Food Rations: Qty 5", self._get_printed_output())
        self.assertNotIn("Water Purifier", self._get_printed_output()) # 60 days is outside 30-day window

        self.mock_stdout = StringIO() # Reset stdout for next check
        sys.stdout = self.mock_stdout
        expiring_60 = self.tracker.get_expiring_resources(days=60)
        self.assertEqual(len(expiring_60), 2)
        self.assertIn("Food Rations", self._get_printed_output())
        self.assertIn("Water Purifier", self._get_printed_output())

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_get_low_stock_resources(self, mock_exists, mock_file_open):
        # Mock rationale: Prevent actual file I/O during low stock checks.
        self.tracker.add_resource("Medical Supplies", 2)
        self.tracker.add_resource("Ammunition", 10)
        self.tracker.add_resource("Fuel", 4)

        low_stock = self.tracker.get_low_stock_resources(threshold=5)
        self.assertEqual(len(low_stock), 2)
        self.assertIn("medical supplies", [r['name'] for r in low_stock])
        self.assertIn("fuel", [r['name'] for r in low_stock])
        self.assertIn("Medical Supplies: Qty 2", self._get_printed_output())
        self.assertIn("Fuel: Qty 4", self._get_printed_output())
        self.assertNotIn("Ammunition", self._get_printed_output())

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_add_existing_resource_fails(self, mock_exists, mock_file_open):
        # Mock rationale: Prevent actual file I/O during resource addition.
        self.tracker.add_resource("Canned Goods", 5)
        result = self.tracker.add_resource("Canned Goods", 10) # Try to add again
        self.assertFalse(result)
        self.assertEqual(self.tracker.resources["canned goods"]["quantity"], 5) # Quantity should not change
        self.assertIn("Resource 'canned goods' already exists. Use 'update' to modify.", self._get_printed_output())
        self.assertEqual(mock_file_open().write.call_count, 1) # Only initial add should save

if __name__ == '__main__':
    unittest.main()
