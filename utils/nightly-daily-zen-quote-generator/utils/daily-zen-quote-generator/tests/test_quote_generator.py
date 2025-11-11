import unittest
from unittest.mock import patch
import datetime
from src import quote_generator


class TestQuoteGenerator(unittest.TestCase):
    def test_same_date_consistency(self):
        date = datetime.date(2023, 1, 1)
        q1 = quote_generator._select_quote(date)
        q2 = quote_generator._select_quote(date)
        self.assertEqual(q1, q2)

    def test_different_dates_yield_different(self):
        d1 = datetime.date(2023, 1, 1)
        d2 = datetime.date(2023, 1, 2)
        q1 = quote_generator._select_quote(d1)
        q2 = quote_generator._select_quote(d2)
        # Mock rationale: Very unlikely to collide for two consecutive dates
        self.assertNotEqual(q1, q2)

    @patch('src.quote_generator._select_quote')
    @patch('src.quote_generator.datetime')
    def test_cli_output(self, mock_datetime, mock_select):
        mock_datetime.date.today.return_value = datetime.date(2022, 12, 25)
        mock_select.return_value = "Mocked zen."
        with patch('sys.stdout') as mock_stdout:
            quote_generator.main()
            mock_stdout.write.assert_called_once_with("Mocked zen.\n")


if __name__ == '__main__':
    unittest.main()
