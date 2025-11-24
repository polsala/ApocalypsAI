import unittest
from unittest.mock import patch, mock_open
import json
import os
from datetime import date, timedelta

# Mock rationale: We need to simulate file system operations (reading/writing hoard.json)
# and control the current date for expiry checks without actually touching the disk
# or relying on the system's clock, ensuring deterministic and isolated tests.

# Import functions from the manager script using relative import
from ..src.manager import load_hoard, save_hoard, add_item, remove_item, list_items, check_expiries, HOARD_FILE, EXPIRY_WARNING_DAYS

class TestResourceHoardManager(unittest.TestCase):

    def setUp(self):
        # Reset mocks before each test if necessary, though patch decorators handle most of it.
        pass

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_hoard_existing(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing hoard file with valid JSON content.
        mock_exists.return_value = True
        mock_json_load.return_value = {'Water': {'quantity': 5, 'expiry': None}}
        hoard = load_hoard()
        self.assertEqual(hoard, {'Water': {'quantity': 5, 'expiry': None}})
        mock_exists.assert_called_once_with(HOARD_FILE)
        mock_open_file.assert_called_once_with(HOARD_FILE, 'r')

    @patch('os.path.exists')
    @patch('builtins.print') # Mock rationale: Capture warning message for corrupted file.
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=json.JSONDecodeError('Expecting value', '', 0))
    def test_load_hoard_corrupted(self, mock_json_load, mock_open_file, mock_print, mock_exists):
        # Mock rationale: Simulate an existing hoard file that is corrupted (invalid JSON).
        mock_exists.return_value = True
        hoard = load_hoard()
        self.assertEqual(hoard, {})
        mock_print.assert_called_once_with(f"Warning: '{HOARD_FILE}' is corrupted or empty. Starting with an empty hoard.")

    @patch('os.path.exists')
    def test_load_hoard_new(self, mock_exists):
        # Mock rationale: Simulate no existing hoard file.
        mock_exists.return_value = False
        hoard = load_hoard()
        self.assertEqual(hoard, {})
        mock_exists.assert_called_once_with(HOARD_FILE)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_hoard(self, mock_json_dump, mock_open_file):
        # Mock rationale: Simulate saving hoard data to a file.
        hoard = {'Food': {'quantity': 10, 'expiry': '2024-12-31'}}
        save_hoard(hoard)
        mock_open_file.assert_called_once_with(HOARD_FILE, 'w')
        mock_json_dump.assert_called_once_with(hoard, mock_open_file(), indent=4)

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_add_item_new(self, mock_print):
        # Mock rationale: Test adding a new item to an empty hoard.
        hoard = {}
        add_item(hoard, 'Bandages', 5, '2025-01-01')
        self.assertEqual(hoard, {'Bandages': {'quantity': 5, 'expiry': '2025-01-01'}})
        mock_print.assert_called_once_with("Added 5 of 'Bandages'. Current quantity: 5")

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_add_item_existing(self, mock_print):
        # Mock rationale: Test adding more quantity to an existing item.
        hoard = {'Bandages': {'quantity': 5, 'expiry': '2025-01-01'}}
        add_item(hoard, 'Bandages', 3)
        self.assertEqual(hoard, {'Bandages': {'quantity': 8, 'expiry': '2025-01-01'}})
        mock_print.assert_called_once_with("Added 3 of 'Bandages'. Current quantity: 8")

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_add_item_invalid_expiry(self, mock_print):
        # Mock rationale: Test adding an item with an invalid expiry date format.
        hoard = {}
        add_item(hoard, 'Medkit', 1, 'invalid-date')
        self.assertEqual(hoard, {'Medkit': {'quantity': 1, 'expiry': None}})
        mock_print.assert_any_call("Warning: Invalid expiry date format for 'Medkit'. Expected YYYY-MM-DD. Not setting expiry.")
        mock_print.assert_any_call("Added 1 of 'Medkit'. Current quantity: 1")

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_add_item_zero_quantity(self, mock_print):
        # Mock rationale: Test adding an item with zero quantity.
        hoard = {}
        add_item(hoard, 'Rope', 0)
        self.assertEqual(hoard, {})
        mock_print.assert_called_once_with("Error: Quantity to add for 'Rope' must be positive.")

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_remove_item_full(self, mock_print):
        # Mock rationale: Test removing all quantity of an item.
        hoard = {'Ammo': {'quantity': 10, 'expiry': None}}
        remove_item(hoard, 'Ammo', 10)
        self.assertEqual(hoard, {})
        mock_print.assert_called_once_with("Removed all 10 of 'Ammo'. Item removed from hoard.")

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_remove_item_partial(self, mock_print):
        # Mock rationale: Test removing part of the quantity of an item.
        hoard = {'Ammo': {'quantity': 10, 'expiry': None}}
        remove_item(hoard, 'Ammo', 3)
        self.assertEqual(hoard, {'Ammo': {'quantity': 7, 'expiry': None}})
        mock_print.assert_called_once_with("Removed 3 of 'Ammo'. Current quantity: 7")

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_remove_item_not_found(self, mock_print):
        # Mock rationale: Test removing an item that doesn't exist.
        hoard = {'Food': {'quantity': 5, 'expiry': None}}
        remove_item(hoard, 'Water', 1)
        self.assertEqual(hoard, {'Food': {'quantity': 5, 'expiry': None}})
        mock_print.assert_called_once_with("Error: 'Water' not found in hoard.")

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_remove_item_zero_quantity(self, mock_print):
        # Mock rationale: Test removing an item with zero quantity.
        hoard = {'Food': {'quantity': 5, 'expiry': None}}
        remove_item(hoard, 'Food', 0)
        self.assertEqual(hoard, {'Food': {'quantity': 5, 'expiry': None}})
        mock_print.assert_called_once_with("Error: Quantity to remove for 'Food' must be positive.")

    @patch('builtins.print')
    def test_list_items_empty(self, mock_print):
        # Mock rationale: Test listing an empty hoard.
        hoard = {}
        list_items(hoard)
        mock_print.assert_called_once_with("Your hoard is currently empty. Time to scavenge!")

    @patch('builtins.print')
    def test_list_items_populated(self, mock_print):
        # Mock rationale: Test listing a hoard with items.
        hoard = {
            'Canned Food': {'quantity': 10, 'expiry': '2025-12-31'},
            'Water Bottles': {'quantity': 20, 'expiry': None}
        }
        list_items(hoard)
        expected_calls = [
            unittest.mock.call("\n--- Current Hoard Inventory ---"),
            unittest.mock.call("- Canned Food: 10 (Expires: 2025-12-31)"),
            unittest.mock.call("- Water Bottles: 20"),
            unittest.mock.call("-------------------------------\n")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=True)

    @patch('builtins.print')
    def test_check_expiries_none_expiring(self, mock_print):
        # Mock rationale: Simulate a hoard where no items are expiring soon.
        hoard = {
            'Long-lasting MREs': {'quantity': 5, 'expiry': '2030-01-01'},
            'Water Filters': {'quantity': 2, 'expiry': None}
        }
        # Mock current date to be far from expiry
        mock_current_date = date(2024, 1, 1)
        check_expiries(hoard, current_date=mock_current_date)
        mock_print.assert_called_once_with("No items are expiring soon. Your hoard is secure for now!")

    @patch('builtins.print')
    def test_check_expiries_some_expiring(self, mock_print):
        # Mock rationale: Simulate a hoard with items expiring soon.
        hoard = {
            'Short-term Rations': {'quantity': 3, 'expiry': '2024-02-15'},
            'Long-lasting MREs': {'quantity': 5, 'expiry': '2030-01-01'},
            'Medkits': {'quantity': 1, 'expiry': '2024-03-01'}
        }
        # Mock current date to catch items expiring within EXPIRY_WARNING_DAYS (30 days)
        mock_current_date = date(2024, 1, 20) # 2024-01-20
        # Rations expire 2024-02-15 (26 days away) -> should be caught
        # Medkits expire 2024-03-01 (41 days away) -> should NOT be caught

        check_expiries(hoard, current_date=mock_current_date)
        expected_calls = [
            unittest.mock.call(f"\n--- Items Expiring Within {EXPIRY_WARNING_DAYS} Days ---"),
            unittest.mock.call("- Short-term Rations: 3 (Expires: 2024-02-15)"),
            unittest.mock.call("-------------------------------------------\n")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=True)
        # Ensure Medkits are NOT printed
        self.assertNotIn("- Medkits: 1 (Expires: 2024-03-01)", [call.args[0] for call in mock_print.call_args_list])

    @patch('builtins.print')
    def test_check_expiries_malformed_date(self, mock_print):
        # Mock rationale: Test handling of malformed expiry dates during check.
        hoard = {
            'Corrupted Data': {'quantity': 1, 'expiry': 'bad-date'}
        }
        mock_current_date = date(2024, 1, 1)
        check_expiries(hoard, current_date=mock_current_date)
        mock_print.assert_any_call("Warning: Malformed expiry date for 'Corrupted Data': bad-date. Skipping expiry check.")
        mock_print.assert_any_call("No items are expiring soon. Your hoard is secure for now!")

if __name__ == '__main__':
    unittest.main()
