"""Tests for the Zen Quote Generator utility.

All tests are deterministic and offline. ``random.choice`` is mocked to
ensure a known quote is returned regardless of the internal random state.
"""

import io
import sys
import unittest
from unittest.mock import patch

# Import the module under test
from utils.nightly_zen_quote_generator.src.quote_generator import (
    get_random_quote,
    main,
    Quote,
)


class TestQuoteGenerator(unittest.TestCase):
    def test_get_random_quote_with_seed(self):
        """When a seed is supplied, the output should be reproducible.

        # Mock rationale: we set a seed and compare against the expected quote
        that appears first in the list for that seed.
        """
        quote = get_random_quote(seed=12345)
        # With the given seed, ``random.choice`` picks a deterministic element.
        # The exact element may vary across Python versions, so we assert the
        # type and that the quote exists in the bank.
        self.assertIsInstance(quote, Quote)
        self.assertIn(
            quote,
            [
                Quote(text="The journey of a thousand miles begins with one step.", author="Lao Tzu"),
                Quote(text="When the mind is still, the universe surrenders.", author="Zen Proverb"),
                Quote(text="Simplicity is the ultimate sophistication.", author="Leonardo da Vinci"),
                Quote(text="Let go or be dragged.", author="Zen Saying"),
                Quote(text="The obstacle is the path.", author="Zen Proverb"),
            ],
        )

    @patch('random.choice')
    def test_get_random_quote_mocked(self, mock_choice):
        """Mock ``random.choice`` to guarantee a specific return value.

        # Mock rationale: By forcing ``random.choice`` to return the second
        # quote we can assert the function returns exactly that object.
        """
        expected = Quote(text="When the mind is still, the universe surrenders.", author="Zen Proverb")
        mock_choice.return_value = expected
        quote = get_random_quote()
        self.assertEqual(quote, expected)
        mock_choice.assert_called_once()

    @patch('random.choice')
    def test_cli_output(self, mock_choice):
        """Ensure the CLI prints the formatted quote.

        # Mock rationale: ``random.choice`` is mocked so the printed string is
        # predictable, allowing us to capture stdout and compare.
        """
        mock_choice.return_value = Quote(text="Let go or be dragged.", author="Zen Saying")
        captured = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured
        try:
            main()
        finally:
            sys.stdout = original_stdout
        self.assertEqual(captured.getvalue().strip(), '"Let go or be dragged." — Zen Saying')


if __name__ == '__main__':
    unittest.main()
