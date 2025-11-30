import unittest

# Mock rationale: the utility is fully deterministic; we verify that repeated calls with the same
# inputs yield identical results and that the length matches the number of days requested.
from utils.emoji_forecast.src.forecast import generate_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_deterministic_output(self):
        start = "2023-01-01"
        end = "2023-01-05"
        first = generate_forecast(start, end)
        second = generate_forecast(start, end)
        self.assertEqual(first, second, "Repeated calls should produce identical forecasts")
        self.assertEqual(len(first), 5, "Forecast length should match number of days in range")

    def test_invalid_range_raises(self):
        # Mock rationale: ensure the function validates input order.
        with self.assertRaises(ValueError):
            generate_forecast("2023-02-01", "2023-01-01")

if __name__ == "__main__":
    unittest.main()
