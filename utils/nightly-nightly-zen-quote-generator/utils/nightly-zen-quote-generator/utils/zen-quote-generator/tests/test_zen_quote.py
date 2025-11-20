import unittest
import sys
import pathlib

# Mock rationale: we patch random.choice to return a deterministic quote,
# ensuring the test is deterministic and offline.

# Adjust sys.path so the src module can be imported without package name constraints.
src_path = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

import zen_quote
from unittest.mock import patch

class TestZenQuote(unittest.TestCase):
    def test_filter_no_tag_returns_all(self):
        all_quotes = zen_quote._filter_quotes(None)
        self.assertGreaterEqual(len(all_quotes), 1)

    def test_filter_specific_tag(self):
        mindfulness = zen_quote._filter_quotes("mindfulness")
        self.assertTrue(all("mindfulness" in q["tags"] for q in mindfulness))
        self.assertGreaterEqual(len(mindfulness), 1)

    def test_filter_unknown_tag_raises(self):
        with self.assertRaises(ValueError):
            zen_quote._filter_quotes("nonexistent")

    @patch("random.choice")
    def test_get_random_quote_deterministic(self, mock_choice):
        # Mock rationale: force a known quote to be returned.
        sample = {"text": "Test quote", "author": "Tester", "tags": []}
        mock_choice.return_value = sample
        quote = zen_quote.get_random_quote()
        self.assertEqual(quote, sample)

    def test_format_quote(self):
        quote = {"text": "Hello", "author": "World"}
        self.assertEqual(zen_quote.format_quote(quote), "“Hello” – World")

if __name__ == "__main__":
    unittest.main()
