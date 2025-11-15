import unittest
import datetime
import sys
import os
from unittest.mock import patch

# Mock rationale: we patch ``datetime.date.today`` to return a fixed date,
# ensuring deterministic output without external dependencies.

# Ensure the ``src`` directory is on ``sys.path`` so we can import ``main``.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from main import get_quote_of_the_day

class TestQuoteOfTheDay(unittest.TestCase):
    def test_fixed_date(self):
        fixed_date = datetime.date(2023, 1, 1)  # ordinal 738156
        expected_index = fixed_date.toordinal() % 8  # len(_QUOTES) == 8
        expected_quotes = [
            "The journey of a thousand miles begins with one step.",
            "When the mind is still, the universe surrenders.",
            "Simplicity is the ultimate sophistication.",
            "The obstacle is the path.",
            "Let go or be dragged.",
            "Silence is a source of great strength.",
            "Know the rules well, so you can break them.",
            "The only constant is change.",
        ]
        expected_quote = expected_quotes[expected_index]

        with patch('datetime.date') as mock_date:
            mock_date.today.return_value = fixed_date
            # ``datetime.date`` needs to be callable for other usages
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            quote = get_quote_of_the_day()
            self.assertEqual(quote, expected_quote)

    def test_custom_date_argument(self):
        # Directly pass a date without mocking
        date = datetime.date(2025, 12, 31)
        index = date.toordinal() % 8
        expected_quotes = [
            "The journey of a thousand miles begins with one step.",
            "When the mind is still, the universe surrenders.",
            "Simplicity is the ultimate sophistication.",
            "The obstacle is the path.",
            "Let go or be dragged.",
            "Silence is a source of great strength.",
            "Know the rules well, so you can break them.",
            "The only constant is change.",
        ]
        expected_quote = expected_quotes[index]
        self.assertEqual(get_quote_of_the_day(date), expected_quote)

if __name__ == "__main__":
    unittest.main()
