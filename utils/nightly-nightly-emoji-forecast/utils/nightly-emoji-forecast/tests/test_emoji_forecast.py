import unittest
from unittest.mock import patch
from src.emoji_forecast import forecast, WEATHER_EMOJIS

class TestEmojiForecast(unittest.TestCase):
    def test_mocked_hash(self):
        # Mock rationale: force a known hash value to test mapping logic.
        with patch('src.emoji_forecast._hash_date', return_value=7):
            self.assertEqual(forecast('any-date'), WEATHER_EMOJIS[7])

    def test_consistency(self):
        date = "2023-07-04"
        self.assertEqual(forecast(date), forecast(date))

if __name__ == "__main__":
    unittest.main()
