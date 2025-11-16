import unittest
import sys
from unittest.mock import patch
from io import StringIO
from src.sorter import categorize_item, sort_inventory, main, CATEGORIES
from typing import List, Dict

class TestApocalypseSnackSorter(unittest.TestCase):

    def test_categorize_item_long_term(self):
        # Test items expected to be categorized as 'Long-Term Survival'
        self.assertEqual(categorize_item("Canned Beans"), "Long-Term Survival")
        self.assertEqual(categorize_item("Dried Pasta"), "Long-Term Survival")
        self.assertEqual(categorize_item("Rice Bag"), "Long-Term Survival")
        self.assertEqual(categorize_item("MRE - Beef Stew"), "Long-Term Survival")
        self.assertEqual(categorize_item("Water Purification Tablets"), "Long-Term Survival")
        self.assertEqual(categorize_item("Salt Block"), "Long-Term Survival")
        self.assertEqual(categorize_item("Honey Jar"), "Long-Term Survival")
        self.assertEqual(categorize_item("Powdered Milk"), "Long-Term Survival")

    def test_categorize_item_morale_boost(self):
        # Test items expected to be categorized as 'Short-Term Morale Boost'
        self.assertEqual(categorize_item("Chocolate Bar"), "Short-Term Morale Boost")
        self.assertEqual(categorize_item("Coffee Grounds"), "Short-Term Morale Boost")
        self.assertEqual(categorize_item("Bag of Chips"), "Short-Term Morale Boost")
        self.assertEqual(categorize_item("Spices Mix"), "Short-Term Morale Boost")
        self.assertEqual(categorize_item("Can of Soda"), "Short-Term Morale Boost")
        self.assertEqual(categorize_item("Whiskey Bottle"), "Short-Term Morale Boost") # 'alcohol' keyword
        self.assertEqual(categorize_item("Sweet Candy"), "Short-Term Morale Boost")

    def test_categorize_item_immediate_consumption(self):
        # Test items expected to be categorized as 'Immediate Consumption'
        self.assertEqual(categorize_item("Fresh Apples"), "Immediate Consumption")
        self.assertEqual(categorize_item("Milk Carton"), "Immediate Consumption")
        self.assertEqual(categorize_item("Raw Meat"), "Immediate Consumption")
        self.assertEqual(categorize_item("Loaf of Bread"), "Immediate Consumption")
        self.assertEqual(categorize_item("Yogurt Cup"), "Immediate Consumption")
        self.assertEqual(categorize_item("Fresh Berries"), "Immediate Consumption")
        self.assertEqual(categorize_item("Green Leafy Vegetables"), "Immediate Consumption")

    def test_categorize_item_uncategorized(self):
        # Test items that should not match any category
        self.assertEqual(categorize_item("Hammer"), "Uncategorized")
        self.assertEqual(categorize_item("Radio"), "Uncategorized")
        self.assertEqual(categorize_item("Empty Can"), "Uncategorized")
        self.assertEqual(categorize_item("Unknown Goo"), "Uncategorized")

    def test_sort_inventory_mixed_items(self):
        # Test sorting a list of mixed items
        items = [
            "Canned Peaches",
            "Fresh Strawberries",
            "Coffee Beans",
            "Dried Fruit",
            "Mystery Can (Unlabeled)",
            "Fresh Fish",
            "Chocolate Cookies"
        ]
        expected_sorted: Dict[str, List[str]] = {
            "Long-Term Survival": ["Canned Peaches", "Dried Fruit"],
            "Short-Term Morale Boost": ["Coffee Beans", "Chocolate Cookies"],
            "Immediate Consumption": ["Fresh Strawberries", "Fresh Fish"],
            "Uncategorized": ["Mystery Can (Unlabeled)"]
        }
        # Ensure all expected categories are present, even if empty in the test case
        for cat in CATEGORIES.keys():
            if cat not in expected_sorted:
                expected_sorted[cat] = []

        result = sort_inventory(items)
        # Sort lists within categories for consistent comparison
        for category in result:
            result[category].sort()
        for category in expected_sorted:
            expected_sorted[category].sort()

        self.assertDictEqual(result, expected_sorted)

    def test_sort_inventory_empty_list(self):
        # Test sorting an empty list
        items: List[str] = []
        expected_sorted: Dict[str, List[str]] = {
            "Long-Term Survival": [],
            "Short-Term Morale Boost": [],
            "Immediate Consumption": [],
            "Uncategorized": []
        }
        for cat in CATEGORIES.keys():
            if cat not in expected_sorted:
                expected_sorted[cat] = []
        
        result = sort_inventory(items)
        self.assertDictEqual(result, expected_sorted)

    def test_main_function_output(self):
        # Mock rationale: We need to capture stdout to verify the main function's print output.
        # We also need to mock sys.argv to simulate command-line arguments.
        test_args = ["sorter.py", "Canned Soup", "Fresh Bread", "Candy Bar", "Water Bottle"]
        
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            with patch('sys.argv', test_args):
                main()
                output = mock_stdout.getvalue()

        self.assertIn("--- Apocalypse Snack Inventory ---", output)
        self.assertIn("Long-Term Survival:", output)
        self.assertIn("  - Canned Soup", output)
        self.assertIn("Short-Term Morale Boost:", output)
        self.assertIn("  - Candy Bar", output)
        self.assertIn("Immediate Consumption:", output)
        self.assertIn("  - Fresh Bread", output)
        self.assertIn("Uncategorized:", output)
        self.assertIn("  - Water Bottle", output) # Water bottle is not explicitly categorized by current rules

    def test_main_function_no_args(self):
        # Mock rationale: We need to capture stdout and stderr to verify the main function's
        # error message and exit code when no arguments are provided.
        test_args = ["sorter.py"]
        
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            with patch('sys.stderr', new=StringIO()) as mock_stderr:
                with patch('sys.argv', test_args):
                    with self.assertRaises(SystemExit) as cm:
                        main()
                    self.assertEqual(cm.exception.code, 1) # Expect exit code 1 for error

                output = mock_stdout.getvalue()
                err_output = mock_stderr.getvalue() # In this case, main prints to stdout for usage

        self.assertIn("Usage: python src/sorter.py \"Item 1\" \"Item 2\" ...", output)
        self.assertEqual(err_output, "") # No stderr output for this specific case, it prints to stdout

if __name__ == '__main__':
    unittest.main()
