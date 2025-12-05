import unittest
import os
import sys
import io
from unittest.mock import patch, mock_open

# Add the src directory to the Python path to allow importing sorter.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from sorter import categorize_item, read_items_from_file, main

class TestApocalypseSnackSorter(unittest.TestCase):

    def test_categorize_item_shelf_stability(self):
        self.assertEqual(categorize_item("Canned Beans")["shelf_stability"], "Long-Haul")
        self.assertEqual(categorize_item("Dried Apricots")["shelf_stability"], "Long-Haul")
        self.assertEqual(categorize_item("Rice")["shelf_stability"], "Long-Haul")
        self.assertEqual(categorize_item("Pasta")["shelf_stability"], "Long-Haul")
        self.assertEqual(categorize_item("Honey")["shelf_stability"], "Long-Haul")
        self.assertEqual(categorize_item("Salt")["shelf_stability"], "Long-Haul")
        self.assertEqual(categorize_item("Beef Jerky")["shelf_stability"], "Long-Haul")
        self.assertEqual(categorize_item("Sugar")["shelf_stability"], "Long-Haul")
        self.assertEqual(categorize_item("Flour")["shelf_stability"], "Long-Haul")
        self.assertEqual(categorize_item("Lentils")["shelf_stability"], "Long-Haul")
        self.assertEqual(categorize_item("Oats")["shelf_stability"], "Long-Haul")

        self.assertEqual(categorize_item("Potatoes")["shelf_stability"], "Mid-Term")
        self.assertEqual(categorize_item("Apples")["shelf_stability"], "Mid-Term")
        self.assertEqual(categorize_item("Hard Cheese")["shelf_stability"], "Mid-Term")
        self.assertEqual(categorize_item("Crackers")["shelf_stability"], "Mid-Term")
        self.assertEqual(categorize_item("Nuts")["shelf_stability"], "Mid-Term")
        self.assertEqual(categorize_item("Chocolate Bar")["shelf_stability"], "Mid-Term")
        self.assertEqual(categorize_item("Coffee")["shelf_stability"], "Mid-Term")
        self.assertEqual(categorize_item("Chips")["shelf_stability"], "Mid-Term")
        self.assertEqual(categorize_item("Bottled Water")["shelf_stability"], "Mid-Term")
        self.assertEqual(categorize_item("Tea Bags")["shelf_stability"], "Mid-Term")
        self.assertEqual(categorize_item("Jam")["shelf_stability"], "Mid-Term")

        self.assertEqual(categorize_item("Fresh Milk")["shelf_stability"], "Perishable Panic")
        self.assertEqual(categorize_item("Bread")["shelf_stability"], "Perishable Panic")
        self.assertEqual(categorize_item("Fresh Strawberries")["shelf_stability"], "Perishable Panic")
        self.assertEqual(categorize_item("Raw Meat")["shelf_stability"], "Perishable Panic")
        self.assertEqual(categorize_item("Yogurt")["shelf_stability"], "Perishable Panic")
        self.assertEqual(categorize_item("Eggs")["shelf_stability"], "Perishable Panic")
        self.assertEqual(categorize_item("Fresh Fish")["shelf_stability"], "Perishable Panic")
        self.assertEqual(categorize_item("Dairy Cream")["shelf_stability"], "Perishable Panic")

        self.assertEqual(categorize_item("Unknown Item")["shelf_stability"], "Unknown Stability") # Default if no match
        self.assertEqual(categorize_item("Water")["shelf_stability"], "Unknown Stability") # Default if no match

    def test_categorize_item_comfort_level(self):
        self.assertEqual(categorize_item("Dark Chocolate")["comfort_level"], "Soul Soother")
        self.assertEqual(categorize_item("Instant Coffee")["comfort_level"], "Soul Soother")
        self.assertEqual(categorize_item("Herbal Tea")["comfort_level"], "Soul Soother")
        self.assertEqual(categorize_item("Cookies")["comfort_level"], "Soul Soother")
        self.assertEqual(categorize_item("Ice Cream")["comfort_level"], "Soul Soother")
        self.assertEqual(categorize_item("Hot Cocoa Mix")["comfort_level"], "Soul Soother")

        self.assertEqual(categorize_item("Potato Chips")["comfort_level"], "Morale Booster")
        self.assertEqual(categorize_item("Cola Soda")["comfort_level"], "Morale Booster")
        self.assertEqual(categorize_item("Gummy Bears Candy")["comfort_level"], "Morale Booster")
        self.assertEqual(categorize_item("Donuts")["comfort_level"], "Morale Booster")
        self.assertEqual(categorize_item("Popcorn")["comfort_level"], "Morale Booster")

        self.assertEqual(categorize_item("Canned Tuna")["comfort_level"], "Pure Sustenance") # Default if no match
        self.assertEqual(categorize_item("Rice")["comfort_level"], "Pure Sustenance") # Default if no match

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_read_items_from_file_success(self, mock_file_open, mock_exists):
        # Mock rationale: We need to simulate file existence and content without actually creating files.
        # `os.path.exists` is mocked to return True, and `builtins.open` is mocked to return a file-like object
        # with predefined content, ensuring deterministic and offline testing.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = "Canned Beans\nFresh Apples\nChocolate Bar\n"
        
        items = read_items_from_file("dummy_path.txt")
        self.assertEqual(items, ["Canned Beans", "Fresh Apples", "Chocolate Bar"])
        mock_file_open.assert_called_once_with("dummy_path.txt", 'r', encoding='utf-8')

    @patch('os.path.exists')
    def test_read_items_from_file_not_found(self, mock_exists):
        # Mock rationale: Simulate a non-existent file to test error handling without actual file system interaction.
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            read_items_from_file("non_existent_file.txt")

    @patch('sys.argv', ['sorter.py', 'test_input.txt'])
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_success(self, mock_stdout, mock_exists, mock_file_open):
        # Mock rationale: Simulate command-line arguments, file existence, file content, and stdout capture.
        # This allows testing the full `main` function flow deterministically and offline.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = "Canned Beans\nChocolate Bar\nWater\n"
        
        main()
        output = mock_stdout.getvalue()
        self.assertIn("--- Canned Beans ---", output)
        self.assertIn("Shelf Stability: Long-Haul", output)
        self.assertIn("Comfort Level: Pure Sustenance", output)
        self.assertIn("--- Chocolate Bar ---", output)
        self.assertIn("Shelf Stability: Mid-Term", output)
        self.assertIn("Comfort Level: Soul Soother", output)
        self.assertIn("--- Water ---", output)
        self.assertIn("Shelf Stability: Unknown Stability", output)
        self.assertIn("Comfort Level: Pure Sustenance", output)

    @patch('sys.argv', ['sorter.py'])
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_no_args(self, mock_exit, mock_stdout):
        # Mock rationale: Simulate missing command-line arguments and capture stdout/exit behavior.
        # `sys.exit` is mocked to prevent the test runner from exiting prematurely.
        main()
        self.assertIn("Usage: python3 sorter.py <input_file_path>", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['sorter.py', 'non_existent.txt'])
    @patch('os.path.exists')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_file_not_found(self, mock_exit, mock_stdout, mock_exists):
        # Mock rationale: Simulate a non-existent input file for `main` and capture stdout/exit behavior.
        mock_exists.return_value = False
        main()
        self.assertIn("Error: Input file not found: non_existent.txt", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
