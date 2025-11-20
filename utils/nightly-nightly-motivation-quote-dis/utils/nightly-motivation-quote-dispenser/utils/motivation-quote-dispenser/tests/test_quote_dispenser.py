import unittest
from unittest.mock import patch
import importlib.util
import pathlib

# Load the module from the relative path.
MODULE_PATH = pathlib.Path(__file__).resolve().parents[2] / "src" / "quote_dispenser.py"
spec = importlib.util.spec_from_file_location("quote_dispenser", MODULE_PATH)
quote_dispenser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quote_dispenser)  # type: ignore

# Mock rationale: we replace random.choice to make the output deterministic.
# This ensures the test does not depend on actual randomness.

class TestQuoteDispenser(unittest.TestCase):
    def test_get_random_quote_no_tag(self):
        with patch("random.choice", return_value={
            "text": "Believe you can and you're halfway there.",
            "author": "Theodore Roosevelt",
            "tags": ["inspiration", "confidence"],
        }) as mock_choice:  # Mock rationale: deterministic selection.
            quote = quote_dispenser.get_random_quote()
            self.assertEqual(quote["author"], "Theodore Roosevelt")
            mock_choice.assert_called_once()

    def test_get_random_quote_with_tag(self):
        with patch("random.choice", return_value={
            "text": "If at first you don’t succeed, call it version 1.0.",
            "author": "Unknown",
            "tags": ["humor", "programming"],
        }) as mock_choice:  # Mock rationale: deterministic selection.
            quote = quote_dispenser.get_random_quote(tag="humor")
            self.assertIn("humor", [t.lower() for t in quote["tags"]])
            mock_choice.assert_called_once()

    def test_get_random_quote_invalid_tag(self):
        with self.assertRaises(ValueError) as ctx:
            quote_dispenser.get_random_quote(tag="nonexistent")
        self.assertIn("No quotes found for tag", str(ctx.exception))

    def test_format_quote(self):
        quote = {
            "text": "Life is what happens when you're busy making other plans.",
            "author": "John Lennon",
            "tags": ["life", "humor"],
        }
        formatted = quote_dispenser.format_quote(quote)
        self.assertEqual(
            formatted,
            "“Life is what happens when you're busy making other plans.” – John Lennon"
        )

if __name__ == "__main__":
    unittest.main()
