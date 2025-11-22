import datetime
import unittest
from unittest.mock import patch, MagicMock

# Import the function under test
from utils.nightly-emoji-forecast.src.forecast import get_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_deterministic_output_with_mock(self):
        """Ensure ``get_forecast`` returns the emoji supplied by the RNG.

        # Mock rationale: we replace ``random.Random`` with a stub whose ``choice``
        # method returns a known emoji, guaranteeing the test is deterministic and
        # does not rely on the actual random implementation.
        """
        mock_rng = MagicMock()
        mock_rng.choice.return_value = "☀️"
        with patch("utils.nightly-emoji-forecast.src.forecast.random.Random", return_value=mock_rng):
            result = get_forecast(datetime.date(2023, 1, 1))
            self.assertEqual(result, "☀️")
            # Verify that ``choice`` was called with the full emoji list
            mock_rng.choice.assert_called_once_with([
                "☀️", "🌤️", "⛅", "🌥️", "☁️", "🌧️", "⛈️", "❄️", "🌪️"
            ])

    def test_real_determinism_without_mock(self):
        """Check that the same date always yields the same emoji without mocking."""
        date = datetime.date(2025, 12, 25)
        first = get_forecast(date)
        second = get_forecast(date)
        self.assertEqual(first, second)

if __name__ == "__main__":
    unittest.main()
