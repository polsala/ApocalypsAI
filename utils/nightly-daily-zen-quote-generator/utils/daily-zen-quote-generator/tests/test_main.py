import unittest
import datetime
from unittest.mock import patch

# Import the function from the sibling ``src`` package.
# The test runner adds the repository root to ``sys.path`` so this works.
from src.main import get_quote, QUOTES

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_deterministic_quote(self):
        """# Mock rationale: ensure the same quote is returned for a fixed date.
        We patch ``datetime.date.today`` to return a known date, making the
        function deterministic without any external state.
        """
        fixed_date = datetime.date(2023, 1, 1)  # known ordinal
        expected_index = fixed_date.toordinal() % len(QUOTES)
        expected_quote = QUOTES[expected_index]
        with patch('datetime.date') as mock_date:
            mock_date.today.return_value = fixed_date
            # ``datetime.date`` must still be callable for other code paths.
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            self.assertEqual(get_quote(), expected_quote)

    def test_wrap_around_behavior(self):
        """# Mock rationale: verify that the modulo operation correctly wraps.
        By choosing a date far in the future we ensure the index cycles.
        """
        far_future = datetime.date(2099, 12, 31)
        expected_index = far_future.toordinal() % len(QUOTES)
        expected_quote = QUOTES[expected_index]
        with patch('datetime.date') as mock_date:
            mock_date.today.return_value = far_future
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            self.assertEqual(get_quote(), expected_quote)

if __name__ == "__main__":
    unittest.main()
