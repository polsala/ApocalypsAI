import unittest
from unittest.mock import patch, mock_open
import sys
from io import StringIO
from utils.nightly_apocalypse_snack_sorter.src.sorter import (
    calculate_priority_score,
    load_inventory,
    sort_inventory,
    print_sorted_inventory,
    main
)

class TestApocalypseSnackSorter(unittest.TestCase):

    def test_calculate_priority_score(self):
        # Test with standard valid input
        item = {
            'item_name': 'Canned Beans',
            'shelf_life_days': '365',
            'calories_per_serving': '150',
            'servings': '2'
        }
        # Expected: (365 * 1) - (150 * 2 * 0.01) = 365 - 3 = 362.0
        self.assertAlmostEqual(calculate_priority_score(item), 362.0)

        # Test with shorter shelf life, higher calories (higher priority)
        item = {
            'item_name': 'Crackers',
            'shelf_life_days': '60',
            'calories_per_serving': '100',
            'servings': '5'
        }
        # Expected: (60 * 1) - (100 * 5 * 0.01) = 60 - 5 = 55.0
        self.assertAlmostEqual(calculate_priority_score(item), 55.0)

        # Test with zero calories
        item = {
            'item_name': 'Bottled Water',
            'shelf_life_days': '730',
            'calories_per_serving': '0',
            'servings': '10'
        }
        # Expected: (730 * 1) - (0 * 10 * 0.01) = 730 - 0 = 730.0
        self.assertAlmostEqual(calculate_priority_score(item), 730.0)

        # Test with missing key (should return inf)
        item_missing_key = {
            'item_name': 'Invalid Item',
            'shelf_life_days': '100',
            'servings': '1'
        }
        self.assertEqual(calculate_priority_score(item_missing_key), float('inf'))

        # Test with non-integer values (should return inf)
        item_bad_value = {
            'item_name': 'Bad Item',
            'shelf_life_days': 'abc',
            'calories_per_serving': '100',
            'servings': '1'
        }
        self.assertEqual(calculate_priority_score(item_bad_value), float('inf'))

    @patch('builtins.open', new_callable=mock_open)
    def test_load_inventory_success(self, mock_file):
        # Mock rationale: We need to simulate reading a CSV file without actually touching the filesystem.
        # `mock_open` allows us to provide a string that acts as the file content.
        csv_content = (
            "item_name,shelf_life_days,calories_per_serving,servings\n"
            "Canned Tuna,365,150,2\n"
            "Protein Bar,90,250,1\n"
        )
        mock_file.return_value.read.return_value = csv_content
        mock_file.return_value.__enter__.return_value = StringIO(csv_content) # For DictReader

        inventory = load_inventory("dummy.csv")
        self.assertEqual(len(inventory), 2)
        self.assertEqual(inventory[0]['item_name'], 'Canned Tuna')
        self.assertEqual(inventory[1]['shelf_life_days'], '90')

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.stderr', new_callable=StringIO)
    def test_load_inventory_file_not_found(self, mock_stderr, mock_file):
        # Mock rationale: Simulate a FileNotFoundError without creating/deleting files.
        # `sys.stderr` is mocked to capture error output.
        with self.assertRaises(SystemExit) as cm:
            load_inventory("non_existent.csv")
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Inventory file 'non_existent.csv' not found.", mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stderr', new_callable=StringIO)
    def test_load_inventory_malformed_csv(self, mock_stderr, mock_file):
        # Mock rationale: Simulate a malformed CSV file to test error handling during parsing.
        # csv.DictReader handles extra fields by ignoring them, so this won't raise an error
        # unless we explicitly check for field count. For this utility, we'll let DictReader handle it.
        # Let's test a more fundamental error, like an unreadable file.
        mock_file.side_effect = Exception("Permission denied")
        with self.assertRaises(SystemExit) as cm:
            load_inventory("bad.csv")
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error reading CSV file 'bad.csv': Permission denied", mock_stderr.getvalue())


    def test_sort_inventory(self):
        inventory = [
            {'item_name': 'Canned Tuna', 'shelf_life_days': '365', 'calories_per_serving': '150', 'servings': '2'}, # Score: 362.0
            {'item_name': 'Protein Bar', 'shelf_life_days': '90', 'calories_per_serving': '250', 'servings': '1'},  # Score: 87.5
            {'item_name': 'Crackers', 'shelf_life_days': '60', 'calories_per_serving': '100', 'servings': '5'},    # Score: 55.0
            {'item_name': 'Bottled Water', 'shelf_life_days': '730', 'calories_per_serving': '0', 'servings': '10'}, # Score: 730.0
        ]
        sorted_items = sort_inventory(inventory)

        # Expected order: Crackers, Protein Bar, Canned Tuna, Bottled Water
        self.assertEqual(sorted_items[0]['item_name'], 'Crackers')
        self.assertAlmostEqual(sorted_items[0]['priority_score'], 55.0)
        self.assertEqual(sorted_items[1]['item_name'], 'Protein Bar')
        self.assertAlmostEqual(sorted_items[1]['priority_score'], 87.5)
        self.assertEqual(sorted_items[2]['item_name'], 'Canned Tuna')
        self.assertAlmostEqual(sorted_items[2]['priority_score'], 362.0)
        self.assertEqual(sorted_items[3]['item_name'], 'Bottled Water')
        self.assertAlmostEqual(sorted_items[3]['priority_score'], 730.0)

        # Test with an item that has malformed data (should be sorted last due to inf score)
        inventory_with_bad_item = inventory + [
            {'item_name': 'Bad Item', 'shelf_life_days': 'abc', 'calories_per_serving': '100', 'servings': '1'}
        ]
        sorted_items_with_bad = sort_inventory(inventory_with_bad_item)
        self.assertEqual(sorted_items_with_bad[-1]['item_name'], 'Bad Item')
        self.assertEqual(sorted_items_with_bad[-1]['priority_score'], float('inf'))


    @patch('sys.stdout', new_callable=StringIO)
    def test_print_sorted_inventory(self, mock_stdout):
        # Mock rationale: Capture stdout to verify the printed output format and content.
        sorted_inventory = [
            {'item_name': 'Crackers', 'shelf_life_days': '60', 'calories_per_serving': '100', 'servings': '5', 'priority_score': 55.0, 'total_calories': 500},
            {'item_name': 'Protein Bar', 'shelf_life_days': '90', 'calories_per_serving': '250', 'servings': '1', 'priority_score': 87.5, 'total_calories': 250},
        ]
        print_sorted_inventory(sorted_inventory)
        output = mock_stdout.getvalue()

        self.assertIn("Apocalypse Snack Sorter - Prioritized Consumption List", output)
        self.assertIn("Crackers", output)
        self.assertIn("55.00", output)
        self.assertIn("Protein Bar", output)
        self.assertIn("87.50", output)
        self.assertIn("Shelf Life (Days)", output)
        self.assertIn("Calories (Total)", output)
        self.assertIn("Priority Score", output)
        self.assertIn("*Lower Priority Score indicates higher consumption priority.*", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_empty_inventory(self, mock_stdout):
        # Mock rationale: Capture stdout to verify the message for empty inventory.
        print_sorted_inventory([])
        output = mock_stdout.getvalue()
        self.assertIn("No items to display.", output)

    @patch('sys.argv', ['sorter.py', 'test_inventory.csv'])
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_success(self, mock_stdout, mock_file):
        # Mock rationale: Simulate command-line arguments and file content for an end-to-end test of main().
        csv_content = (
            "item_name,shelf_life_days,calories_per_serving,servings\n"
            "Canned Tuna,365,150,2\n"
            "Crackers,60,100,5\n"
        )
        mock_file.return_value.read.return_value = csv_content
        mock_file.return_value.__enter__.return_value = StringIO(csv_content)

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Apocalypse Snack Sorter", output)
        self.assertIn("Crackers", output) # Crackers should be first due to higher priority
        self.assertIn("Canned Tuna", output)

    @patch('sys.argv', ['sorter.py'])
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_no_arguments(self, mock_stderr):
        # Mock rationale: Simulate running the script without arguments to test usage message and exit code.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Usage: python sorter.py <path_to_inventory.csv>", mock_stderr.getvalue())

    @patch('sys.argv', ['sorter.py', 'non_existent.csv'])
    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_file_not_found(self, mock_stderr, mock_file):
        # Mock rationale: Simulate a FileNotFoundError during main execution.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Inventory file 'non_existent.csv' not found.", mock_stderr.getvalue())

    @patch('sys.argv', ['sorter.py', 'empty.csv'])
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_empty_inventory_file(self, mock_stdout, mock_file):
        # Mock rationale: Simulate an empty CSV file.
        csv_content = "item_name,shelf_life_days,calories_per_serving,servings\n"
        mock_file.return_value.read.return_value = csv_content
        mock_file.return_value.__enter__.return_value = StringIO(csv_content)

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0) # Exit 0 for no items to display is acceptable
        self.assertIn("No valid items found in inventory.", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
