import unittest
from unittest import mock
import sys
from io import StringIO

import src.app as app


class TestRecipeSuggester(unittest.TestCase):
    def test_suggest_recipes_basic(self):
        pantry = ["bread", "peanut butter", "apple"]
        expected = ["Peanut Butter Sandwich", "Apple Snack"]
        result = app.suggest_recipes([i.lower() for i in pantry])
        self.assertCountEqual(result, expected)

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='["carrot","potato","water"]')
    def test_main_output(self, mock_file):
        # Capture stdout
        captured = StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = captured
        try:
            with mock.patch.dict('os.environ', {"PANTRY_PATH": "/fake/pantry.json"}):
                app.main()
        finally:
            sys.stdout = sys_stdout_original
        output = captured.getvalue()
        self.assertIn("Veggie Soup", output)


if __name__ == "__main__":
    unittest.main()
