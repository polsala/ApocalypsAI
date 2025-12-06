import unittest
from unittest.mock import patch

# Import the module under test
from utils.simulated_weather_forecast.src import forecast

class TestForecast(unittest.TestCase):
    def test_deterministic_mapping_via_hash_patch(self):
        """Patch the internal _hash function to control the output index.

        # Mock rationale: By forcing _hash to return a known integer we can
        # assert that get_forecast selects the expected weather condition
        without relying on the actual SHA‑256 implementation.
        """
        with patch.object(forecast, "_hash", return_value=7):
            # Index 7 corresponds to "hail" in the _WEATHER_CONDITIONS list
            result = forecast.get_forecast("Neverland", "2099-01-01")
            self.assertEqual(result, "hail")

    def test_real_hash_consistency(self):
        """Verify that the real hash produces a stable result for a known input.
        """
        result = forecast.get_forecast("Atlantis", "2099-01-01")
        # Pre‑computed expected value using the same algorithm
        expected = "stormy"  # This is the deterministic outcome for the given pair
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
