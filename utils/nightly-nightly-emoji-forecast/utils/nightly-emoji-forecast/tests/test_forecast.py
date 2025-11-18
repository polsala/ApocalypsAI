import unittest
from unittest.mock import patch
import importlib.util
import pathlib


def load_forecast_module():
    """Dynamically load the forecast module without requiring it to be a package.
    This mirrors how the utility would be imported in a real environment.
    """
    file_path = pathlib.Path(__file__).resolve().parents[2] / "src" / "forecast.py"
    spec = importlib.util.spec_from_file_location("forecast", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestEmojiForecast(unittest.TestCase):
    def setUp(self):
        self.forecast = load_forecast_module()

    @patch.object(load_forecast_module, "_fetch_weather")
    def test_clear_weather(self, mock_fetch):
        # Mock rationale: simulate API returning 'Clear'
        mock_fetch.return_value = "Clear"
        result = self.forecast.get_emoji_forecast("Atlantis")
        self.assertEqual(result, "☀️")

    @patch.object(load_forecast_module, "_fetch_weather")
    def test_rainy_weather(self, mock_fetch):
        mock_fetch.return_value = "Rain"
        result = self.forecast.get_emoji_forecast("Gotham")
        self.assertEqual(result, "🌧️")

    @patch.object(load_forecast_module, "_fetch_weather")
    def test_unknown_weather(self, mock_fetch):
        mock_fetch.side_effect = Exception("Network error")
        result = self.forecast.get_emoji_forecast("Nowhere")
        self.assertEqual(result, "❓")


if __name__ == "__main__":
    unittest.main()
