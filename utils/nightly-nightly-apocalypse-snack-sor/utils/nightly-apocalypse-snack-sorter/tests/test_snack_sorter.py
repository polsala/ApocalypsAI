import unittest
import json
from unittest.mock import patch, mock_open
import os

# Mock rationale: We need to test the `load_snacks` function without actual file I/O.
# `mock_open` allows us to simulate reading a file from disk, providing predefined content.
# `patch('os.path.exists')` ensures that `os.path.exists` returns True for our mocked file path,
# preventing `FileNotFoundError` before `mock_open` can intercept the file opening.

from src.snack_sorter import Snack, load_snacks, sort_snacks

class TestSnackSorter(unittest.TestCase):

    def test_snack_initialization(self):
        snack = Snack("Test Bar", 100, 300, 4)
        self.assertEqual(snack.name, "Test Bar")
        self.assertEqual(snack.shelf_life_days, 100)
        self.assertEqual(snack.calories_per_serving, 300)
        self.assertEqual(snack.comfort_factor, 4)

        with self.assertRaises(ValueError):
            Snack("Bad Snack", 10, 10, 0) # Comfort factor too low
        with self.assertRaises(ValueError):
            Snack("Bad Snack", 10, 10, 6) # Comfort factor too high

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_load_snacks_success(self, mock_file, mock_exists):
        mock_data = [
            {"name": "Canned Beans", "shelf_life_days": 365, "calories_per_serving": 200, "comfort_factor": 2},
            {"name": "Chocolate Bar", "shelf_life_days": 90, "calories_per_serving": 250, "comfort_factor": 5}
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_data)

        snacks = load_snacks("dummy/path/snacks.json")
        self.assertEqual(len(snacks), 2)
        self.assertEqual(snacks[0].name, "Canned Beans")
        self.assertEqual(snacks[1].name, "Chocolate Bar")

    @patch('os.path.exists', return_value=False)
    def test_load_snacks_file_not_found(self, mock_exists):
        with self.assertRaises(FileNotFoundError):
            load_snacks("nonexistent/path/snacks.json")

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_load_snacks_invalid_json(self, mock_file, mock_exists):
        mock_file.return_value.read.return_value = "{invalid json"
        with self.assertRaises(json.JSONDecodeError):
            load_snacks("dummy/path/snacks.json")

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_load_snacks_missing_key(self, mock_file, mock_exists):
        mock_data = [
            {"name": "Canned Beans", "shelf_life_days": 365, "calories_per_serving": 200}
        ] # Missing comfort_factor
        mock_file.return_value.read.return_value = json.dumps(mock_data)
        with self.assertRaises(ValueError) as cm:
            load_snacks("dummy/path/snacks.json")
        self.assertIn("Missing key in snack data: 'comfort_factor'", str(cm.exception))

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_load_snacks_invalid_comfort_factor(self, mock_file, mock_exists):
        mock_data = [
            {"name": "Canned Beans", "shelf_life_days": 365, "calories_per_serving": 200, "comfort_factor": 0}
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_data)
        with self.assertRaises(ValueError) as cm:
            load_snacks("dummy/path/snacks.json")
        self.assertIn("Invalid value in snack data: Comfort factor must be between 1 and 5.", str(cm.exception))

    def test_sort_snacks_logic(self):
        snack1 = Snack("Chocolate Bar", 90, 250, 5)  # Shortest shelf life, high comfort
        snack2 = Snack("Dried Fruit", 180, 150, 3)   # Medium shelf life
        snack3 = Snack("Canned Beans", 365, 200, 2)  # Longest shelf life
        snack4 = Snack("MRE", 730, 1200, 3)          # Very long shelf life, very high calories
        snack5 = Snack("Protein Bar", 90, 300, 4)   # Same shelf life as snack1, higher calories, lower comfort

        snacks = [snack3, snack2, snack1, snack4, snack5]
        sorted_snacks = sort_snacks(snacks)

        # Expected order:
        # 1. snack5 (90 days, 300 cal, 4 comfort) - because 90 days, 300 cal > snack1
        # 2. snack1 (90 days, 250 cal, 5 comfort) - because 90 days, 250 cal
        # 3. snack2 (180 days, 150 cal, 3 comfort)
        # 4. snack3 (365 days, 200 cal, 2 comfort)
        # 5. snack4 (730 days, 1200 cal, 3 comfort)

        self.assertEqual(sorted_snacks[0].name, "Protein Bar")
        self.assertEqual(sorted_snacks[1].name, "Chocolate Bar")
        self.assertEqual(sorted_snacks[2].name, "Dried Fruit")
        self.assertEqual(sorted_snacks[3].name, "Canned Beans")
        self.assertEqual(sorted_snacks[4].name, "MRE")

    def test_sort_snacks_empty_list(self):
        self.assertEqual(sort_snacks([]), [])

    def test_sort_snacks_single_item(self):
        snack = Snack("Single Item", 100, 100, 3)
        self.assertEqual(sort_snacks([snack]), [snack])

    def test_sort_snacks_all_same_values(self):
        snack1 = Snack("A", 100, 200, 3)
        snack2 = Snack("B", 100, 200, 3)
        snack3 = Snack("C", 100, 200, 3)
        snacks = [snack3, snack1, snack2]
        sorted_snacks = sort_snacks(snacks)
        # Python's `sorted` is stable, so original order for equal elements is preserved.
        # However, `__lt__` defines the comparison, so the order will be consistent.
        # For this test, we just ensure the list contains the same items.
        self.assertCountEqual(sorted_snacks, [snack1, snack2, snack3])
