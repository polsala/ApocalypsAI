import unittest
from unittest.mock import patch, mock_open
import json
import os
from src.scavenger import ScavengerListGenerator

class TestScavengerListGenerator(unittest.TestCase):

    # Mock rationale: We don't want tests to depend on actual file system state.
    # Mocking `open` allows us to provide a consistent, in-memory JSON string
    # as if it were read from `items.json`, ensuring deterministic tests.
    MOCK_ITEMS_JSON = json.dumps([
        {"name": "Item A", "category": "survival", "priority": 10},
        {"name": "Item B", "category": "food", "priority": 9},
        {"name": "Item C", "category": "tools", "priority": 8},
        {"name": "Item D", "category": "morale", "priority": 7},
        {"name": "Item E", "category": "food", "priority": 6},
        {"name": "Item F", "category": "survival", "priority": 5},
        {"name": "Item G", "category": "luxury", "priority": 4},
        {"name": "Item H", "category": "morale", "priority": 3}
    ])

    @patch('builtins.open', new_callable=mock_open, read_data=MOCK_ITEMS_JSON)
    @patch('os.path.exists', return_value=True)
    def test_load_items_success(self, mock_exists, mock_file):
        # Mock rationale: Ensure `os.path.exists` returns True so `open` is called.
        generator = ScavengerListGenerator(items_filepath='mock_items.json')
        self.assertIsNotNone(generator.items)
        self.assertEqual(len(generator.items), 8)
        self.assertEqual(generator.items[0]['name'], 'Item A')

    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('os.path.exists', return_value=True)
    def test_load_items_invalid_json(self, mock_exists, mock_file):
        # Mock rationale: Simulate a corrupted JSON file.
        generator = ScavengerListGenerator(items_filepath='mock_items.json')
        self.assertEqual(generator.items, [])

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('os.path.exists', return_value=False)
    def test_load_items_file_not_found(self, mock_exists, mock_file):
        # Mock rationale: Simulate the items file being missing.
        generator = ScavengerListGenerator(items_filepath='non_existent.json')
        self.assertEqual(generator.items, [])

    @patch('builtins.open', new_callable=mock_open, read_data=MOCK_ITEMS_JSON)
    @patch('os.path.exists', return_value=True)
    def test_generate_list_all_categories(self, mock_exists, mock_file):
        # Mock rationale: Use the predefined mock JSON data.
        generator = ScavengerListGenerator(items_filepath='mock_items.json')
        result = generator.generate_list(['all'])
        self.assertEqual(len(result), 8)
        # Check sorting by priority (descending)
        self.assertEqual(result[0]['name'], 'Item A') # Priority 10
        self.assertEqual(result[1]['name'], 'Item B') # Priority 9
        self.assertEqual(result[-1]['name'], 'Item H') # Priority 3

    @patch('builtins.open', new_callable=mock_open, read_data=MOCK_ITEMS_JSON)
    @patch('os.path.exists', return_value=True)
    def test_generate_list_specific_categories(self, mock_exists, mock_file):
        # Mock rationale: Use the predefined mock JSON data.
        generator = ScavengerListGenerator(items_filepath='mock_items.json')
        result = generator.generate_list(['food', 'morale'])
        self.assertEqual(len(result), 4)
        # Check sorting and filtering
        self.assertEqual(result[0]['name'], 'Item B') # Food, Priority 9
        self.assertEqual(result[1]['name'], 'Item D') # Morale, Priority 7
        self.assertEqual(result[2]['name'], 'Item E') # Food, Priority 6
        self.assertEqual(result[3]['name'], 'Item H') # Morale, Priority 3

    @patch('builtins.open', new_callable=mock_open, read_data=MOCK_ITEMS_JSON)
    @patch('os.path.exists', return_value=True)
    def test_generate_list_with_count(self, mock_exists, mock_file):
        # Mock rationale: Use the predefined mock JSON data.
        generator = ScavengerListGenerator(items_filepath='mock_items.json')
        result = generator.generate_list(['all'], count=3)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['name'], 'Item A')
        self.assertEqual(result[1]['name'], 'Item B')
        self.assertEqual(result[2]['name'], 'Item C')

    @patch('builtins.open', new_callable=mock_open, read_data=MOCK_ITEMS_JSON)
    @patch('os.path.exists', return_value=True)
    def test_generate_list_no_matching_categories(self, mock_exists, mock_file):
        # Mock rationale: Use the predefined mock JSON data.
        generator = ScavengerListGenerator(items_filepath='mock_items.json')
        result = generator.generate_list(['nonexistent_category'])
        self.assertEqual(len(result), 0)

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([]))
    @patch('os.path.exists', return_value=True)
    def test_generate_list_empty_items_file(self, mock_exists, mock_file):
        # Mock rationale: Simulate an empty items.json file.
        generator = ScavengerListGenerator(items_filepath='mock_items.json')
        result = generator.generate_list(['all'])
        self.assertEqual(len(result), 0)

    @patch('builtins.open', new_callable=mock_open, read_data=MOCK_ITEMS_JSON)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout') # Mock rationale: Capture print output for verification.
    def test_print_list_output(self, mock_stdout, mock_exists, mock_file):
        generator = ScavengerListGenerator(items_filepath='mock_items.json')
        items_to_print = [
            {"name": "Test Item 1", "category": "test", "priority": 5},
            {"name": "Test Item 2", "category": "another", "priority": 3}
        ]
        generator.print_list(items_to_print, ['test', 'another'])
        output = mock_stdout.write.call_args_list
        self.assertIn("--- Apocalypse Scavenging List (Categories: test, another) ---", output[0].args[0])
        self.assertIn("1. Test Item 1 (Test, Priority: 5)", output[1].args[0])
        self.assertIn("2. Test Item 2 (Another, Priority: 3)", output[2].args[0])

    @patch('builtins.open', new_callable=mock_open, read_data=MOCK_ITEMS_JSON)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout') # Mock rationale: Capture print output for verification.
    def test_print_list_empty_input(self, mock_stdout, mock_exists, mock_file):
        generator = ScavengerListGenerator(items_filepath='mock_items.json')
        generator.print_list([], ['empty'])
        output = mock_stdout.write.call_args_list
        self.assertIn("No items found for categories: empty", output[0].args[0])


if __name__ == '__main__':
    unittest.main()
