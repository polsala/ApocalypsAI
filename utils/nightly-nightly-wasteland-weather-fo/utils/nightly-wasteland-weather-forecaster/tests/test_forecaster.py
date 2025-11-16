import unittest
import unittest.mock as mock
from datetime import datetime, timedelta
import sys
import io
import os

# Add the src directory to the path for importing forecaster
# Mock rationale: This ensures the test can find the module to be tested
# when run from the utility's root directory as per instructions.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from forecaster import WastelandForecaster
sys.path.pop(0)

class TestWastelandForecaster(unittest.TestCase):

    def setUp(self):
        self.forecaster = WastelandForecaster()

    @mock.patch('random.choice')
    @mock.patch('random.randint')
    def test_get_forecast_deterministic(self, mock_randint, mock_choice):
        # Mock rationale: Ensure deterministic output for random selections.
        # We control the 'random' choices to predict the exact forecast.
        mock_choice.side_effect = [
            # Day 1
            ("Chilly", 1, 10), # temperature
            ("Moderate", "Geiger counter clicking steadily"), # radiation
            "Overcast", # conditions
            "Gusty (Watch for flying debris!)", # wind
            "Mutant Swarm Alert - Stay Indoors!", # special_event
            # Day 2
            ("Scorching Hot", 31, 40), # temperature
            ("Low", "Safe for short excursions"), # radiation
            "Clear Skies", # conditions
            "Calm", # wind
            "Scavenger's Luck - Increased chance of finding useful scrap!", # special_event
            # Day 3
            ("Bone-Chilling Cold", -10, 0), # temperature
            ("High - Seek Shelter!", "Geiger counter screaming!"), # radiation
            "Radiation Storm", # conditions
            "Howling Winds (Structural damage possible!)", # wind
            "None" # special_event
        ]
        mock_randint.side_effect = [5, 35, -5] # temperatures for Day 1, 2, 3

        location = "Test Location"
        days = 3
        forecast = self.forecaster.get_forecast(location, days)

        self.assertEqual(len(forecast), days)

        # Verify Day 1
        self.assertEqual(forecast[0]["conditions"], "Overcast")
        self.assertEqual(forecast[0]["temperature"], "Chilly (5°C / 41°F)")
        self.assertEqual(forecast[0]["radiation"], "Moderate (Geiger counter clicking steadily)")
        self.assertEqual(forecast[0]["wind"], "Gusty (Watch for flying debris!)")
        self.assertEqual(forecast[0]["special_event"], "Mutant Swarm Alert - Stay Indoors!")

        # Verify Day 2
        self.assertEqual(forecast[1]["conditions"], "Clear Skies")
        self.assertEqual(forecast[1]["temperature"], "Scorching Hot (35°C / 95°F)")
        self.assertEqual(forecast[1]["radiation"], "Low (Safe for short excursions)")
        self.assertEqual(forecast[1]["wind"], "Calm")
        self.assertEqual(forecast[1]["special_event"], "Scavenger's Luck - Increased chance of finding useful scrap!")

        # Verify Day 3
        self.assertEqual(forecast[2]["conditions"], "Radiation Storm")
        self.assertEqual(forecast[2]["temperature"], "Bone-Chilling Cold (-5°C / 23°F)")
        self.assertEqual(forecast[2]["radiation"], "High - Seek Shelter! (Geiger counter screaming!)")
        self.assertEqual(forecast[2]["wind"], "Howling Winds (Structural damage possible!)")
        self.assertEqual(forecast[2]["special_event"], "None")

    @mock.patch('random.choice')
    @mock.patch('random.randint')
    def test_run_output_format(self, mock_randint, mock_choice):
        # Mock rationale: Capture and verify the console output format.
        # We control random choices to ensure predictable output for comparison.
        mock_choice.side_effect = [
            # Day 1
            ("Chilly", 1, 10), # temperature
            ("Moderate", "Geiger counter clicking steadily"), # radiation
            "Overcast", # conditions
            "Gusty (Watch for flying debris!)", # wind
            "Mutant Swarm Alert - Stay Indoors!", # special_event
        ]
        mock_randint.side_effect = [5] # temperature for Day 1

        location = "Test Outpost"
        days = 1

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Mock datetime.now() to ensure consistent date in output
        # Mock rationale: Make the date in the output deterministic for testing.
        with mock.patch('forecaster.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2077, 10, 23) # A fitting date
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow normal datetime operations
            mock_dt.timedelta = timedelta # Ensure timedelta works
            self.forecaster.run(location, days)

        sys.stdout = sys.__stdout__ # Restore stdout

        expected_output = (
            f"Forecasting for {location} for {days} days:\n\n"
            f"Day 1 (2077-10-23):\n"
            f"  Conditions: Overcast\n"
            f"  Temperature: Chilly (5°C / 41°F)\n"
            f"  Radiation: Moderate (Geiger counter clicking steadily)\n"
            f"  Wind: Gusty (Watch for flying debris!)\n"
            f"  Special Event: Mutant Swarm Alert - Stay Indoors!\n\n"
        )
        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_default_days(self):
        # Test that default days is 3
        forecast = self.forecaster.get_forecast("Anywhere")
        self.assertEqual(len(forecast), 3)

    def test_custom_days(self):
        # Test custom number of days
        forecast = self.forecaster.get_forecast("Anywhere", days=5)
        self.assertEqual(len(forecast), 5)

    def test_single_day_forecast_structure(self):
        # Test that a single day's forecast has all expected keys
        # No need to mock random here, just checking structure
        forecast_day = self.forecaster._generate_day_forecast(0)
        expected_keys = [
            "conditions", "temperature", "radiation", "wind", "special_event"
        ]
        self.assertCountEqual(forecast_day.keys(), expected_keys)
