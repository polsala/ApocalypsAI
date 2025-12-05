"""Tests for Quip Quotient Quoter with deterministic mocks."""
import json
import unittest
import random
from pathlib import Path
from unittest.mock import patch

from quoter import generate_quote, batch_quotes, export_quotes


class TestQuoter(unittest.TestCase):
    """Test suite with mocked randomness for deterministic results."""

    def setUp(self) -> None:
        self.temp_dir = Path(__file__).parent / 'temp'
        self.temp_dir.mkdir(exist_ok=True)

    def tearDown(self) -> None:
        # Clean up temp files
        for p in self.temp_dir.iterdir():
            if p.is_file():
                p.unlink()
        self.temp_dir.rmdir()

    @patch('quoter.random.choice')
    def test_generate_quote_deterministic(self, mock_choice):
        """Mock rationale: Freeze randomness to verify exact output."""
        expected_quote = "Logic is the beginning of wisdom, not the end. – ApocalypsAI"
        mock_choice.return_value = expected_quote

        result = generate_quote()

        self.assertEqual(result['quote'], expected_quote)
        self.assertEqual(result['category'], 'whimsical-dev')
        self.assertEqual(result['source'], 'mock-llm')

    @patch('quoter.generate_quote')
    def test_batch_quotes(self, mock_generate):
        """Mock rationale: Simulate three identical quotes to verify list length."""
        mock_generate.return_value = {'quote': 'Test quote', 'category': 'dev', 'source': 'mock'}

        result = batch_quotes(3)

        self.assertEqual(len(result), 3)
        for item in result:
            self.assertEqual(item['quote'], 'Test quote')

    def test_export_quotes(self):
        """Verify JSON file creation and content."""
        quotes = [
            {'quote': 'First quote', 'category': 'a', 'source': 'mock'},
            {'quote': 'Second quote', 'category': 'b', 'source': 'mock'}
        ]
        output_path = self.temp_dir / 'test_quotes.json'

        export_quotes(quotes, output_path)

        self.assertTrue(output_path.exists())
        with open(output_path) as f:
            data = json.load(f)
        self.assertEqual(data, quotes)


if __name__ == '__main__':
    unittest.main()
