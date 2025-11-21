import unittest
from unittest.mock import patch
import datetime

from src.forecast import get_forecast, EMOJIS


class TestEmojiForecast(unittest.TestCase):
    @patch('src.forecast.datetime')
    def test_fixed_date_forecast(self, mock_datetime):
        # Mock today's date to a known value (2023-01-01)
        mock_datetime.date.today.return_value = datetime.date(2023, 1, 1)
        # Ensure other datetime.date constructors still work
        mock_datetime.date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        result = get_forecast()
        self.assertEqual(len(result), 3)  # default count
        for emoji in result:
            self.assertIn(emoji, EMOJIS)

    def test_custom_date(self):
        custom_date = datetime.date(1999, 12, 31)
        result = get_forecast(date=custom_date, count=5)
        self.assertEqual(len(result), 5)
        for emoji in result:
            self.assertIn(emoji, EMOJIS)


if __name__ == '__main__':
    unittest.main()
