import unittest
from unittest.mock import patch

from src.emoji_forecast import get_emoji_forecast, _fetch_weather


class TestEmojiForecast(unittest.TestCase):
    def test_known_weather(self):
        # Mock the internal weather fetch to return a known condition
        with patch('src.emoji_forecast._fetch_weather', return_value='rainy'):
            self.assertEqual(get_emoji_forecast('2023-10-31', 'Paris'), '🌧️')

    def test_unknown_weather_fallback(self):
        with patch('src.emoji_forecast._fetch_weather', return_value='alien'):
            self.assertEqual(get_emoji_forecast('2023-10-31', 'Mars'), '❓')

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            get_emoji_forecast('31-10-2023', 'Berlin')

    def test_fetch_weather_deterministic(self):
        # Ensure the mock provider returns the same result for identical inputs
        w1 = _fetch_weather('2023-01-01', 'Tokyo')
        w2 = _fetch_weather('2023-01-01', 'Tokyo')
        self.assertEqual(w1, w2)


if __name__ == '__main__':
    unittest.main()
