import unittest
import sys
import pathlib
from unittest.mock import patch

# Add src directory to sys.path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from main import get_zen_quote


class TestZenQuoteGenerator(unittest.TestCase):
    def test_random_quote_mocked(self):
        with patch("random.choice", lambda seq: seq[0]):  # Mock rationale: deterministic first element
            quote = get_zen_quote()
            self.assertEqual(quote, "The journey of a thousand miles begins with one step.")

    def test_theme_filter_mocked(self):
        with patch("random.choice", lambda seq: seq[0]):  # Mock rationale: deterministic first element
            quote = get_zen_quote(theme="mindfulness")
            self.assertEqual(quote, "When the mind is still, the universe surrenders.")

    def test_invalid_theme(self):
        with self.assertRaises(ValueError) as cm:
            get_zen_quote(theme="nonexistent")
        self.assertIn("No quotes found for theme", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
