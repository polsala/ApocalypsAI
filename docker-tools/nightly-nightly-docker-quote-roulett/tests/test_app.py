import unittest
import os
import sys
from io import StringIO
import importlib.util

class TestQuoteApp(unittest.TestCase):
    def setUp(self):
        # Load the app module from src/app.py without installing the package
        spec = importlib.util.spec_from_file_location(
            "app", os.path.join(os.path.dirname(__file__), "..", "src", "app.py")
        )
        self.app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.app)

    def test_deterministic_quote(self):
        os.environ["QUOTE_INDEX"] = "0"
        captured = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured
        try:
            self.app.main()
        finally:
            sys.stdout = original_stdout
        output = captured.getvalue().strip()
        expected = "The only limit to our realization of tomorrow is our doubts today."
        self.assertEqual(output, expected)

    def test_random_fallback(self):
        os.environ.pop("QUOTE_INDEX", None)
        captured = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured
        try:
            self.app.main()
        finally:
            sys.stdout = original_stdout
        output = captured.getvalue().strip()
        self.assertIn(output, self.app.load_quotes())

if __name__ == "__main__":
    unittest.main()
