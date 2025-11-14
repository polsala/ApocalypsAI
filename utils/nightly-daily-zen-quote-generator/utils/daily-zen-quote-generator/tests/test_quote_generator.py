import unittest
import sys
import pathlib
from unittest import mock

# Mock rationale: Add the src directory to sys.path for import without package.
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from quote_generator import get_random_quote, _QUOTES


class TestQuoteGenerator(unittest.TestCase):
    @mock.patch("random.choice", side_effect=lambda seq: seq[0])  # Mock rationale: deterministic first element
    def test_random_without_keyword(self, _):
        quote = get_random_quote()
        self.assertEqual(quote, _QUOTES[0])

    @mock.patch("random.choice", side_effect=lambda seq: seq[-1])  # Mock rationale: deterministic last element
    def test_random_with_keyword(self, _):
        # keyword "peace" matches exactly one quote
        quote = get_random_quote(keyword="peace")
        self.assertIn("peace", quote.lower())

    def test_keyword_no_match(self):
        with self.assertRaises(ValueError) as cm:
            get_random_quote(keyword="nonexistent")
        self.assertIn("No quotes found", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
