import datetime
import unittest
from unittest.mock import patch

# Mock rationale: we patch datetime.date.today to control the date without network.
# This ensures deterministic behavior for the test.

from forecast import get_forecast


class TestEmojiForecast(unittest.TestCase):
    @patch('forecast.datetime.date')
    def test_fixed_date_forecast(self, mock_date):
        # Mock today's date to 2023-01-01
        mock_date.today.return_value = datetime.date(2023, 1, 1)
        mock_date.isoformat = datetime.date.isoformat
        forecast = get_forecast()
        # Expected forecast based on seed "2023-01-01"
        expected = get_forecast(datetime.date(2023, 1, 1))
        self.assertEqual(forecast, expected)

    def test_consistency_same_date(self):
        date = datetime.date(2025, 12, 25)
        first = get_forecast(date)
        second = get_forecast(date)
        self.assertEqual(first, second)


if __name__ == '__main__':
    unittest.main()
