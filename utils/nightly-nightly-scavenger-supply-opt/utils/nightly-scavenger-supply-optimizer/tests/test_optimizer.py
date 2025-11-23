import unittest
from unittest.mock import patch, mock_open
import json
from src.optimizer import optimize_haul, load_item_manifest

class TestScavengerSupplyOptimizer(unittest.TestCase):

    def test_optimize_haul_basic_case(self):
        items = [
            {'name': 'A', 'weight': 1, 'value': 10}, # Ratio 10
            {'name': 'B', 'weight': 2, 'value': 18}, # Ratio 9
            {'name': 'C', 'weight': 3, 'value': 25}, # Ratio 8.33
        ]
        max_capacity = 3
        selected, weight, value = optimize_haul(items, max_capacity)
        self.assertIn({'name': 'A', 'weight': 1, 'value': 10}, selected)
        self.assertIn({'name': 'B', 'weight': 2, 'value': 18}, selected)
        self.assertEqual(len(selected), 2)
        self.assertAlmostEqual(weight, 3.0)
        self.assertAlmostEqual(value, 28.0)

    def test_optimize_haul_empty_items(self):
        items = []
        max_capacity = 10
        selected, weight, value = optimize_haul(items, max_capacity)
        self.assertEqual(selected, [])
        self.assertEqual(weight, 0.0)
        self.assertEqual(value, 0.0)

    def test_optimize_haul_zero_capacity(self):
        items = [{'name': 'A', 'weight': 1, 'value': 10}]
        max_capacity = 0
        selected, weight, value = optimize_haul(items, max_capacity)
        self.assertEqual(selected, [])
        self.assertEqual(weight, 0.0)
        self.assertEqual(value, 0.0)

    def test_optimize_haul_items_exceeding_capacity(self):
        items = [
            {'name': 'Heavy', 'weight': 5, 'value': 100},
            {'name': 'Light', 'weight': 1, 'value': 10},
        ]
        max_capacity = 3
        selected, weight, value = optimize_haul(items, max_capacity)
        self.assertIn({'name': 'Light', 'weight': 1, 'value': 10}, selected)
        self.assertEqual(len(selected), 1)
        self.assertAlmostEqual(weight, 1.0)
        self.assertAlmostEqual(value, 10.0)

    def test_optimize_haul_all_items_fit(self):
        items = [
            {'name': 'A', 'weight': 1, 'value': 10},
            {'name': 'B', 'weight': 1, 'value': 5},
        ]
        max_capacity = 5
        selected, weight, value = optimize_haul(items, max_capacity)
        self.assertIn({'name': 'A', 'weight': 1, 'value': 10}, selected)
        self.assertIn({'name': 'B', 'weight': 1, 'value': 5}, selected)
        self.assertEqual(len(selected), 2)
        self.assertAlmostEqual(weight, 2.0)
        self.assertAlmostEqual(value, 15.0)

    def test_optimize_haul_zero_weight_item(self):
        items = [
            {'name': 'ZeroWeight', 'weight': 0, 'value': 100}, # Should be prioritized highly
            {'name': 'Normal', 'weight': 1, 'value': 5},
        ]
        max_capacity = 1
        selected, weight, value = optimize_haul(items, max_capacity)
        self.assertIn({'name': 'ZeroWeight', 'weight': 0, 'value': 100}, selected)
        self.assertIn({'name': 'Normal', 'weight': 1, 'value': 5}, selected)
        self.assertEqual(len(selected), 2)
        self.assertAlmostEqual(weight, 1.0)
        self.assertAlmostEqual(value, 105.0)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_item_manifest(self, mock_json_load, mock_file_open):
        # Mock rationale: We want to test the `load_item_manifest` function without
        # actually reading from the filesystem. Mocking `builtins.open` and `json.load`
        # allows us to simulate file I/O and JSON parsing deterministically.
        mock_json_load.return_value = [
            {'name': 'Mock Item 1', 'weight': 1.0, 'value': 10},
            {'name': 'Mock Item 2', 'weight': 2.0, 'value': 20},
        ]
        filepath = 'mock_manifest.json'
        result = load_item_manifest(filepath)

        mock_file_open.assert_called_once_with(filepath, 'r')
        mock_json_load.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Mock Item 1')
        self.assertEqual(result[1]['value'], 20)
