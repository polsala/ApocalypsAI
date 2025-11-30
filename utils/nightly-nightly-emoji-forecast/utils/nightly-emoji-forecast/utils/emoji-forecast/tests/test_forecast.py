import datetime
import unittest
from unittest import mock

from src.forecast import get_forecast


class TestEmojiForecast(unittest.TestCase):
    @mock.patch('src.forecast._hash_date')
    def test_mocked_hash(self, mock_hash):
        # Mock rationale: force the hash to a known value so the forecast is predictable.
        mock_hash.return_value = 5  # Index 5 corresponds to "🌦️" in the emoji list.
        date = datetime.date(2023, 1, 1)
        self.assertEqual(get_forecast(date), "🌦️")


if __name__ == "__main__":
    unittest.main()
