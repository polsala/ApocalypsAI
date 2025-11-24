import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Mock rationale: We are testing the core logic of the recommender, as well as
# the command-line interface's interaction with the core logic and its output.
# For the `main` function, we need to capture stdout and simulate command-line
# arguments to ensure the full utility runs as expected without actual user interaction.
# The `SurvivalCookbook` is designed to be self-contained and does not require external mocks.

from src.recommender import Recipe, SurvivalCookbook, recommend_recipes, main

class TestRecipe(unittest.TestCase):
    def test_recipe_creation(self):
        recipe = Recipe(
            name="Test Stew",
            ingredients=["potato", "carrot"],
            instructions=["Boil", "Eat"],
            tip="Stay warm."
        )
        self.assertEqual(recipe.name, "Test Stew")
        self.assertEqual(recipe.ingredients, ["potato", "carrot"])
        self.assertEqual(recipe.instructions, ["Boil", "Eat"])
        self.assertEqual(recipe.tip, "Stay warm.")
        self.assertEqual(recipe.get_details()["name"], "Test Stew")

    def test_ingredient_normalization(self):
        recipe = Recipe(
            name="Mixed Greens",
            ingredients=["Spinach", "KALE"],
            instructions=["Mix"],
            tip="Healthy."
        )
        self.assertEqual(recipe.ingredients, ["spinach", "kale"])

class TestSurvivalCookbook(unittest.TestCase):
    def test_add_recipe(self):
        cookbook = SurvivalCookbook()
        initial_count = len(cookbook.get_all_recipes())
        new_recipe = Recipe("New Dish", ["a", "b"], ["c"], "d")
        cookbook.add_recipe(new_recipe)
        self.assertEqual(len(cookbook.get_all_recipes()), initial_count + 1)
        self.assertIn(new_recipe, cookbook.get_all_recipes())

    def test_default_recipes_loaded(self):
        cookbook = SurvivalCookbook()
        self.assertGreater(len(cookbook.get_all_recipes()), 0)
        # Check for a specific default recipe
        found_bunker_bean_stew = False
        for recipe in cookbook.get_all_recipes():
            if recipe.name == "Bunker Bean Stew":
                found_bunker_bean_stew = True
                break
        self.assertTrue(found_bunker_bean_stew)

