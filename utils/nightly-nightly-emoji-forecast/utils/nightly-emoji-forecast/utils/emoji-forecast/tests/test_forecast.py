import unittest
from unittest.mock import mock_open, patch
from pathlib import Path

from src.forecast import get_forecast, main

class TestEmojiForecast(unittest.TestCase):
    def test_get_forecast_clear(self):
        data = {
            "temperature_c": 23,
            "condition": "clear",
            "precipitation_mm": 0,
        }
        result = get_forecast(data)
        self.assertEqual(result, "🌞 23°C – Clear")

    def test_get_forecast_unknown_condition(self):
        data = {
            "temperature_c": 10,
            "condition": "alien_storm",
            "precipitation_mm": 5,
        }
        result = get_forecast(data)
        # Fallback emoji is 🌈 for unknown conditions
        self.assertEqual(result, "🌈 10°C – Alien Storm (Precip: 5mm)")

    def test_cli_reads_from_file(self):
        mock_json = '{"temperature_c": 15, "condition": "rain", "precipitation_mm": 2}'
        m = mock_open(read_data=mock_json)
        with patch('builtins.open', m), patch('pathlib.Path.is_file', return_value=True):
            # Simulate passing a file path argument
            with patch('src.forecast._load_json_file') as load_mock:
                load_mock.return_value = {
                    "temperature_c": 15,
                    "condition": "rain",
                    "precipitation_mm": 2,
                }
                with patch('sys.stdout') as fake_out:
                    main(["dummy_path.json"])
                    # Capture printed output
                    printed = fake_out.write.call_args[0][0]
                    self.assertIn("🌧️ 15°C – Rain (Precip: 2mm)", printed)

    def test_cli_reads_from_stdin(self):
        mock_json = '{"temperature_c": 30, "condition": "clear", "precipitation_mm": 0}'
        with patch('sys.stdin', new=mock_open(read_data=mock_json)()):
            with patch('sys.stdout') as fake_out:
                main([])
                printed = fake_out.write.call_args[0][0]
                self.assertIn("🌞 30°C – Clear", printed)

if __name__ == "__main__":
    unittest.main()
