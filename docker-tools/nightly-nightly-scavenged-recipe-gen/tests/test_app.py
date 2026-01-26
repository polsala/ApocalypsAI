import unittest
from unittest.mock import patch
import sys
import os

# Add the src directory to the path to allow importing app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import generate_recipe

class TestRecipeGenerator(unittest.TestCase):

    def test_generate_recipe_with_ingredients(self):
        # Mock rationale: We want to test the function's output format and content
        # without relying on actual user input or external randomness for structure.
        # The 'random' module is not mocked here to allow for varied output, but
        # the test asserts on the *structure* and *presence* of elements, not specific random values.
        ingredients = "old boot, stale bread, puddle water"
        recipe = generate_recipe(ingredients)

        self.assertIsInstance(recipe, str)
        self.assertIn("--- The", recipe)
        self.assertIn("---", recipe)
        self.assertIn("A hearty", recipe)
        self.assertIn("featuring the rare", recipe)
        self.assertIn("Instructions:", recipe)
        self.assertIn("1. Gather your", recipe)
        self.assertIn("2. ", recipe)
        self.assertIn("3. Serve with a side of existential dread.", recipe)
        self.assertIn("old boot", recipe)
        self.assertIn("stale bread", recipe)
        self.assertIn("puddle water", recipe)

    def test_generate_recipe_without_ingredients(self):
        # Mock rationale: Same as above, testing the default behavior when no ingredients are provided.
        recipe = generate_recipe("")

        self.assertIsInstance(recipe, str)
        self.assertIn("--- The", recipe)
        self.assertIn("---", recipe)
        self.assertIn("A hearty", recipe)
        self.assertIn("featuring the rare mystery ingredient.", recipe)
        self.assertIn("Instructions:", recipe)
        self.assertIn("1. Gather your mystery ingredients.", recipe)
        self.assertIn("2. ", recipe)
        self.assertIn("3. Serve with a side of existential dread.", recipe)

    @patch('sys.argv', ['app.py', 'canned beans,dried jerky'])
    @patch('builtins.print')
    def test_main_execution_with_args(self, mock_print):
        # Mock rationale: We need to simulate command-line arguments (sys.argv)
        # and capture the output of print() to verify the script's behavior
        # when run as a standalone script.
        import app # Re-import to trigger __main__ block with patched sys.argv
        mock_print.assert_called_once()
        output = mock_print.call_args[0][0]

        self.assertIn("--- The", output)
        self.assertIn("canned beans", output)
        self.assertIn("dried jerky", output)

    @patch('sys.argv', ['app.py'])
    @patch('builtins.print')
    def test_main_execution_without_args(self, mock_print):
        # Mock rationale: Simulating command-line execution without arguments
        # to ensure the default 'mystery ingredient' path is taken.
        import app # Re-import to trigger __main__ block with patched sys.argv
        mock_print.assert_called_once()
        output = mock_print.call_args[0][0]

        self.assertIn("--- The", output)
        self.assertIn("mystery ingredient", output)

if __name__ == '__main__':
    unittest.main()
