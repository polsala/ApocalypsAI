import unittest
from unittest.mock import patch, mock_open
import sys
import io
from src.sorter import Snack, parse_snacks_from_file, sort_snacks, print_prioritized_snacks

class TestSnackSorter(unittest.TestCase):

    def test_snack_comparison(self):
        # Test primary sort: shelf life (ascending)
        s1 = Snack("Short Life", 10, 100, 3)
        s2 = Snack("Long Life", 100, 100, 3)
        self.assertTrue(s1 < s2)

        # Test secondary sort: calories (descending) when shelf life is equal
        s3 = Snack("High Cal", 50, 200, 3)
        s4 = Snack("Low Cal", 50, 100, 3)
        self.assertTrue(s3 < s4) # High Cal should come before Low Cal

        # Test tertiary sort: comfort score (descending) when shelf life and calories are equal
        s5 = Snack("High Comfort", 20, 150, 5)
        s6 = Snack("Low Comfort", 20, 150, 2)
        self.assertTrue(s5 < s6) # High Comfort should come before Low Comfort

        # Test equality
        s7 = Snack("Same", 30, 120, 4)
        s8 = Snack("Same", 30, 120, 4)
        self.assertFalse(s7 < s8)
        self.assertFalse(s8 < s7)

    @patch('builtins.open', new_callable=mock_open)
    def test_parse_snacks_from_file_success(self, mock_file_open):
        # Mock rationale: We need to simulate reading from a file without actually creating one.
        # `mock_open` allows us to control the content returned by `open()`.
        mock_file_open.return_value.read.return_value = (
            "Fresh Apple,7,95,4\n"
            "Canned Beans,730,200,2\n"
            "MRE,1825,1200,3\n"
        )
        snacks = parse_snacks_from_file("dummy_snacks.txt")
        self.assertEqual(len(snacks), 3)
        self.assertEqual(snacks[0].name, "Fresh Apple")
        self.assertEqual(snacks[1].shelf_life_days, 730)
        self.assertEqual(snacks[2].calories, 1200)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_parse_snacks_from_file_invalid_lines(self, mock_stderr, mock_file_open):
        # Mock rationale: Simulate file content with errors and capture stderr output.
        mock_file_open.return_value.read.return_value = (
            "Valid Snack,10,100,3\n"
            "Invalid Line,10,abc,3\n" # Invalid calories
            "Another Invalid Line,10,100\n" # Missing comfort score
            "Comfort Out of Range,10,100,6\n" # Comfort score out of range
            "# This is a comment\n"
            "\n"
        )
        snacks = parse_snacks_from_file("dummy_snacks.txt")
        self.assertEqual(len(snacks), 1)
        self.assertEqual(snacks[0].name, "Valid Snack")
        error_output = mock_stderr.getvalue()
        self.assertIn("Warning: Could not parse line: 'Invalid Line,10,abc,3'. Skipping.", error_output)
        self.assertIn("Warning: Incorrect format for line: 'Another Invalid Line,10,100'. Skipping.", error_output)
        self.assertIn("Warning: Comfort score for 'Comfort Out of Range' out of range (1-5). Skipping.", error_output)

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_parse_snacks_from_file_not_found(self, mock_exit, mock_stderr, mock_file_open):
        # Mock rationale: Simulate a FileNotFoundError when `open()` is called and capture stderr/exit.
        parse_snacks_from_file("non_existent.txt")
        mock_exit.assert_called_with(1)
        self.assertIn("Error: Input file not found at 'non_existent.txt'", mock_stderr.getvalue())

    def test_sort_snacks(self):
        snacks = [
            Snack("MRE", 1825, 1200, 3),
            Snack("Fresh Apple", 7, 95, 4),
            Snack("Canned Beans", 730, 200, 2),
            Snack("Chocolate Bar", 365, 250, 5),
            Snack("Dried Fruit", 365, 150, 3),
        ]
        sorted_snacks = sort_snacks(snacks)
        self.assertEqual(sorted_snacks[0].name, "Fresh Apple")
        self.assertEqual(sorted_snacks[1].name, "Chocolate Bar") # Same shelf life as Dried Fruit, but higher calories/comfort
        self.assertEqual(sorted_snacks[2].name, "Dried Fruit")
        self.assertEqual(sorted_snacks[3].name, "Canned Beans")
        self.assertEqual(sorted_snacks[4].name, "MRE")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_prioritized_snacks(self, mock_stdout):
        # Mock rationale: Capture stdout to verify the printed output without affecting the console.
        snacks = [
            Snack("Fresh Apple", 7, 95, 4),
            Snack("Chocolate Bar", 365, 250, 5),
            Snack("Dried Fruit", 365, 150, 3),
            Snack("Canned Beans", 730, 200, 2),
            Snack("MRE", 1825, 1200, 3),
            Snack("Rotten Banana", 1, 50, 1) # Very short shelf life
        ]
        print_prioritized_snacks(snacks)
        output = mock_stdout.getvalue()

        self.assertIn("--- Apocalypse Snack Prioritization ---", output)
        self.assertIn("1. Fresh Apple (Shelf Life: 7 days, Calories: 95, Comfort: 4) - **CRITICAL: CONSUME IMMEDIATELY!**", output)
        self.assertIn("2. Chocolate Bar (Shelf Life: 365 days, Calories: 250, Comfort: 5) - Consume Soon!", output)
        self.assertIn("3. Dried Fruit (Shelf Life: 365 days, Calories: 150, Comfort: 3) - Consume Soon!", output)
        self.assertIn("4. Canned Beans (Shelf Life: 730 days, Calories: 200, Comfort: 2) - Store for Later.", output)
        self.assertIn("5. MRE (Shelf Life: 1825 days, Calories: 1200, Comfort: 3) - Store for Later.", output)
        self.assertIn("6. Rotten Banana (Shelf Life: 1 days, Calories: 50, Comfort: 1) - **CRITICAL: CONSUME IMMEDIATELY!**", output)
        self.assertIn("--- Stay Fed, Stay Alive! ---", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_no_args(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: Simulate running the script without arguments and capture stderr/exit.
        sys.argv = ['sorter.py']
        with self.assertRaises(SystemExit): # sys.exit raises SystemExit
            # We need to re-import the module to trigger the __main__ block again
            # as it's only executed once per process. This is a common pattern for testing main functions.
            import importlib
            importlib.reload(sys.modules['src.sorter'])
        mock_exit.assert_called_with(1)
        self.assertIn("Usage: python3 sorter.py <path_to_snack_file.txt>", mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_no_valid_snacks(self, mock_exit, mock_stderr, mock_stdout, mock_file_open):
        # Mock rationale: Simulate an input file with no valid snack data and capture stderr/exit.
        mock_file_open.return_value.read.return_value = (
            "Invalid Line,10,abc,3\n" # Invalid calories
            "# Comment\n"
        )
        sys.argv = ['sorter.py', 'empty.txt']
        with self.assertRaises(SystemExit): # sys.exit raises SystemExit
            # Reload module to re-trigger __main__ block
            import importlib
            importlib.reload(sys.modules['src.sorter'])
        mock_exit.assert_called_with(0)
        self.assertIn("No valid snacks found to sort.", mock_stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
