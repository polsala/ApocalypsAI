import unittest
from unittest.mock import mock_open, patch

# Mock rationale: we avoid filesystem I/O by patching builtins.open with a deterministic string.

from src.analyzer import count_words, top_n, markdown_table

class TestWordFrequencyAnalyzer(unittest.TestCase):
    def test_count_words_basic(self):
        text = "Hello, hello! World? world world."
        expected = {"hello": 2, "world": 3}
        self.assertEqual(count_words(text), expected)

    def test_top_n_ordering(self):
        counter = {"apple": 5, "banana": 5, "cherry": 2}
        # Should sort by count desc, then alphabetically for ties.
        expected = [("apple", 5), ("banana", 5), ("cherry", 2)]
        self.assertEqual(top_n(counter, 3), expected)

    def test_markdown_table_format(self):
        pairs = [("foo", 3), ("bar", 1)]
        md = markdown_table(pairs)
        lines = md.splitlines()
        self.assertEqual(lines[0], "| Word | Count |")
        self.assertEqual(lines[1], "|------|-------|")
        self.assertIn("| foo | 3 |", lines)
        self.assertIn("| bar | 1 |", lines)

    @patch("builtins.open", new_callable=mock_open, read_data="Alpha beta alpha. Beta! Gamma?")
    def test_integration_via_file_read(self, mock_file):
        # Simulate reading from a file path using Path.read_text which internally calls open.
        from pathlib import Path
        path = Path("dummy.txt")
        # Path.read_text will use the patched open.
        text = path.read_text()
        self.assertEqual(count_words(text), {"alpha": 2, "beta": 2, "gamma": 1})
        mock_file.assert_called_once_with("dummy.txt", "r", encoding="utf-8")

if __name__ == "__main__":
    unittest.main()
