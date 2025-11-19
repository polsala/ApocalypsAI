import unittest
from unittest import mock
from pathlib import Path

# Import the module under test
from utils.nightly-emoji-forecast.src.main import (
    condition_to_emoji,
    build_emoji_forecast,
    load_weather_data,
    MOCK_WEATHER,
)

class TestEmojiForecast(unittest.TestCase):
    def test_condition_to_emoji_exact_match(self):
        self.assertEqual(condition_to_emoji("clear"), "🌞")
        self.assertEqual(condition_to_emoji("Rain"), "☔️")
        self.assertEqual(condition_to_emoji("PARTLY CLOUDY"), "⛅")

    def test_condition_to_emoji_substring_match(self):
        # "light rain" contains "rain"
        self.assertEqual(condition_to_emoji("light rain"), "☔️")
        # "snow showers" contains "snow"
        self.assertEqual(condition_to_emoji("snow showers"), "❄️")

    def test_condition_to_emoji_unknown(self):
        self.assertEqual(condition_to_emoji("alien invasion"), "❓")

    def test_build_emoji_forecast(self):
        sample = {
            "forecast": [
                {"time": "morning", "condition": "clear"},
                {"time": "afternoon", "condition": "rain"},
                {"time": "evening", "condition": "snow"},
            ]
        }
        expected = ["🌞", "☔️", "❄️"]
        self.assertEqual(build_emoji_forecast(sample), expected)

    def test_load_weather_data_with_path(self):
        # Mock JSON content
        mock_json = {"forecast": [{"time": "noon", "condition": "cloudy"}]}
        mock_path = mock.Mock(spec=Path)
        mock_path.open.return_value.__enter__.return_value.read.return_value = "{}".format(
            json.dumps(mock_json)
        )
        # # Mock rationale: we replace the file read with a controlled JSON string.
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(mock_json))):
            data = load_weather_data(Path("dummy.json"))
        self.assertEqual(data, mock_json)

    def test_load_weather_data_without_path_returns_mock(self):
        self.assertEqual(load_weather_data(None), MOCK_WEATHER)

if __name__ == "__main__":
    unittest.main()
