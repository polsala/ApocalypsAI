import unittest
import datetime
from unittest.mock import patch
from src.oracle import get_wasteland_forecast

class TestWastelandWeatherOracle(unittest.TestCase):

    def test_deterministic_forecast_with_date(self):
        """
        Test that providing a specific date always yields the same forecast.
        """
        # Mock rationale: By providing a specific date string, the internal
        # random.seed() call in get_wasteland_forecast will be deterministic,
        # ensuring the same forecast is returned every time for this date.
        forecast1 = get_wasteland_forecast("2077-10-23")
        forecast2 = get_wasteland_forecast("2077-10-23")
        forecast3 = get_wasteland_forecast("2077-10-23")

        self.assertIsNotNone(forecast1)
        self.assertEqual(forecast1, forecast2)
        self.assertEqual(forecast2, forecast3)
        self.assertEqual(forecast1["date"], "2077-10-23")
        self.assertEqual(forecast1["forecast"], "Scorching Sun")
        self.assertEqual(forecast1["impact"], "Dehydration risk is extreme. Seek shade and conserve water.")

    def test_different_dates_different_forecasts(self):
        """
        Test that different dates generally yield different forecasts.
        (Though technically, two different seeds could rarely produce the same sequence,
        this test aims for practical difference).
        """
        # Mock rationale: Different date strings lead to different random.seed() values,
        # which should result in different forecasts most of the time.
        forecast_date1 = "2077-10-23"
        forecast_date2 = "2077-10-24"

        forecast1 = get_wasteland_forecast(forecast_date1)
        forecast2 = get_wasteland_forecast(forecast_date2)

        self.assertIsNotNone(forecast1)
        self.assertIsNotNone(forecast2)
        self.assertNotEqual(forecast1, forecast2) # Expect different forecasts

    @patch('datetime.date')
    def test_no_date_uses_today(self, mock_date):
        """
        Test that if no date is provided, the utility uses datetime.date.today().
        """
        # Mock rationale: Patching datetime.date.today() allows us to control
        # what 'today' means for the test, making the test deterministic
        # regardless of when it's run.
        mock_date.today.return_value = datetime.date(2077, 11, 5)
        mock_date.strptime = datetime.datetime.strptime # Ensure strptime still works if called
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw) # Allow date constructor

        forecast = get_wasteland_forecast(date_str=None)

        self.assertIsNotNone(forecast)
        self.assertEqual(forecast["date"], "2077-11-05")
        self.assertEqual(forecast["forecast"], "Freezing Winds") # Based on seed for 2077-11-05
        self.assertEqual(forecast["impact"], "Hypothermia risk. Bundle up and find warmth.")
        mock_date.today.assert_called_once()

    def test_invalid_date_format(self):
        """
        Test that an invalid date string returns None and prints an error.
        """
        # Mock rationale: No specific mocking needed here, as the test focuses
        # on the error handling of the input date string.
        with patch('builtins.print') as mock_print:
            forecast = get_wasteland_forecast("invalid-date")
            self.assertIsNone(forecast)
            mock_print.assert_called_with("Error: Invalid date format 'invalid-date'. Please use YYYY-MM-DD.")

    def test_all_weather_events_can_be_generated(self):
        """
        Test that all defined weather events are reachable over a range of dates.
        This isn't strictly deterministic for a single run, but ensures coverage
        of the random choice mechanism over a reasonable period.
        """
        # Mock rationale: While the specific outcome of each date is deterministic,
        # iterating over a range of dates allows us to confirm that the random.choice
        # mechanism can indeed select all possible weather events. This test
        # doesn't rely on a specific sequence but on the set of possible outcomes.
        all_possible_forecasts = {
            "Clear Skies, High Radiation", "Dust Storm", "Acid Rain", "Scorching Sun",
            "Freezing Winds", "Mutant Fog", "Ashfall", "Gamma Burst (rare)",
            "Scattered Debris Showers", "Whispering Winds"
        }
        generated_forecasts = set()

        start_date = datetime.date(2077, 1, 1)
        end_date = datetime.date(2077, 12, 31)
        delta = datetime.timedelta(days=1)

        current_date = start_date
        while current_date <= end_date:
            forecast_data = get_wasteland_forecast(current_date.isoformat())
            if forecast_data:
                generated_forecasts.add(forecast_data["forecast"])
            current_date += delta

        self.assertSetEqual(all_possible_forecasts, generated_forecasts)
