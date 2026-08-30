import unittest
from unittest import mock
import sys
import io

# Import the module under test
from src import app

class TestScavengerMealPlanner(unittest.TestCase):
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='rat\nwater\nspice\n')
    def test_recipe_found(self, mock_file):
        # Capture stdout
        captured = io.StringIO()
        sys.stdout = captured
        try:
            app.main()
        finally:
            sys.stdout = sys.__stdout__
        output = captured.getvalue()
        # With the fixed random seed, the first matching recipe should be Radiated Rat Stew
        self.assertIn('Recipe: Radiated Rat Stew', output)
        self.assertIn('Ingredients needed: rat, spice, water', output)
        self.assertIn('Instructions: Boil rat in water, add spice, simmer until glowing.', output)

    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='cactus\noil\n')
    def test_no_recipe(self, mock_file):
        captured = io.StringIO()
        sys.stdout = captured
        try:
            app.main()
        finally:
            sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn('No matching recipe found with given ingredients.', output)

if __name__ == '__main__':
    unittest.main()
