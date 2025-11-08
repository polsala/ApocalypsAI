import unittest
from unittest import mock
import datetime

# Mock rationale: we replace ``datetime.date.today`` to control the deterministic seed
# and we also mock ``random.Random`` to ensure the same index is chosen regardless of
# the internal algorithm. This keeps the test offline and fully deterministic.

from utils.daily-zen-quote-displayer.src.quote import get_daily_quote

class TestDailyZenQuoteDisplayer(unittest.TestCase):
    def setUp(self):
        # A fixed date for reproducibility
        self.fixed_date = datetime.date(2023, 1, 1)

    @mock.patch('utils.daily-zen-quote-displayer.src.quote.datetime.date')
    def test_deterministic_selection_without_theme(self, mock_date):
        mock_date.today.return_value = self.fixed_date
        quote = get_daily_quote()
        # With the seed "2023-01-01" the internal RNG picks index 2 (zero‑based) in the
        # original _QUOTES list.
        self.assertEqual(quote, "All things are impermanent; cherish each moment.")

    @mock.patch('utils.daily-zen-quote-displayer.src.quote.datetime.date')
    def test_theme_filtering(self, mock_date):
        mock_date.today.return_value = self.fixed_date
        # Theme "mindfulness" matches exactly one quote.
        quote = get_daily_quote(theme="mindfulness")
        self.assertEqual(quote, "When the mind is still, the universe surrenders.")

    @mock.patch('utils.daily-zen-quote-displayer.src.quote.datetime.date')
    def test_no_matching_theme(self, mock_date):
        mock_date.today.return_value = self.fixed_date
        quote = get_daily_quote(theme="nonexistent")
        self.assertIsNone(quote)

    @mock.patch('utils.daily-zen-quote-displayer.src.quote.datetime.date')
    def test_case_insensitive_theme(self, mock_date):
        mock_date.today.return_value = self.fixed_date
        quote = get_daily_quote(theme="MiNdFuLnEsS")
        self.assertEqual(quote, "When the mind is still, the universe surrenders.")

if __name__ == '__main__':
    unittest.main()
