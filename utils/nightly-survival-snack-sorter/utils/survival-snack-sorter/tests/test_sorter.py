import unittest
from unittest.mock import patch, mock_open
from datetime import date
import sys
import io
from src.sorter import load_inventory, sort_inventory, display_inventory, main

class TestSurvivalSnackSorter(unittest.TestCase):

    def setUp(self):
        self.mock_inventory_data = (
            "Canned Beans,2025-12-31,Food,10\n"
            "Water Bottle,2030-01-01,Drink,5\n"
            "First Aid Kit,2024-06-15,Medical,1\n"
            "MRE,2026-03-20,Food,7\n"
            "Bandages,2024-09-01,Medical,20\n"
        )
        self.expected_parsed_inventory = [
            {'item_name': 'Canned Beans', 'expiration_date': date(2025, 12, 31), 'category': 'Food', 'quantity': 10},
            {'item_name': 'Water Bottle', 'expiration_date': date(2030, 1, 1), 'category': 'Drink', 'quantity': 5},
            {'item_name': 'First Aid Kit', 'expiration_date': date(2024, 6, 15), 'category': 'Medical', 'quantity': 1},
            {'item_name': 'MRE', 'expiration_date': date(2026, 3, 20), 'category': 'Food', 'quantity': 7},
            {'item_name': 'Bandages', 'expiration_date': date(2024, 9, 1), 'category': 'Medical', 'quantity': 20},
        ]

    @patch('builtins.open', new_callable=mock_open)
    def test_load_inventory_success(self, mock_file):
        # Mock rationale: Simulates reading a valid inventory file without actual file I/O.
        mock_file.return_value.read.return_value = self.mock_inventory_data
        mock_file.return_value.__iter__.return_value = self.mock_inventory_data.splitlines()

        inventory = load_inventory('dummy_path.txt')
        self.assertEqual(inventory, self.expected_parsed_inventory)
        mock_file.assert_called_once_with('dummy_path.txt', 'r', newline='', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_load_inventory_malformed_line(self, mock_stderr, mock_file):
        # Mock rationale: Simulates reading a file with a malformed line and captures stderr output.
        malformed_data = "Item1,2025-01-01,Food,10\nMalformed Line\nItem3,2026-01-01,Drink,5"
        mock_file.return_value.read.return_value = malformed_data
        mock_file.return_value.__iter__.return_value = malformed_data.splitlines()

        inventory = load_inventory('dummy_path.txt')
        self.assertEqual(len(inventory), 2) # Only 2 valid items should be loaded
        self.assertIn("Warning: Skipping malformed line 2", mock_stderr.getvalue())

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_load_inventory_file_not_found(self, mock_exit, mock_stderr, mock_file):
        # Mock rationale: Simulates a FileNotFoundError and checks for correct error message and exit code.
        load_inventory('non_existent_file.txt')
        self.assertIn("Error: Inventory file not found", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    def test_sort_inventory_by_expiration(self):
        # Mock rationale: Tests the sorting logic directly with pre-parsed data.
        sorted_inventory = sort_inventory(self.expected_parsed_inventory, 'expiration')
        expected_order = [
            'First Aid Kit', 'Bandages', 'Canned Beans', 'MRE', 'Water Bottle'
        ]
        actual_order = [item['item_name'] for item in sorted_inventory]
        self.assertEqual(actual_order, expected_order)

    def test_sort_inventory_by_category(self):
        # Mock rationale: Tests the sorting logic directly with pre-parsed data.
        sorted_inventory = sort_inventory(self.expected_parsed_inventory, 'category')
        expected_order = [
            'Water Bottle', 'Canned Beans', 'MRE', 'Bandages', 'First Aid Kit'
        ]
        actual_order = [item['item_name'] for item in sorted_inventory]
        self.assertEqual(actual_order, expected_order)

    def test_sort_inventory_invalid_key(self):
        # Mock rationale: Tests error handling for invalid sort keys.
        with self.assertRaises(ValueError) as cm:
            sort_inventory(self.expected_parsed_inventory, 'invalid_key')
        self.assertIn("Invalid sort_key", str(cm.exception))

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_display_inventory(self, mock_stdout):
        # Mock rationale: Captures stdout to verify the formatted output of the display function.
        inventory_to_display = [
            {'item_name': 'MRE', 'expiration_date': date(2026, 3, 20), 'category': 'Food', 'quantity': 7},
            {'item_name': 'Canned Beans', 'expiration_date': date(2025, 12, 31), 'category': 'Food', 'quantity': 10},
        ]
        display_inventory(inventory_to_display, 'expiration')
        output = mock_stdout.getvalue()
        self.assertIn("--- Survival Inventory (Sorted by Expiration) ---", output)
        self.assertIn("Item Name           Expiration  Category  Quantity", output)
        self.assertIn("MRE                 2026-03-20  Food      7", output)
        self.assertIn("Canned Beans        2025-12-31  Food      10", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_display_inventory_empty(self, mock_stdout):
        # Mock rationale: Captures stdout to verify output for an empty inventory.
        display_inventory([], 'expiration')
        output = mock_stdout.getvalue()
        self.assertIn("No items in inventory.", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.sorter.load_inventory')
    @patch('src.sorter.sort_inventory')
    @patch('src.sorter.display_inventory')
    def test_main_function(self, mock_display, mock_sort, mock_load, mock_parse_args):
        # Mock rationale: Mocks CLI argument parsing and internal functions to test the main execution flow.
        mock_parse_args.return_value = argparse.Namespace(file='test.txt', sort_by='expiration')
        mock_load.return_value = self.expected_parsed_inventory
        mock_sort.return_value = self.expected_parsed_inventory # Assume sorted for this test

        main()

        mock_load.assert_called_once_with('test.txt')
        mock_sort.assert_called_once_with(self.expected_parsed_inventory, 'expiration')
        mock_display.assert_called_once_with(self.expected_parsed_inventory, 'expiration')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.sorter.load_inventory')
    @patch('src.sorter.sort_inventory')
    @patch('src.sorter.display_inventory')
    def test_main_function_empty_inventory(self, mock_display, mock_sort, mock_load, mock_parse_args):
        # Mock rationale: Mocks CLI argument parsing and internal functions to test the main execution flow with an empty inventory.
        mock_parse_args.return_value = argparse.Namespace(file='empty.txt', sort_by='expiration')
        mock_load.return_value = []

        main()

        mock_load.assert_called_once_with('empty.txt')
        mock_sort.assert_not_called() # Should not try to sort empty inventory
        mock_display.assert_called_once_with([], 'expiration') # Should still try to display empty inventory
