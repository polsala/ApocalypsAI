import unittest
import sys
import os
from datetime import date
from unittest.mock import patch

# Ensure the src directory is on the import path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from forecast import get_forecast, main

class TestEmojiForecast(unittest.TestCase):
    def test_deterministic_forecast(self):
        # Mock rationale: ensure deterministic output for a known date.
        test_date = date(2023, 1, 1)  # ordinal 738156
        forecast = get_forecast(test_date)
        expected = [
            "☀️ Sunny",
            "🌤️ Partly Cloudy",
            "☁️ Cloudy",
            "🌧️ Rainy",
            "⛈️ Stormy",
            "❄️ Snowy",
            "🌪️ Windy",
            "🌈 Rainbow",
        ][test_date.toordinal() % 8]
        self.assertEqual(forecast, expected)

    @patch('forecast.date')
    def test_cli_today(self, mock_date):
        # Mock rationale: simulate today's date without relying on the real clock.
        mock_date.today.return_value = date(2022, 12, 25)  # ordinal 738122
        # Capture stdout
        with patch('sys.stdout') as mock_stdout:
            exit_code = main([])
        self.assertEqual(exit_code, 0)
        expected = [
            "☀️ Sunny",
            "🌤️ Partly Cloudy",
            "☁️ Cloudy",
            "🌧️ Rainy",
            "⛈️ Stormy",
            "❄️ Snowy",
            "🌪️ Windy",
            "🌈 Rainbow",
        ][mock_date.today.return_value.toordinal() % 8]
        # ``print`` adds a newline, so we expect the string plus "\n"
        mock_stdout.write.assert_called_with(expected + "\n")

if __name__ == "__main__":
    unittest.main()
