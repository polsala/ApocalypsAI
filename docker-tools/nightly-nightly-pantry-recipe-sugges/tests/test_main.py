import unittest
import tempfile
import os
from unittest import mock
import importlib.util

# Dynamically import the module from src/main.py
module_path = os.path.join(os.path.dirname(__file__), "..", "src", "main.py")
spec = importlib.util.spec_from_file_location("main", module_path)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)

class TestPantrySuggester(unittest.TestCase):
    def test_load_ingredients(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tf:
            tf.write("canned beans\nRice\nspice mix\n")
            tf.flush()
            ingredients = main.load_ingredients(tf.name)
            self.assertEqual(ingredients, {"canned beans", "rice", "spice mix"})
        os.unlink(tf.name)

    def test_suggest_recipes_exact_match(self):
        ingredients = {"canned beans", "water", "spice mix"}
        suggestions = main.suggest_recipes(ingredients)
        self.assertIn("Bean Soup", suggestions)
        self.assertEqual(len(suggestions), 1)

    def test_suggest_recipes_multiple(self):
        ingredients = {"canned beans", "rice", "water", "spice mix"}
        suggestions = main.suggest_recipes(ingredients)
        self.assertCountEqual(suggestions, ["Bean Soup", "Simple Stew"])

    @mock.patch('os.path.exists', return_value=False)
    @mock.patch('sys.exit')
    @mock.patch('sys.stderr', new_callable=mock.Mock)
    def test_main_missing_file(self, mock_stderr, mock_exit, mock_exists):
        # Run main(); it should detect missing file and exit with code 1
        main.main()
        mock_exit.assert_called_once_with(1)
        # Ensure an error message was written to stderr
        self.assertTrue(mock_stderr.write.called)

if __name__ == "__main__":
    unittest.main()
