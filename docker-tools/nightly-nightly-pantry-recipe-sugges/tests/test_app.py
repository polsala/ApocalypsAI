import io
import unittest
from unittest import mock

# Import the functions from the implementation module
from src.app import load_inventory, suggest_recipes, RECIPE_DB

class TestPantrySuggester(unittest.TestCase):
    def test_load_inventory_basic(self):
        csv_content = """ingredient,quantity\nOats,2\nHoney,1\nNuts,5\n"""
        # Mock open to return the CSV string without touching the filesystem
        with mock.patch('builtins.open', mock.mock_open(read_data=csv_content)):
            inventory = load_inventory('dummy.csv')
        expected = {"oats": 2, "honey": 1, "nuts": 5}
        self.assertEqual(inventory, expected)

    def test_load_inventory_ignores_invalid_quantity(self):
        csv_content = """ingredient,quantity\nEgg,abc\nBroth,0\nNoodles,3\n"""
        with mock.patch('builtins.open', mock.mock_open(read_data=csv_content)):
            inventory = load_inventory('dummy.csv')
        expected = {"noodles": 3}
        self.assertEqual(inventory, expected)

    def test_suggest_recipes_all_match(self):
        # Inventory contains everything needed for all recipes
        inventory = {"oats": 1, "honey": 1, "nuts": 1,
                     "noodles": 1, "broth": 1, "egg": 1,
                     "carrot": 1, "potato": 1, "beans": 1,
                     "tortilla": 1, "cheese": 1, "tomato": 1}
        suggestions = suggest_recipes(inventory)
        # Order is not guaranteed; compare as sets
        self.assertEqual(set(suggestions), set(RECIPE_DB.keys()))

    def test_suggest_recipes_partial_match(self):
        inventory = {"oats": 1, "honey": 1, "nuts": 1, "carrot": 1, "potato": 1}
        suggestions = suggest_recipes(inventory)
        # Only Mystic Muesli can be made; Scavenger's Stew lacks beans, etc.
        self.assertEqual(suggestions, ["Mystic Muesli"])

    def test_suggest_recipes_none(self):
        inventory = {"water": 10, "salt": 2}
        suggestions = suggest_recipes(inventory)
        self.assertEqual(suggestions, [])

if __name__ == '__main__':
    unittest.main()
