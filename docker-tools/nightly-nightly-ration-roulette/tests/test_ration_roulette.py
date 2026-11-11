import unittest
from unittest.mock import patch, mock_open
import json
import sys
import io
from src.ration_roulette import load_inventory, suggest_meal, main

class TestRationRoulette(unittest.TestCase):

    def setUp(self):
        self.mock_inventory_data = {
            "inventory": {
                "protein": [
                    {"name": "Canned Tuna", "quantity": 5},
                    {"name": "Dried Beef Jerky", "quantity": 10}
                ],
                "carb": [
                    {"name": "Hardtack Biscuits", "quantity": 20},
                    {"name": "Instant Noodles", "quantity": 7}
                ],
                "fat": [
                    {"name": "Peanut Butter Jar", "quantity": 2}
                ],
                "veggie": [
                    {"name": "Canned Green Beans", "quantity": 6}
                ],
                "treat": [
                    {"name": "Chocolate Bar", "quantity": 3}
                ]
            },
            "meal_composition": {
                "standard": ["protein", "carb", "veggie"],
                "hearty": ["protein", "carb", "fat", "veggie"],
                "snack": ["protein", "treat"],
                "empty_category_meal": ["protein", "non_existent_category"]
            }
        }
        # Mock rationale: We need a consistent inventory for testing without relying on actual files.
        self.mock_file_content = json.dumps(self.mock_inventory_data)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_inventory_success(self, mock_json_load, mock_file_open):
        # Mock rationale: Simulate successful file reading and JSON parsing.
        mock_file_open.return_value.read.return_value = self.mock_file_content
        mock_json_load.return_value = self.mock_inventory_data
        
        inventory = load_inventory("dummy_path.json")
        self.assertEqual(inventory, self.mock_inventory_data)
        mock_file_open.assert_called_once_with("dummy_path.json", 'r')
        mock_json_load.assert_called_once()

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_load_inventory_file_not_found(self, mock_stderr, mock_file_open):
        # Mock rationale: Simulate a missing inventory file.
        with self.assertRaises(SystemExit) as cm:
            load_inventory("non_existent.json")
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Inventory file 'non_existent.json' not found.", mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "doc", 0))
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_load_inventory_invalid_json(self, mock_stderr, mock_json_load, mock_file_open):
        # Mock rationale: Simulate a malformed JSON inventory file.
        mock_file_open.return_value.read.return_value = "{invalid json"
        with self.assertRaises(SystemExit) as cm:
            load_inventory("invalid.json")
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Invalid JSON in 'invalid.json'.", mock_stderr.getvalue())

    @patch('random.choice')
    def test_suggest_meal_standard(self, mock_random_choice):
        # Mock rationale: Control random choices for deterministic testing.
        mock_random_choice.side_effect = [
            {"name": "Canned Tuna", "quantity": 5},      # protein
            {"name": "Hardtack Biscuits", "quantity": 20}, # carb
            {"name": "Canned Green Beans", "quantity": 6}  # veggie
        ]
        
        meal = suggest_meal(self.mock_inventory_data, "standard")
        self.assertIsNotNone(meal)
        self.assertIn("protein", meal)
        self.assertIn("carb", meal)
        self.assertIn("veggie", meal)
        self.assertEqual(meal["protein"], "Canned Tuna")
        self.assertEqual(meal["carb"], "Hardtack Biscuits")
        self.assertEqual(meal["veggie"], "Canned Green Beans")
        self.assertEqual(mock_random_choice.call_count, 3)

    @patch('random.choice')
    def test_suggest_meal_hearty(self, mock_random_choice):
        # Mock rationale: Control random choices for deterministic testing.
        mock_random_choice.side_effect = [
            {"name": "Dried Beef Jerky", "quantity": 10}, # protein
            {"name": "Instant Noodles", "quantity": 7},    # carb
            {"name": "Peanut Butter Jar", "quantity": 2},  # fat
            {"name": "Canned Green Beans", "quantity": 6}  # veggie
        ]
        
        meal = suggest_meal(self.mock_inventory_data, "hearty")
        self.assertIsNotNone(meal)
        self.assertIn("protein", meal)
        self.assertIn("carb", meal)
        self.assertIn("fat", meal)
        self.assertIn("veggie", meal)
        self.assertEqual(meal["protein"], "Dried Beef Jerky")
        self.assertEqual(meal["carb"], "Instant Noodles")
        self.assertEqual(meal["fat"], "Peanut Butter Jar")
        self.assertEqual(meal["veggie"], "Canned Green Beans")
        self.assertEqual(mock_random_choice.call_count, 4)

    @patch('random.choice')
    def test_suggest_meal_snack(self, mock_random_choice):
        # Mock rationale: Control random choices for deterministic testing.
        mock_random_choice.side_effect = [
            {"name": "Canned Tuna", "quantity": 5},      # protein
            {"name": "Chocolate Bar", "quantity": 3}     # treat
        ]
        
        meal = suggest_meal(self.mock_inventory_data, "snack")
        self.assertIsNotNone(meal)
        self.assertIn("protein", meal)
        self.assertIn("treat", meal)
        self.assertEqual(meal["protein"], "Canned Tuna")
        self.assertEqual(meal["treat"], "Chocolate Bar")
        self.assertEqual(mock_random_choice.call_count, 2)

    def test_suggest_meal_unknown_type(self):
        meal = suggest_meal(self.mock_inventory_data, "breakfast")
        self.assertIsNone(meal)

    @patch('sys.stderr', new_callable=io.StringIO)
    def test_suggest_meal_missing_category_in_composition(self, mock_stderr):
        # Mock rationale: Test handling of a meal composition referencing a non-existent category.
        meal = suggest_meal(self.mock_inventory_data, "empty_category_meal")
        self.assertIsNotNone(meal) # It should still return a meal, just with fewer items
        self.assertIn("protein", meal)
        self.assertNotIn("non_existent_category", meal)
        self.assertIn("Warning: No items available for category 'non_existent_category'", mock_stderr.getvalue())

    @patch('src.ration_roulette.load_inventory')
    @patch('src.ration_roulette.suggest_meal')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['ration_roulette.py', 'standard'])
    def test_main_standard_meal(self, mock_stdout, mock_suggest_meal, mock_load_inventory):
        # Mock rationale: Isolate main function logic from file I/O and random choices.
        mock_load_inventory.return_value = self.mock_inventory_data
        mock_suggest_meal.return_value = {
            "protein": "Canned Tuna",
            "carb": "Hardtack Biscuits",
            "veggie": "Canned Green Beans"
        }

        main()
        output = mock_stdout.getvalue()
        self.assertIn("--- ApocalypsAI Ration Roulette: Standard Meal ---", output)
        self.assertIn("- Protein: Canned Tuna", output)
        self.assertIn("- Carb: Hardtack Biscuits", output)
        self.assertIn("- Veggie: Canned Green Beans", output)
        self.assertIn("Enjoy your varied sustenance!", output)
        mock_load_inventory.assert_called_once()
        mock_suggest_meal.assert_called_once_with(self.mock_inventory_data, "standard")

    @patch('src.ration_roulette.load_inventory')
    @patch('src.ration_roulette.suggest_meal')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.argv', ['ration_roulette.py', 'unknown_meal_type'])
    def test_main_unknown_meal_type(self, mock_stderr, mock_stdout, mock_suggest_meal, mock_load_inventory):
        # Mock rationale: Test main function behavior when an unknown meal type is requested.
        mock_load_inventory.return_value = self.mock_inventory_data
        mock_suggest_meal.return_value = None # Simulate suggest_meal returning None for unknown type

        main()
        output_stdout = mock_stdout.getvalue()
        output_stderr = mock_stderr.getvalue()
        self.assertIn("Failed to suggest a meal. Check your inventory and meal compositions.", output_stdout)
        self.assertIn("Error: Meal type 'unknown_meal_type' not found in meal_composition.", output_stderr)
        mock_load_inventory.assert_called_once()
        mock_suggest_meal.assert_called_once_with(self.mock_inventory_data, "unknown_meal_type")

    @patch('src.ration_roulette.load_inventory')
    @patch('src.ration_roulette.suggest_meal')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['ration_roulette.py']) # No meal type specified, defaults to standard
    def test_main_default_meal_type(self, mock_stdout, mock_suggest_meal, mock_load_inventory):
        # Mock rationale: Test main function behavior when no meal type is provided, expecting 'standard'.
        mock_load_inventory.return_value = self.mock_inventory_data
        mock_suggest_meal.return_value = {
            "protein": "Dried Beef Jerky",
            "carb": "Instant Noodles",
            "veggie": "Canned Green Beans"
        }

        main()
        output = mock_stdout.getvalue()
        self.assertIn("--- ApocalypsAI Ration Roulette: Standard Meal ---", output)
        self.assertIn("- Protein: Dried Beef Jerky", output)
        mock_suggest_meal.assert_called_once_with(self.mock_inventory_data, "standard")

    @patch('src.ration_roulette.load_inventory')
    @patch('src.ration_roulette.suggest_meal')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['ration_roulette.py', 'standard'])
    def test_main_no_meal_composed(self, mock_stdout, mock_suggest_meal, mock_load_inventory):
        # Mock rationale: Test scenario where suggest_meal returns an empty dictionary (e.g., no items available).
        mock_load_inventory.return_value = self.mock_inventory_data
        mock_suggest_meal.return_value = {}

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Could not compose a meal with available rations.", output)
        mock_load_inventory.assert_called_once()
        mock_suggest_meal.assert_called_once_with(self.mock_inventory_data, "standard")

    @patch('src.ration_roulette.load_inventory')
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['ration_roulette.py', 'standard'])
    def test_main_load_inventory_fails(self, mock_stdout, mock_stderr, mock_load_inventory):
        # Mock rationale: Test main function behavior when inventory loading fails.
        mock_load_inventory.return_value = None # Simulate load_inventory failing and exiting
        
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        # load_inventory itself prints the error, main just exits.
        self.assertEqual(mock_stdout.getvalue(), "") # No output from main if load fails early
        mock_load_inventory.assert_called_once()

    @patch('random.choice')
    def test_suggest_meal_with_zero_quantity(self, mock_random_choice):
        # Mock rationale: Ensure items with quantity 0 are not chosen.
        inventory_with_zero = {
            "inventory": {
                "protein": [
                    {"name": "Empty Can", "quantity": 0},
                    {"name": "Full Can", "quantity": 1}
                ]
            },
            "meal_composition": {"test": ["protein"]}
        }
        mock_random_choice.return_value = {"name": "Full Can", "quantity": 1}
        
        meal = suggest_meal(inventory_with_zero, "test")
        self.assertEqual(meal["protein"], "Full Can")
        # Ensure random.choice was called with only the 'Full Can' item
        mock_random_choice.assert_called_once_with([{"name": "Full Can", "quantity": 1}])

if __name__ == '__main__':
    unittest.main()
