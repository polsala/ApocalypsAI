import unittest
from unittest.mock import patch
from src.forecast import get_emoji_forecast

class TestEmojiForecast(unittest.TestCase):
    @patch('src.forecast._hash_date')
    def test_deterministic_output(self, mock_hash):
        # Mock hash returns a known value
        mock_hash.return_value = 0x123456789ABCDEF
        seed = 0x123456789ABCDEF
        emojis = ["☀️", "🌤️", "⛅️", "🌥️", "☁️", "🌧️", "⛈️", "🌩️", "🌨️", "❄️", "🌈", "☔️"]
        expected = "".join([
            emojis[(seed >> (i * 8)) % len(emojis)] for i in range(3)
        ])
        self.assertEqual(get_emoji_forecast("2025-01-01"), expected)

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            get_emoji_forecast("2025/01/01")

if __name__ == "__main__":
    unittest.main()
