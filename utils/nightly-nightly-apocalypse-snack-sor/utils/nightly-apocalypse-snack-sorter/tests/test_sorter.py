import unittest
from unittest.mock import patch, mock_open
import sys
import io
from src.sorter import FoodItem, parse_food_items, sort_food_items, print_items

class TestApocalypseSnackSorter(unittest.TestCase):

    def setUp(self):
        # Capture stdout/stderr for testing print_items and error messages
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = self._captured_stdout = io.StringIO()
        sys.stderr = self._captured_stderr = io.StringIO()

    def tearDown(self):
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

    def test_parse_food_items_valid_csv(self):
        # Mock rationale: Simulates reading a CSV file without actual file I/O.
        mock_csv_content = (
            "Item Name,Shelf Life (days),Calories per serving,Category\n"
            "Canned Beans,1825,200,Canned\n"
            "Rice,3650,130,Dry Goods\n"
            "MRE,1825,1200,Prepared Meal"
        )
        with patch('builtins.open', mock_open(read_data=mock_csv_content)) as mock_file:
            items = parse_food_items("dummy.csv")
            self.assertEqual(len(items), 3)
            self.assertEqual(items[0], FoodItem("Canned Beans", 1825, 200, "Canned"))
            self.assertEqual(items[1], FoodItem("Rice", 3650, 130, "Dry Goods"))
            self.assertEqual(items[2], FoodItem("MRE", 1825, 1200, "Prepared Meal"))
            mock_file.assert_called_with("dummy.csv", 'r', newline='', encoding='utf-8')

    def test_parse_food_items_file_not_found(self):
        # Mock rationale: Simulates a FileNotFoundError without needing to create/delete files.
        with patch('builtins.open', side_effect=FileNotFoundError) as mock_file:
            with self.assertRaises(SystemExit) as cm:
                parse_food_items("non_existent.csv")
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Input file 'non_existent.csv' not found.", self._captured_stderr.getvalue())

    def test_parse_food_items_malformed_row(self):
        # Mock rationale: Tests error handling for malformed CSV rows.
        mock_csv_content = (
            "Item Name,Shelf Life (days),Calories per serving,Category\n"
            "Canned Beans,1825,200,Canned\n"
            "Bad Row,100\n"
            "Rice,3650,130,Dry Goods"
        )
        with patch('builtins.open', mock_open(read_data=mock_csv_content)):
            items = parse_food_items("dummy.csv")
            self.assertEqual(len(items), 2) # Only valid rows should be parsed
            self.assertIn("Warning: Skipping malformed row 3", self._captured_stderr.getvalue())
            self.assertEqual(items[0], FoodItem("Canned Beans", 1825, 200, "Canned"))
            self.assertEqual(items[1], FoodItem("Rice", 3650, 130, "Dry Goods"))

    def test_parse_food_items_value_error_in_row(self):
        # Mock rationale: Tests error handling for non-integer shelf life/calories.
        mock_csv_content = (
            "Item Name,Shelf Life (days),Calories per serving,Category\n"
            "Canned Beans,1825,200,Canned\n"
            "Invalid Shelf Life,abc,100,Snack\n"
            "Invalid Calories,100,def,Snack"
        )
        with patch('builtins.open', mock_open(read_data=mock_csv_content)):
            items = parse_food_items("dummy.csv")
            self.assertEqual(len(items), 1)
            self.assertIn("Warning: Skipping row 3 due to data conversion error", self._captured_stderr.getvalue())
            self.assertIn("Warning: Skipping row 4 due to data conversion error", self._captured_stderr.getvalue())
            self.assertEqual(items[0], FoodItem("Canned Beans", 1825, 200, "Canned"))

    def test_sort_food_items(self):
        items = [
            FoodItem("Chocolate Bar", 365, 250, "Snack"),
            FoodItem("MRE", 1825, 1200, "Prepared Meal"),
            FoodItem("Canned Beans", 1825, 200, "Canned"),
            FoodItem("Rice", 3650, 130, "Dry Goods"),
            FoodItem("Water Bottle", 365, 0, "Beverage"),
            FoodItem("Dried Fruit", 730, 100, "Snack"),
        ]
        expected_sorted_items = [
            FoodItem("Rice", 3650, 130, "Dry Goods"),
            FoodItem("MRE", 1825, 1200, "Prepared Meal"),
            FoodItem("Canned Beans", 1825, 200, "Canned"),
            FoodItem("Dried Fruit", 730, 100, "Snack"),
            FoodItem("Chocolate Bar", 365, 250, "Snack"),
            FoodItem("Water Bottle", 365, 0, "Beverage"),
        ]
        self.assertEqual(sort_food_items(items), expected_sorted_items)

    def test_print_items_to_stdout(self):
        items = [
            FoodItem("Rice", 3650, 130, "Dry Goods"),
            FoodItem("MRE", 1825, 1200, "Prepared Meal"),
        ]
        print_items(items)
        output = self._captured_stdout.getvalue()
        self.assertIn("Sorted Supplies:", output)
        self.assertIn("Rice", output)
        self.assertIn("MRE", output)
        self.assertIn("3650", output)
        self.assertIn("1200", output)

    def test_print_items_to_file(self):
        # Mock rationale: Simulates writing to an output CSV file without actual file I/O.
        items = [
            FoodItem("Rice", 3650, 130, "Dry Goods"),
            FoodItem("MRE", 1825, 1200, "Prepared Meal"),
        ]
        mock_output_file_content = io.StringIO()
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.return_value.__enter__.return_value = mock_output_file_content
            print_items(items, "output.csv")
            
            mock_file.assert_called_with("output.csv", 'w', newline='', encoding='utf-8')
            output_content = mock_output_file_content.getvalue()
            self.assertIn("Item Name,Shelf Life,Calories,Category", output_content)
            self.assertIn("Rice,3650,130,Dry Goods", output_content)
            self.assertIn("MRE,1825,1200,Prepared Meal", output_content)
            self.assertIn("Sorted supplies written to 'output.csv'.", self._captured_stdout.getvalue())

    def test_main_function_stdout(self):
        # Mock rationale: Simulates command-line arguments and file input/output for an end-to-end test.
        mock_csv_content = (
            "Item Name,Shelf Life (days),Calories per serving,Category\n"
            "Canned Beans,1825,200,Canned\n"
            "Rice,3650,130,Dry Goods"
        )
        with patch('argparse.ArgumentParser.parse_args') as mock_args,
             patch('builtins.open', mock_open(read_data=mock_csv_content)):
            mock_args.return_value.input = "input.csv"
            mock_args.return_value.output = None

            from src.sorter import main
            main()

            output = self._captured_stdout.getvalue()
            self.assertIn("Rice", output)
            self.assertIn("Canned Beans", output)
            self.assertNotIn("Sorted supplies written to", output)

    def test_main_function_file_output(self):
        # Mock rationale: Simulates command-line arguments and file input/output for an end-to-end test.
        mock_csv_content = (
            "Item Name,Shelf Life (days),Calories per serving,Category\n"
            "Canned Beans,1825,200,Canned\n"
            "Rice,3650,130,Dry Goods"
        )
        mock_output_file_content = io.StringIO()
        with patch('argparse.ArgumentParser.parse_args') as mock_args,
             patch('builtins.open', mock_open(read_data=mock_csv_content)) as mock_file_open:
            mock_file_open.return_value.__enter__.return_value = mock_output_file_content # For the output file
            mock_args.return_value.input = "input.csv"
            mock_args.return_value.output = "output.csv"

            from src.sorter import main
            main()

            output_content = mock_output_file_content.getvalue()
            self.assertIn("Item Name,Shelf Life,Calories,Category", output_content)
            self.assertIn("Rice,3650,130,Dry Goods", output_content)
            self.assertIn("Canned Beans,1825,200,Canned", output_content)
            self.assertIn("Sorted supplies written to 'output.csv'.", self._captured_stdout.getvalue())

    def test_main_no_items_found(self):
        # Mock rationale: Simulates an empty or invalid input file.
        mock_csv_content = (
            "Item Name,Shelf Life (days),Calories per serving,Category\n"
            "Bad Row,100\n"
        )
        with patch('argparse.ArgumentParser.parse_args') as mock_args,
             patch('builtins.open', mock_open(read_data=mock_csv_content)):
            mock_args.return_value.input = "empty.csv"
            mock_args.return_value.output = None

            with self.assertRaises(SystemExit) as cm:
                from src.sorter import main
                main()
            self.assertEqual(cm.exception.code, 2) # Exit code 2 for no-op (nothing to change/sort)
            self.assertIn("No valid food items found to sort.", self._captured_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
