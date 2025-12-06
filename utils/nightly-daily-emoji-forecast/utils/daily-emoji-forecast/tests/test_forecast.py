import datetime
import unittest
from unittest.mock import patch

from src.forecast import get_forecast

class TestForecast(unittest.TestCase):
    def test_mocked_hash(self):
        # Mock rationale: control the hash output to test index selection.
        with patch('src.forecast._hash_date', return_value=3):
            self.assertEqual(get_forecast(datetime.date(2000, 1, 1)), "🌪️")  # index 3
        with patch('src.forecast._hash_date', return_value=9):
            self.assertEqual(get_forecast(datetime.date(2000, 1, 2)), "🌟")  # index 9

    def test_invalid_input(self):
        # Mock rationale: ensure passing a non‑date raises an AttributeError.
        with self.assertRaises(AttributeError):
            get_forecast("2023-01-01")  # type: ignore

if __name__ == "__main__":
    unittest.main()
