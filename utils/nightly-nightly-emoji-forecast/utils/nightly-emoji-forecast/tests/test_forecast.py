import sys
import pathlib
import unittest
from unittest.mock import patch, Mock

# Ensure the src directory is on the import path for the test run.
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from forecast import get_emoji_forecast


class TestEmojiForecast(unittest.TestCase):
    @patch('forecast.requests.get')
    def test_freezing(self, mock_get):
        # Mock rationale: simulate API returning -5°C
        mock_resp = Mock()
        mock_resp.json.return_value = {"temperature_c": -5}
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp
        self.assertEqual(get_emoji_forecast("Reykjavik"), "🥶")

    @patch('forecast.requests.get')
    def test_mild(self, mock_get):
        mock_resp = Mock()
        mock_resp.json.return_value = {"temperature_c": 15}
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp
        self.assertEqual(get_emoji_forecast("London"), "🌤️")

    @patch('forecast.requests.get')
    def test_hot(self, mock_get):
        mock_resp = Mock()
        mock_resp.json.return_value = {"temperature_c": 35}
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp
        self.assertEqual(get_emoji_forecast("Dubai"), "🔥")


if __name__ == "__main__":
    unittest.main()
