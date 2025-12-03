import unittest
import datetime
from unittest.mock import patch
from src.forecast import get_emoji_forecast, WEATHER_EMOJIS

class TestEmojiForecast(unittest.TestCase):
    def test_mocked_hash(self):
        # Mock rationale: force hash to a known value to test mapping.
        with patch('src.forecast._hash_date', return_value=5):
            # 5 % len(WEATHER_EMOJIS) == 5 -> "🌦️"
            self.assertEqual(
                get_emoji_forecast(datetime.date(2025, 12, 3)),
                "🌦️",
            )

    def test_consistency_without_mock(self):
        # Same date should always yield the same emoji (deterministic).
        date = datetime.date(2023, 7, 15)
        first = get_emoji_forecast(date)
        for _ in range(3):
            self.assertEqual(get_emoji_forecast(date), first)

    def test_invalid_input(self):
        # Mock rationale: ensure passing a non‑date raises an AttributeError when .isoformat is accessed.
        with self.assertRaises(AttributeError):
            get_emoji_forecast("2023-07-15")  # type: ignore[arg-type]

if __name__ == "__main__":
    unittest.main()