class TestRecipeRecommender(unittest.TestCase):
    def setUp(self):
        self.cookbook = SurvivalCookbook()
        # Clear default recipes and add specific ones for controlled testing
        self.cookbook._recipes = []
        self.cookbook.add_recipe(Recipe(
            name="Simple Soup",
            ingredients=["water", "salt"],
            instructions=["Boil water", "Add salt"],
            tip="Basic survival."
        ))
        self.cookbook.add_recipe(Recipe(
            name="Hearty Stew",
            ingredients=["water", "salt", "canned beans", "mystery meat"],
            instructions=["Combine", "Cook"],
            tip="Full belly."
        ))
        self.cookbook.add_recipe(Recipe(
            name="Dry Ration",
            ingredients=["hard tack"],
            instructions=["Chew slowly"],
            tip="Lasts forever."
        ))
        self.cookbook.add_recipe(Recipe(
            name="Berry Delight",
            ingredients=["foraged berries", "clean water"],
            instructions=["Wash", "Mash"],
            tip="Sweet treat."
        ))

    def test_no_matching_ingredients(self):
        available = ["sugar", "flour"]
        recommendations = recommend_recipes(available, self.cookbook)
        self.assertEqual(len(recommendations), 0)

    def test_partial_match(self):
        available = ["water", "canned beans"]
        recommendations = recommend_recipes(available, self.cookbook)
        self.assertEqual(len(recommendations), 2) # Simple Soup (1 match), Hearty Stew (2 matches)

        # Check sorting: Hearty Stew should come first
        self.assertEqual(recommendations[0]["name"], "Hearty Stew")
        self.assertEqual(recommendations[0]["match_count"], 2)
        self.assertEqual(recommendations[1]["name"], "Simple Soup")
        self.assertEqual(recommendations[1]["match_count"], 1)

    def test_full_match(self):
        available = ["water", "salt", "canned beans", "mystery meat"]
        recommendations = recommend_recipes(available, self.cookbook)
        self.assertEqual(len(recommendations), 2) # Simple Soup (2 matches), Hearty Stew (4 matches)

        # Check sorting: Hearty Stew should come first
        self.assertEqual(recommendations[0]["name"], "Hearty Stew")
        self.assertEqual(recommendations[0]["match_count"], 4)
        self.assertEqual(recommendations[1]["name"], "Simple Soup")
        self.assertEqual(recommendations[1]["match_count"], 2)

    def test_case_insensitivity(self):
        available = ["Water", "SALT"]
        recommendations = recommend_recipes(available, self.cookbook)
        self.assertEqual(len(recommendations), 2)
        self.assertEqual(recommendations[0]["name"], "Simple Soup")
        self.assertEqual(recommendations[0]["match_count"], 2)

    def test_duplicate_ingredients_in_available(self):
        available = ["water", "water", "salt"] # Duplicates should not affect match count
        recommendations = recommend_recipes(available, self.cookbook)
        self.assertEqual(len(recommendations), 2)
        self.assertEqual(recommendations[0]["name"], "Simple Soup")
        self.assertEqual(recommendations[0]["match_count"], 2)

    def test_single_ingredient_recipe(self):
        available = ["hard tack"]
        recommendations = recommend_recipes(available, self.cookbook)
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0]["name"], "Dry Ration")
        self.assertEqual(recommendations[0]["match_count"], 1)

    def test_multiple_ingredients_one_match(self):
        available = ["water"]
        recommendations = recommend_recipes(available, self.cookbook)
        self.assertEqual(len(recommendations), 2) # Simple Soup (1 match), Hearty Stew (1 match)
        # Order might be arbitrary if match_count is same, but both should be present
        self.assertIn("Simple Soup", [r["name"] for r in recommendations])
        self.assertIn("Hearty Stew", [r["name"] for r in recommendations])
        self.assertEqual(recommendations[0]["match_count"], 1)
        self.assertEqual(recommendations[1]["match_count"], 1)


class TestMainFunction(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_recommendations(self, mock_stdout, mock_parse_args):
        # Mock rationale: Simulate command-line arguments and capture stdout
        # to verify the output format and content without actual CLI interaction.
        mock_parse_args.return_value = MagicMock(
            ingredients=["canned beans", "water", "salt"]
        )

        main()
        output = mock_stdout.getvalue()

        self.assertIn("--- Rad-Resistant Recipe Recommendations ---", output)
        self.assertIn("Bunker Bean Stew", output)
        self.assertIn("Matches 3/4 ingredients", output)
        self.assertIn("Stale Bread & Water Gruel", output)
        self.assertIn("Matches 2/2 ingredients", output)
        self.assertIn("Ingredients: canned beans, water, salt, scavenged greens", output)
        self.assertIn("Instructions:", output)
        self.assertIn("* Combine canned beans, water, and a pinch of salt in a pot.", output)
        self.assertIn("*Survival Tip:", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_recommendations(self, mock_stdout, mock_parse_args):
        # Mock rationale: Simulate command-line arguments and capture stdout
        # to verify the output when no recipes match.
        mock_parse_args.return_value = MagicMock(
            ingredients=["sugar", "flour", "chocolate"]
        )

        main()
        output = mock_stdout.getvalue()

        self.assertIn("--- Rad-Resistant Recipe Recommendations ---", output)
        self.assertIn("No recipes found matching your ingredients. Time to get creative (or hungry).", output)
        self.assertNotIn("Bunker Bean Stew", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_no_ingredients_provided(self, mock_exit, mock_stdout, mock_parse_args):
        # Mock rationale: Simulate command-line arguments where no ingredients are provided
        # and capture stdout/stderr to verify the error message and exit code.
        mock_parse_args.return_value = MagicMock(
            ingredients=[] # Simulate no ingredients provided after --ingredients
        )

        main()
        output = mock_stdout.getvalue()

        self.assertIn("Error: Please provide at least one ingredient using --ingredients.", output)
        mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
