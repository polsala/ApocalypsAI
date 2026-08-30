import os
import sys
import unittest
from pathlib import Path
from unittest import mock

# Ensure the src package is importable
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src import app

class TestScavengerMealPlanner(unittest.TestCase):
    def setUp(self):
        # Force deterministic randomness
        os.environ["SCAVENGER_TEST_MODE"] = "1"
        # Mock the ingredient file path used by the app
        self.patcher = mock.patch('src.app.Path.is_file', return_value=True)
        self.mock_is_file = self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.read_text_patcher = mock.patch('src.app.Path.read_text', return_value="canned beans\nspiced jerky\nmystery powder\n")
        self.mock_read_text = self.read_text_patcher.start()
        self.addCleanup(self.read_text_patcher.stop)

    def test_generate_recipe_output(self):
        # Load ingredients via the app's helper (will use mocked file)
        ingredients = app.load_ingredients(Path('/data/ingredients.txt'))
        self.assertEqual(ingredients, ["canned beans", "spiced jerky", "mystery powder"])
        recipe = app.generate_recipe(ingredients)
        # With seed=0 the chosen template and ordering are deterministic
        expected = "🛠️  Radiated Stew with canned beans, spiced jerky, and mystery powder. Enjoy your post‑apocalypse feast!"
        self.assertEqual(recipe, expected)

    def test_fewer_ingredients(self):
        # Change mock to return only one ingredient
        self.mock_read_text.return_value = "lonely can\n"
        ingredients = app.load_ingredients(Path('/data/ingredients.txt'))
        self.assertEqual(ingredients, ["lonely can"])
        recipe = app.generate_recipe(ingredients)
        # Should still produce a valid string containing the single ingredient
        self.assertIn("lonely can", recipe)

if __name__ == '__main__':
    unittest.main()
