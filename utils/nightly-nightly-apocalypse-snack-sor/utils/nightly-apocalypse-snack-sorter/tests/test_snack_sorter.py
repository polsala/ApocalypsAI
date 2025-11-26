import unittest
import json
from unittest.mock import patch, mock_open
import sys
import io
from src.snack_sorter import load_snacks, sort_by_shelf_life, sort_by_calories, find_high_morale_boosters

class TestSnackSorter(unittest.TestCase):

    def setUp(self):
        self.mock_snack_data = [
            {"name": "Canned Beans", "calories_per_serving": 150, "shelf_life_days": 1825, "morale_boost": 2},
            {"name": "Energy Bar", "calories_per_serving": 250, "shelf_life_days": 730, "morale_boost": 4},
            {"name": "Dried Fruit Mix", "calories_per_serving": 100, "shelf_life_days": 365, "morale_boost": 3},
            {"name": "Chocolate Bar", "calories_per_serving": 300, "shelf_life_days": 180, "morale_boost": 5},
            {"name": "MRE (Meal, Ready-to-Eat)", "calories_per_serving": 1200, "shelf_life_days": 1825, "morale_boost": 3}
        ]
        self.mock_json_content = json.dumps(self.mock_snack_data)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_snacks_success(self, mock_json_load, mock_file_open):
        # Mock rationale: We don't want to rely on actual file system access for tests.
        # `mock_open` simulates opening a file, and `json.load` simulates reading JSON content.
        mock_json_load.return_value = self.mock_snack_data
        
        snacks = load_snacks('dummy_path.json')
        self.assertEqual(snacks, self.mock_snack_data)
        mock_file_open.assert_called_once_with('dummy_path.json', 'r', encoding='utf-8')
        mock_json_load.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_load_snacks_file_not_found(self, mock_file_open):
        # Mock rationale: Simulate a FileNotFoundError without needing to create/delete files.
        mock_file_open.side_effect = FileNotFoundError
        
        with patch('sys.stderr', new=io.StringIO()) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                load_snacks('non_existent.json')
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Inventory file not found", mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_snacks_invalid_json(self, mock_json_load, mock_file_open):
        # Mock rationale: Simulate a JSONDecodeError without needing to write malformed JSON to a file.
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        
        with patch('sys.stderr', new=io.StringIO()) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                load_snacks('malformed.json')
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Invalid JSON format", mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_snacks_invalid_data_structure(self, mock_json_load, mock_file_open):
        # Mock rationale: Test validation of the loaded data structure (must be a list) without external files.
        mock_json_load.return_value = {"not_a_list": []}
        
        with patch('sys.stderr', new=io.StringIO()) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                load_snacks('invalid_structure.json')
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Invalid snack data in 'invalid_structure.json': Snack data must be a list of objects.", mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_snacks_missing_key(self, mock_json_load, mock_file_open):
        # Mock rationale: Test validation for missing required keys in snack objects.
        mock_json_load.return_value = [
            {"name": "Missing Key Snack", "calories_per_serving": 100}
        ]
        
        with patch('sys.stderr', new=io.StringIO()) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                load_snacks('missing_key.json')
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Invalid snack data in 'missing_key.json': Snack missing required key(s): shelf_life_days, morale_boost", mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_snacks_invalid_data_type(self, mock_json_load, mock_file_open):
        # Mock rationale: Test validation for incorrect data types.
        mock_json_load.return_value = [
            {"name": "Bad Type Snack", "calories_per_serving": "100", "shelf_life_days": 365, "morale_boost": 3}
        ]
        
        with patch('sys.stderr', new=io.StringIO()) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                load_snacks('bad_type.json')
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Invalid snack data in 'bad_type.json': Snack has invalid data types for one or more fields", mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_snacks_invalid_morale_boost_range(self, mock_json_load, mock_file_open):
        # Mock rationale: Test validation for morale_boost being out of the 1-5 range.
        mock_json_load.return_value = [
            {"name": "Bad Morale Snack", "calories_per_serving": 100, "shelf_life_days": 365, "morale_boost": 0}
        ]
        
        with patch('sys.stderr', new=io.StringIO()) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                load_snacks('bad_morale.json')
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Invalid snack data in 'bad_morale.json': Morale boost must be between 1 and 5", mock_stderr.getvalue())

    def test_sort_by_shelf_life(self):
        sorted_snacks = sort_by_shelf_life(self.mock_snack_data)
        expected_order = [
            "Canned Beans", # 1825 (original order preserved for ties)
            "MRE (Meal, Ready-to-Eat)", # 1825
            "Energy Bar", # 730
            "Dried Fruit Mix", # 365
            "Chocolate Bar" # 180
        ]
        self.assertEqual([s['name'] for s in sorted_snacks], expected_order)

    def test_sort_by_calories(self):
        sorted_snacks = sort_by_calories(self.mock_snack_data)
        expected_order = [
            "MRE (Meal, Ready-to-Eat)", # 1200
            "Chocolate Bar", # 300
            "Energy Bar", # 250
            "Canned Beans", # 150
            "Dried Fruit Mix" # 100
        ]
        self.assertEqual([s['name'] for s in sorted_snacks], expected_order)

    def test_find_high_morale_boosters(self):
        top_2_morale = find_high_morale_boosters(self.mock_snack_data, 2)
        expected_order = [
            "Chocolate Bar", # 5
            "Energy Bar" # 4
        ]
        self.assertEqual([s['name'] for s in top_2_morale], expected_order)

        top_5_morale = find_high_morale_boosters(self.mock_snack_data, 5)
        expected_order_5 = [
            "Chocolate Bar", # 5
            "Energy Bar", # 4
            "Dried Fruit Mix", # 3 (original order preserved for ties)
            "MRE (Meal, Ready-to-Eat)", # 3
            "Canned Beans" # 2
        ]
        self.assertEqual([s['name'] for s in top_5_morale], expected_order_5)

        # Test with count > number of snacks
        top_10_morale = find_high_morale_boosters(self.mock_snack_data, 10)
        self.assertEqual(len(top_10_morale), len(self.mock_snack_data))

        # Test with empty list
        self.assertEqual(find_high_morale_boosters([], 1), [])

if __name__ == '__main__':
    unittest.main()
