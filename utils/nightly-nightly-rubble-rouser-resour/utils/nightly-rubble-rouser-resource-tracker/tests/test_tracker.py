import unittest
from unittest.mock import patch, mock_open
import json
import os
from src.tracker import (
    load_resources, save_resources, add_resource, remove_resource,
    get_summary, get_low_stock_alerts, DATA_FILE
)

class TestResourceTracker(unittest.TestCase):

    def setUp(self):
        # Ensure DATA_FILE is clean for each test (for local runs, mocks prevent actual file creation)
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def tearDown(self):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_resources_empty(self, mock_file, mock_exists):
        # Mock rationale: Simulate the data file not existing.
        mock_exists.return_value = False
        resources = load_resources()
        self.assertEqual(resources, {})
        mock_exists.assert_called_once_with(DATA_FILE)
        mock_file.assert_not_called()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='{"Stash1": {"Water": 10}}')
    def test_load_resources_existing(self, mock_file, mock_exists):
        # Mock rationale: Simulate the data file existing with content.
        mock_exists.return_value = True
        resources = load_resources()
        self.assertEqual(resources, {"Stash1": {"Water": 10}})
        mock_exists.assert_called_once_with(DATA_FILE)
        mock_file.assert_called_once_with(DATA_FILE, 'r')

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_resources(self, mock_json_dump, mock_file):
        # Mock rationale: Simulate saving data to a file without actual disk I/O.
        test_data = {"Stash1": {"Food": 5}}
        save_resources(test_data)
        mock_file.assert_called_once_with(DATA_FILE, 'w')
        mock_json_dump.assert_called_once_with(test_data, mock_file(), indent=4)

    @patch('src.tracker.save_resources')
    @patch('src.tracker.load_resources', return_value={})
    def test_add_resource_new_stash_item(self, mock_load, mock_save):
        # Mock rationale: Isolate the add_resource logic from file I/O.
        result = add_resource("StashA", "Medkit", 2)
        self.assertEqual(result, "Added 2 of Medkit to StashA. New total: 2")
        mock_load.assert_called_once()
        mock_save.assert_called_once_with({"StashA": {"Medkit": 2}}, DATA_FILE)

    @patch('src.tracker.save_resources')
    @patch('src.tracker.load_resources', return_value={"StashB": {"Ammo": 10}})
    def test_add_resource_existing_item(self, mock_load, mock_save):
        # Mock rationale: Isolate the add_resource logic from file I/O.
        result = add_resource("StashB", "Ammo", 5)
        self.assertEqual(result, "Added 5 of Ammo to StashB. New total: 15")
        mock_load.assert_called_once()
        mock_save.assert_called_once_with({"StashB": {"Ammo": 15}}, DATA_FILE)

    @patch('src.tracker.save_resources')
    @patch('src.tracker.load_resources', return_value={"StashC": {"Rope": 5}})
    def test_remove_resource_partial(self, mock_load, mock_save):
        # Mock rationale: Isolate the remove_resource logic from file I/O.
        result = remove_resource("StashC", "Rope", 2)
        self.assertEqual(result, "Removed 2 of Rope from StashC. Remaining: 3")
        mock_load.assert_called_once()
        mock_save.assert_called_once_with({"StashC": {"Rope": 3}}, DATA_FILE)

    @patch('src.tracker.save_resources')
    @patch('src.tracker.load_resources', return_value={"StashD": {"Fuel": 3}})
    def test_remove_resource_all(self, mock_load, mock_save):
        # Mock rationale: Isolate the remove_resource logic from file I/O.
        result = remove_resource("StashD", "Fuel", 3)
        self.assertEqual(result, "Removed all 3 of Fuel from StashD.")
        mock_load.assert_called_once()
        mock_save.assert_called_once_with({}, DATA_FILE) # StashD should be removed if empty

    @patch('src.tracker.save_resources')
    @patch('src.tracker.load_resources', return_value={"StashE": {"Tools": 5}})
    def test_remove_resource_not_found_item(self, mock_load, mock_save):
        # Mock rationale: Isolate the remove_resource logic from file I/O.
        result = remove_resource("StashE", "Water", 1)
        self.assertEqual(result, "Error: Water not found in StashE.")
        mock_load.assert_called_once()
        mock_save.assert_not_called() # No change should be saved

    @patch('src.tracker.save_resources')
    @patch('src.tracker.load_resources', return_value={})
    def test_remove_resource_not_found_stash(self, mock_load, mock_save):
        # Mock rationale: Isolate the remove_resource logic from file I/O.
        result = remove_resource("StashF", "Food", 1)
        self.assertEqual(result, "Error: Food not found in StashF.")
        mock_load.assert_called_once()
        mock_save.assert_not_called() # No change should be saved

    @patch('src.tracker.load_resources', return_value={})
    def test_get_summary_empty(self, mock_load):
        # Mock rationale: Isolate the get_summary logic from file I/O.
        result = get_summary()
        self.assertEqual(result, "No resources tracked yet. Start adding some!")
        mock_load.assert_called_once()

    @patch('src.tracker.load_resources', return_value={
        "StashAlpha": {"Water": 10, "Food": 5},
        "StashBeta": {"Water": 3, "Medkit": 2}
    })
    def test_get_summary_with_data(self, mock_load):
        # Mock rationale: Isolate the get_summary logic from file I/O.
        expected_summary = (
            "--- Resource Summary ---\n"
            "\nStash: StashAlpha\n"
            "  - Water: 10\n"
            "  - Food: 5\n"
            "\nStash: StashBeta\n"
            "  - Water: 3\n"
            "  - Medkit: 2\n"
            "\n--- Global Totals ---\n"
            "  - Food: 5\n"
            "  - Medkit: 2\n"
            "  - Water: 13"
        )
        result = get_summary()
        self.assertEqual(result, expected_summary)
        mock_load.assert_called_once()

    @patch('src.tracker.load_resources', return_value={})
    def test_get_low_stock_alerts_empty(self, mock_load):
        # Mock rationale: Isolate the get_low_stock_alerts logic from file I/O.
        result = get_low_stock_alerts(5)
        self.assertEqual(result, "No resources tracked yet. No low stock alerts.")
        mock_load.assert_called_once()

    @patch('src.tracker.load_resources', return_value={
        "StashX": {"Water": 10, "Food": 3, "Ammo": 1},
        "StashY": {"Medkit": 2, "Fuel": 7}
    })
    def test_get_low_stock_alerts_with_data(self, mock_load):
        # Mock rationale: Isolate the get_low_stock_alerts logic from file I/O.
        expected_alerts = (
            "--- Low Stock Alerts ---\n"
            "LOW STOCK: Food in StashX has only 3 left (threshold: 5)\n"
            "LOW STOCK: Ammo in StashX has only 1 left (threshold: 5)\n"
            "LOW STOCK: Medkit in StashY has only 2 left (threshold: 5)"
        )
        result = get_low_stock_alerts(5)
        self.assertEqual(result, expected_alerts)
        mock_load.assert_called_once()

    @patch('src.tracker.load_resources', return_value={
        "StashZ": {"Water": 10, "Food": 8}
    })
    def test_get_low_stock_alerts_no_alerts(self, mock_load):
        # Mock rationale: Isolate the get_low_stock_alerts logic from file I/O.
        result = get_low_stock_alerts(5)
        self.assertEqual(result, "All resources are above the low stock threshold of 5.")
        mock_load.assert_called_once()

if __name__ == '__main__':
    unittest.main()
