import unittest
import datetime
import sys
import os
from unittest.mock import patch

# Add the src directory to sys.path so we can import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))
from quote_of_the_day import get_quote

class TestQuoteOfTheDay(unittest.TestCase):
    def test_deterministic_today(self):
        # Mock today's date to a known value (2023-01-01)
        fixed_date = datetime.date(2023, 1, 1)  # ordinal 738156, 738156 % 8 == 4
        with patch('datetime.date') as mock_date:
            mock_date.today.return_value = fixed_date
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            quote = get_quote()
        expected = "Life is short. Smile while you still have teeth."
        self.assertEqual(quote, expected)

    def test_custom_date(self):
        # Use a custom date (1999-12-31) -> ordinal 730119, 730119 % 8 == 7
        custom_date = datetime.date(1999, 12, 31)
        quote = get_quote(custom_date)
        expected = "Debugging: Being the detective in a crime movie where you are also the murderer."
        self.assertEqual(quote, expected)

if __name__ == "__main__":
    unittest.main()
