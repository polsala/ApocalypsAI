import pathlib
import sys
import unittest
from unittest.mock import patch

# Ensure the src directory is on the import path.
# Mock rationale: adds the utility's src folder without external dependencies.
utils_root = pathlib.Path(__file__).resolve().parents[1]
src_path = utils_root / "src"
sys.path.append(str(src_path))

from quote_generator import get_random_quote, QUOTES


class TestQuoteGenerator(unittest.TestCase):
    def test_random_quote_no_theme(self):
        # Mock rationale: deterministic selection of the first quote.
        with patch("random.choice", return_value=QUOTES[0]) as mock_choice:
            quote = get_random_quote()
            self.assertEqual(quote, QUOTES[0])
            mock_choice.assert_called_once()

    def test_random_quote_with_theme(self):
        # Mock rationale: deterministic selection from the filtered list.
        with patch("random.choice", return_value=QUOTES[1]) as mock_choice:
            quote = get_random_quote(theme="mindfulness")
            self.assertEqual(quote, QUOTES[1])
            mock_choice.assert_called_once()

    def test_invalid_theme(self):
        with self.assertRaises(ValueError) as cm:
            get_random_quote(theme="nonexistent")
        self.assertIn("No quotes found for theme", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
