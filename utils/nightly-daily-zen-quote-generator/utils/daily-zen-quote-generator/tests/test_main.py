import unittest
from unittest.mock import patch
import datetime
import sys
import os

# Add the src directory to ``sys.path`` so we can import ``main`` directly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from main import get_quote


class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_fixed_date(self):
        """Ensure a known date returns the expected quote."""
        test_date = datetime.date(2023, 1, 1)  # ordinal 738156, 738156 % 5 == 1
        expected = "🌱 “Be yourself; everyone else is already taken.” – Oscar Wilde"
        self.assertEqual(get_quote(test_date), expected)

    @patch('main.datetime')
    def test_today_mocked(self, mock_datetime):
        """Mock ``datetime.date.today`` to control output.

        # Mock rationale: we replace ``today()`` to return a fixed date for deterministic test.
        """
        mock_today = datetime.date(2023, 1, 5)  # ordinal 738160, 738160 % 5 == 0
        mock_datetime.date.today.return_value = mock_today
        # Ensure other ``datetime.date`` constructors still work.
        mock_datetime.date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        expected = "🌿 “The only true wisdom is in knowing you know nothing.” – Socrates"
        self.assertEqual(get_quote(), expected)


if __name__ == "__main__":
    unittest.main()
