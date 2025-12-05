import io
import sys
import unittest
from unittest.mock import patch

# Import the module under test
from utils.zen_quote.src.quote import get_random_quote, main


class TestZenQuote(unittest.TestCase):
    def test_get_random_quote_with_category(self):
        # Mock random.choice to return a predictable quote
        with patch("random.choice", return_value="Mocked Quote"):
            quote = get_random_quote(category="life")
            self.assertEqual(quote, "Mocked Quote")

    def test_get_random_quote_without_category(self):
        with patch("random.choice", return_value="Universal Mock"):
            quote = get_random_quote()
            self.assertEqual(quote, "Universal Mock")

    def test_cli_output(self):
        test_args = ["--category", "work"]
        with patch("random.choice", return_value="CLI Mock Quote"):
            with patch.object(sys, "argv", ["quote.py"] + test_args):
                captured = io.StringIO()
                with patch("sys.stdout", new=captured):
                    exit_code = main()
                self.assertEqual(exit_code, 0)
                self.assertIn("CLI Mock Quote", captured.getvalue())


if __name__ == "__main__":
    unittest.main()
