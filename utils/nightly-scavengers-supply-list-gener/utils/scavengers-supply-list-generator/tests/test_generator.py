import unittest
import json
import os
from unittest.mock import patch, mock_open
from src.generator import ScavengerSupplyGenerator

# Mock rationale: We need to ensure the ScavengerSupplyGenerator always loads
# a predictable dataset for testing, regardless of the actual file system state.
# Mocking 'open' prevents file system access and provides a consistent JSON string.
# Mocking 'os.path.exists' ensures that the generator believes the mocked file exists.
MOCK_DATA = {
    "flashlight": {
        "description": "A portable light source.",
        "components": [
            {"name": "battery", "quantity": "2-4 (AA/AAA)"},
            {"name": "bulb", "quantity": "1 (LED preferred)"}
        ],
        "locations": ["abandoned homes", "hardware stores"],
        "alternatives": ["candle", "oil lamp"]
    },
    "water filter": {
        "description": "Device to purify water.",
        "components": [
            {"name": "cloth", "quantity": "1 (fine weave)"},
            {"name": "charcoal", "quantity": "1 bag"}
        ],
        "locations": ["camping stores", "survival bunkers"],
        "alternatives": ["boiling water"]
    },
    "unknown item": {
        "description": "This item has no specific details.",
        "components": [],
        "locations": [],
        "alternatives": []
    }
}

class TestScavengerSupplyGenerator(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(MOCK_DATA))
    @patch('os.path.exists', return_value=True)
    def setUp(self, mock_exists, mock_file):
        # Initialize the generator, it will use the mocked open and exists check
        self.generator = ScavengerSupplyGenerator(data_path="mock_data.json")

    def test_load_data_success(self):
        # Verify that data was loaded correctly from the mock
        self.assertIn("flashlight", self.generator.supplies)
        self.assertIn("water filter", self.generator.supplies)
        self.assertEqual(len(self.generator.supplies), 3)

    def test_get_supply_list_known_item(self):
        result = self.generator.get_supply_list("flashlight")
        self.assertTrue(result["found"])
        self.assertEqual(result["item"], "flashlight")
        self.assertEqual(result["description"], MOCK_DATA["flashlight"]["description"])
        self.assertEqual(len(result["components"]), 2)
        self.assertIn({"name": "battery", "quantity": "2-4 (AA/AAA)"}, result["components"])
        self.assertEqual(len(result["locations"]), 2)
        self.assertIn("abandoned homes", result["locations"])
        self.assertEqual(len(result["alternatives"]), 2)
        self.assertIn("candle", result["alternatives"])

    def test_get_supply_list_unknown_item(self):
        result = self.generator.get_supply_list("nonexistent item")
        self.assertFalse(result["found"])
        self.assertEqual(result["item"], "nonexistent item")
        self.assertIn("No information found", result["message"])

    def test_get_supply_list_case_insensitivity(self):
        result = self.generator.get_supply_list("Flashlight")
        self.assertTrue(result["found"])
        self.assertEqual(result["item"], "Flashlight") # Original casing is preserved in output
        self.assertEqual(result["description"], MOCK_DATA["flashlight"]["description"])

    def test_get_supply_list_item_with_no_details(self):
        result = self.generator.get_supply_list("unknown item")
        self.assertTrue(result["found"])
        self.assertEqual(result["item"], "unknown item")
        self.assertEqual(result["description"], MOCK_DATA["unknown item"]["description"])
        self.assertEqual(result["components"], [])
        self.assertEqual(result["locations"], [])
        self.assertEqual(result["alternatives"], [])

    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('os.path.exists', return_value=True)
    def test_load_data_invalid_json(self, mock_exists, mock_file):
        # Mock rationale: Simulate a corrupted data.json file to test error handling.
        # Test that an empty supplies dict is returned on JSON decode error
        generator = ScavengerSupplyGenerator(data_path="mock_data.json")
        self.assertEqual(generator.supplies, {})

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('os.path.exists', return_value=False)
    def test_load_data_file_not_found(self, mock_exists, mock_file):
        # Mock rationale: Simulate a missing data.json file to test error handling.
        # Test that an empty supplies dict is returned on FileNotFoundError
        generator = ScavengerSupplyGenerator(data_path="non_existent_file.json")
        self.assertEqual(generator.supplies, {})

    def test_list_available_items(self):
        items = self.generator.list_available_items()
        # The list should be sorted alphabetically
        self.assertEqual(items, ["flashlight", "unknown item", "water filter"])
