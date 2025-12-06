import unittest
import os
from unittest.mock import patch, MagicMock
import requests
from src.app import get_weather_data, format_weather_report

class TestWastelandWeatherStation(unittest.TestCase):

    # Mock rationale: We need to test the `get_weather_data` function without making actual external HTTP requests
    # to the OpenWeatherMap API. Mocking `requests.get` allows us to control the API response, ensuring
    # deterministic and offline tests.
    @patch('requests.get')
    def test_get_weather_data_by_location_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "coord": {"lon": -0.13, "lat": 51.51},
            "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
            "base": "stations",
            "main": {"temp": 20.0, "feels_like": 19.5, "temp_min": 18.0, "temp_max": 22.0, "pressure": 1012, "humidity": 70},
            "visibility": 10000,
            "wind": {"speed": 3.6, "deg": 270},
            "clouds": {"all": 0},
            "dt": 1678886400,
            "sys": {"type": 1, "id": 1414, "country": "GB", "sunrise": 1678860000, "sunset": 1678900000},
            "timezone": 0,
            "id": 2643743,
            "name": "London",
            "cod": 200
        }
        mock_get.return_value = mock_response

        api_key = "test_api_key"
        location = "London"
        data = get_weather_data(api_key, location=location)

        mock_get.assert_called_once_with(
            "http://api.openweathermap.org/data/2.5/weather",
            params={"appid": api_key, "units": "metric", "q": location}
        )
        self.assertIn("name", data)
        self.assertEqual(data["name"], "London")

    # Mock rationale: Similar to the above, we mock `requests.get` to simulate an API call failure
    # (e.g., network error, invalid API key) without actually hitting the network. This allows us to test
    # error handling paths deterministically.
    @patch('requests.get')
    def test_get_weather_data_api_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("API is down")

        api_key = "test_api_key"
        location = "InvalidCity"

        with self.assertRaises(SystemExit) as cm:
            get_weather_data(api_key, location=location)
        self.assertEqual(cm.exception.code, 1)

    def test_get_weather_data_no_location_or_coords(self):
        api_key = "test_api_key"
        with self.assertRaises(ValueError):
            get_weather_data(api_key)

    def test_format_weather_report_clear_sky(self):
        data = {
            "name": "Sunnyville",
            "weather": [{"description": "clear sky"}],
            "main": {"temp": 30.0, "feels_like": 32.0, "humidity": 40},
            "wind": {"speed": 5.0, "deg": 180}
        }
        report = format_weather_report(data)
        self.assertIn("Location: Sunnyville", report)
        self.assertIn("Conditions: Clear sky ☀️", report)
        self.assertIn("Temperature: 30°C (Feels like: 32°C)", report)
        self.assertIn("Wind: 18 km/h S", report)
        self.assertIn("Humidity: 40%", report)

    def test_format_weather_report_dust_storm(self):
        data = {
            "name": "Dusty Flats",
            "weather": [{"description": "dust storm"}],
            "main": {"temp": 45.0, "feels_like": 50.0, "humidity": 10},
            "wind": {"speed": 15.0, "deg": 45}
        }
        report = format_weather_report(data)
        self.assertIn("Location: Dusty Flats", report)
        self.assertIn("Conditions: Dust storm 🌪️", report)
        self.assertIn("Temperature: 45°C (Feels like: 50°C)", report)
        self.assertIn("Wind: 54 km/h NE", report)
        self.assertIn("Humidity: 10%", report)

    def test_format_weather_report_incomplete_data(self):
        data = {
            "name": "Broken Data",
            "weather": [{"description": "partly cloudy"}]
        }
        report = format_weather_report(data)
        self.assertEqual(report, "ERROR: Incomplete weather data received.")

    def test_format_weather_report_unknown_wasteland(self):
        data = {
            "weather": [{"description": "overcast clouds"}],
            "main": {"temp": 10.0, "feels_like": 8.0, "humidity": 90},
            "wind": {"speed": 2.0, "deg": 0}
        }
        report = format_weather_report(data)
        self.assertIn("Location: Unknown Wasteland", report)
        self.assertIn("Conditions: Overcast clouds ☁️", report)

if __name__ == '__main__':
    unittest.main()
