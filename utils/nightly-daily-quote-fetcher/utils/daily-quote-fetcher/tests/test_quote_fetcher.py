import unittest
import sys
import os
from unittest.mock import patch

# Adjust import path so that src/ can be imported when tests run.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.quote_fetcher import get_quotes, pick_random

class TestQuoteFetcher(unittest.TestCase):
    def test_get_quotes_all(self):
        all_quotes = get_quotes()
        self.assertEqual(len(all_quotes), 4)  # Mock rationale: known list size

    def test_get_quotes_category(self):
        insp = get_quotes("inspiration")
        self.assertTrue(all(q["category"] == "inspiration" for q in insp))
        self.assertEqual(len(insp), 2)  # Mock rationale: two inspiration quotes

    @patch('src.quote_fetcher.random.choice')
    def test_pick_random_mock(self, mock_choice):
        # Mock rationale: ensure deterministic output
        sample = {"text": "Test quote", "category": "test"}
        mock_choice.return_value = sample
        result = pick_random([sample])
        self.assertEqual(result, sample)

if __name__ == "__main__":
    unittest.main()
