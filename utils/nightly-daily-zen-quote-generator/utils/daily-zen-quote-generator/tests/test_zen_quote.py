import unittest
from unittest import mock

# Import the module under test
from utils.daily_zen_quote_generator.src import zen_quote

class TestZenQuote(unittest.TestCase):
    def setUp(self):
        # Ensure the internal quote list is in a known state for all tests.
        self.original_quotes = zen_quote._QUOTES.copy()

    def tearDown(self):
        # Restore original quotes to avoid side‑effects between tests.
        zen_quote._QUOTES = self.original_quotes

    def test_random_quote_without_tag(self):
        # Mock ``random.choice`` to always return the first element.
        with mock.patch('random.choice') as mock_choice:
            mock_choice.side_effect = lambda seq: seq[0]  # Mock rationale: deterministic selection for test stability
            quote = zen_quote.get_random_quote()
            self.assertEqual(quote, self.original_quotes[0]["text"])
            mock_choice.assert_called_once()

    def test_random_quote_with_valid_tag(self):
        # Tag 'humor' matches exactly one quote in the collection.
        with mock.patch('random.choice') as mock_choice:
            mock_choice.side_effect = lambda seq: seq[0]
            quote = zen_quote.get_random_quote(tag='humor')
            # The only humor quote is the third entry.
            expected = self.original_quotes[2]["text"]
            self.assertEqual(quote, expected)
            mock_choice.assert_called_once()

    def test_random_quote_with_invalid_tag_raises(self):
        with self.assertRaises(ValueError) as ctx:
            zen_quote.get_random_quote(tag='nonexistent')
        self.assertIn("No quotes found for tag 'nonexistent'", str(ctx.exception))

    def test_cli_output(self):
        # Simulate CLI execution with ``--tag`` argument.
        test_args = ['zen_quote.py', '--tag', 'mindfulness']
        with mock.patch('sys.argv', test_args):
            with mock.patch('builtins.print') as mock_print:
                with mock.patch('random.choice') as mock_choice:
                    mock_choice.side_effect = lambda seq: seq[0]
                    zen_quote.main()
                    # The first mindfulness quote is the first entry.
                    expected = self.original_quotes[0]["text"]
                    mock_print.assert_called_once_with(expected)

if __name__ == '__main__':
    unittest.main()
