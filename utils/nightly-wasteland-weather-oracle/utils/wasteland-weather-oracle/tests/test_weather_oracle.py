import unittest
from unittest.mock import patch, MagicMock
import io
import sys
from utils.wasteland_weather_oracle.src import weather_oracle

class TestWastelandWeatherOracle(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        self.mock_stdout = io.StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('utils.wasteland_weather_oracle.src.weather_oracle._mock_weather_api_call')
    def test_main_with_location(self, mock_api_call):
        # Mock rationale: We are testing the CLI entry point and its interaction
        # with the weather data retrieval. Mocking the external (or simulated external)
        # API call ensures the test is deterministic and doesn't rely on network access.
        mock_api_call.return_value = {
            "name": "Testville",
            "main": {"temp": 290.15}, # ~17C
            "weather": [{"id": 800, "description": "clear sky"}],
            "wind": {"speed": 3.0} # ~10.8 kph
        }

        test_args = ['--location', 'Testville']
        with patch('sys.argv', ['weather_oracle.py'] + test_args):
            weather_oracle.main()
            output = self.mock_stdout.getvalue()
            self.assertIn("--- Wasteland Weather Report for Testville ---", output)
            self.assertIn("Conditions: Mild, but don't get complacent. Clear skies, but watch for raiders and mutated wildlife.", output)
            self.assertIn("Wind: A gentle, eerie breeze.", output)

    @patch('utils.wasteland_weather_oracle.src.weather_oracle._mock_weather_api_call')
    def test_main_with_coordinates(self, mock_api_call):
        # Mock rationale: Similar to the location test, this ensures the coordinate
        # parsing and subsequent logic work correctly without actual API calls.
        mock_api_call.return_value = {
            "name": "Coordinate City",
            "main": {"temp": 270.15}, # ~-3C
            "weather": [{"id": 600, "description": "light snow"}],
            "wind": {"speed": 7.0} # ~25.2 kph
        }

        test_args = ['--lat', '10.0', '--lon', '20.0']
        with patch('sys.argv', ['weather_oracle.py'] + test_args):
            weather_oracle.main()
            output = self.mock_stdout.getvalue()
            self.assertIn("--- Wasteland Weather Report for Coordinate City ---", output)
            self.assertIn("Conditions: Chilly winds. Blizzard conditions, visibility near zero.", output)
            self.assertIn("Wind: Gusty winds, secure your scavenged goods.", output)

    def test_main_no_args_error(self):
        # Mock rationale: Testing argument parsing errors doesn't require API mocks.
        # We expect a SystemExit (from argparse.error) and an error message to stderr.
        test_args = []
        with patch('sys.argv', ['weather_oracle.py'] + test_args),
             self.assertRaises(SystemExit) as cm,
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            weather_oracle.main()
            self.assertEqual(cm.exception.code, 2) # argparse exits with 2 for usage errors
            self.assertIn("error: Either --location or both --lat and --lon must be provided.", mock_stderr.getvalue())

    def test_get_apocalyptic_description_clear_hot(self):
        # Mock rationale: Directly testing the interpretation logic with predefined
        # weather data ensures the translation rules are applied correctly.
        mock_data = {
            "name": "Desert Outpost",
            "main": {"temp": 305.15}, # 32C
            "weather": [{"id": 800, "description": "clear sky"}],
            "wind": {"speed": 2.5} # 9 kph
        }
        result = weather_oracle._get_apocalyptic_description(mock_data)
        self.assertIn("--- Wasteland Weather Report for Desert Outpost ---", result)
        self.assertIn("Conditions: Scorching sun. Clear skies, but watch for raiders and mutated wildlife.", result)
        self.assertIn("Wind: A gentle, eerie breeze.", result)

    def test_get_apocalyptic_description_rain_chilly(self):
        mock_data = {
            "name": "Swamp Hideout",
            "main": {"temp": 278.15}, # 5C
            "weather": [{"id": 501, "description": "moderate rain"}],
            "wind": {"speed": 15.0} # 54 kph
        }
        result = weather_oracle._get_apocalyptic_description(mock_data)
        self.assertIn("--- Wasteland Weather Report for Swamp Hideout ---", result)
        self.assertIn("Conditions: Chilly winds. Heavy acid downpour, seek immediate shelter!", result)
        self.assertIn("Wind: Gale force winds, shelter immediately or risk being blown away!", result)

    def test_get_apocalyptic_description_thunderstorm_mild(self):
        mock_data = {
            "name": "Ruined City",
            "main": {"temp": 288.15}, # 15C
            "weather": [{"id": 201, "description": "thunderstorm with light rain"}],
            "wind": {"speed": 8.0} # 28.8 kph
        }
        result = weather_oracle._get_apocalyptic_description(mock_data)
        self.assertIn("--- Wasteland Weather Report for Ruined City ---", result)
        self.assertIn("Conditions: Mild, but don't get complacent. Electrical storms rage, avoid high ground!", result)
        self.assertIn("Wind: Gusty winds, secure your scavenged goods.", result)

    def test_get_apocalyptic_description_fog_cold(self):
        mock_data = {
            "name": "Forgotten Bunker",
            "main": {"temp": 260.15}, # -13C
            "weather": [{"id": 741, "description": "fog"}],
            "wind": {"speed": 4.0} # 14.4 kph
        }
        result = weather_oracle._get_apocalyptic_description(mock_data)
        self.assertIn("--- Wasteland Weather Report for Forgotten Bunker ---", result)
        self.assertIn("Conditions: Freezing wastes. Toxic fog/dust/ash cloud rolling in, don your respirators!", result)
        self.assertIn("Wind: Gusty winds, secure your scavenged goods.", result)

    def test_get_apocalyptic_description_tornado(self):
        mock_data = {
            "name": "Tornado Alley",
            "main": {"temp": 295.15}, # 22C
            "weather": [{"id": 781, "description": "tornado"}],
            "wind": {"speed": 20.0} # 72 kph
        }
        result = weather_oracle._get_apocalyptic_description(mock_data)
        self.assertIn("--- Wasteland Weather Report for Tornado Alley ---", result)
        self.assertIn("Conditions: Scorching sun. Twister inbound! Find deep shelter NOW!", result)
        self.assertIn("Wind: Gale force winds, shelter immediately or risk being blown away!", result)

    def test_get_apocalyptic_description_dust_devils(self):
        mock_data = {
            "name": "Dust Bowl",
            "main": {"temp": 300.15}, # 27C
            "weather": [{"id": 731, "description": "dust"}],
            "wind": {"speed": 18.0} # 64.8 kph
        }
        result = weather_oracle._get_apocalyptic_description(mock_data)
        self.assertIn("--- Wasteland Weather Report for Dust Bowl ---", result)
        self.assertIn("Conditions: Scorching sun. Dust devils brewing, visibility low, don your respirators!", result)
        self.assertIn("Wind: Gale force winds, shelter immediately or risk being blown away!", result)

    def test_get_apocalyptic_description_overcast(self):
        mock_data = {
            "name": "Cloudy Peaks",
            "main": {"temp": 283.15}, # 10C
            "weather": [{"id": 803, "description": "broken clouds"}],
            "wind": {"speed": 6.0} # 21.6 kph
        }
        result = weather_oracle._get_apocalyptic_description(mock_data)
        self.assertIn("--- Wasteland Weather Report for Cloudy Peaks ---", result)
        self.assertIn("Conditions: Mild, but don't get complacent. Overcast, good for stealth, but watch for aerial threats.", result)
        self.assertIn("Wind: Gusty winds, secure your scavenged goods.", result)


if __name__ == '__main__':
    unittest.main()
