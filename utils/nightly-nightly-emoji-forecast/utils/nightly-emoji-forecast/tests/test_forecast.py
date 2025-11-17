import datetime
import unittest
from unittest import mock

# Import the module under test
from utils.nightly_emoji_forecast.src.forecast import get_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_deterministic_output(self):
        """Ensure the forecast for a known date is reproducible.

        # Mock rationale: No external state influences the result; we simply
        # verify that the deterministic seeding logic yields the expected
        # emojis for a fixed date.
        """
        date = datetime.date(2025, 12, 25)
        forecast = get_forecast(date)
        # The expected forecast was generated once and hard‑coded here.
        self.assertEqual(forecast, "🌈☔️⛈️")

    def test_today_uses_system_date(self):
        """Patch datetime.date.today to a fixed date and verify output.

        # Mock rationale: By mocking `today()` we keep the test offline and
        # deterministic, avoiding flaky behavior on different run days.
        """
        fixed_today = datetime.date(2023, 1, 1)
        with mock.patch.object(datetime.date, "today", return_value=fixed_today):
            # Import inside the patch to ensure any internal calls use the mock.
            from utils.nightly_emoji_forecast.src.forecast import get_forecast as gf
            forecast = gf(datetime.date.today())
            self.assertEqual(forecast, "☀️🌤️⛅")

if __name__ == "__main__":
    unittest.main()
