import unittest
from pathlib import Path
import sys

# Ensure the src directory is importable
src_path = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(src_path))

from main import suggest_recipe, load_ingredients

class TestScavengerMealPlanner(unittest.TestCase):
    def setUp(self):
        # Mock pantry file content
        self.pantry_file = Path(__file__).parent / "mock_ingredients.txt"
        self.pantry_file.write_text("spaghetti\nTomato Sauce\nCANNED BEANS\nwater\n")

    def tearDown(self):
        self.pantry_file.unlink()

    def test_load_ingredients(self):
        ingredients = load_ingredients(self.pantry_file)
        expected = {"spaghetti", "tomato sauce", "canned beans", "water"}
        self.assertEqual(ingredients, expected)

    def test_suggest_recipe(self):
        pantry = {"spaghetti", "tomato sauce", "canned beans", "water"}
        # With fixed seed, the first matching recipe chosen is deterministic
        recipe = suggest_recipe(pantry)
        self.assertEqual(recipe, "Spaghetti with Tomato Sauce and Canned Beans")

    def test_no_match(self):
        pantry = {"rice"}
        recipe = suggest_recipe(pantry)
        self.assertEqual(recipe, "No viable recipe found with given ingredients.")

if __name__ == "__main__":
    unittest.main()
