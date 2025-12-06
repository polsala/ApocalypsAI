import unittest
from datetime import date

# Mock rationale: No external services are called; all logic is pure and deterministic.

from utils.nightly-emoji_weather.src.weather import get_weather_emoji

class TestWeatherEmoji(unittest.TestCase):
    def test_known_dates(self):
        # A few hand‑picked dates with expected emojis computed via the same algorithm.
        test_cases = [
            ("2023-01-01", self._expected("2023-01-01")),
            ("2023-12-25", self._expected("2023-12-25")),
            ("2000-02-29", self._expected("2000-02-29")),
            (date.today().isoformat(), self._expected(date.today().isoformat())),
        ]
        for input_date, expected in test_cases:
            with self.subTest(date=input_date):
                self.assertEqual(get_weather_emoji(input_date), expected)

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            get_weather_emoji("31-12-2023")  # wrong order
        with self.assertRaises(ValueError):
            get_weather_emoji("2023/12/31")  # wrong separator
        with self.assertRaises(ValueError):
            get_weather_emoji("not-a-date")

    @staticmethod
    def _expected(date_str: str) -> str:
        """Calculate the expected emoji using the same deterministic rule.

        This mirrors the implementation but is kept separate to make the intention clear.
        """
        from utils.nightly-emoji_weather.src.weather import _parse_date, _EMOJIS
        d = _parse_date(date_str)
        idx = d.toordinal() % len(_EMOJIS)
        return _EMOJIS[idx]

if __name__ == "__main__":
    unittest.main()
