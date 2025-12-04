import unittest
from datetime import date

# Mock rationale: Import the function from the sibling src directory.
from ..src.forecast import generate_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_deterministic_output(self):
        # Fixed date range; expected output is pre‑computed using the same algorithm.
        start = "2023-01-01"
        end = "2023-01-03"
        expected = [
            "2023-01-01: 🌤️",
            "2023-01-02: 🌧️",
            "2023-01-03: 🌈",
        ]
        result = generate_forecast(start, end)
        self.assertEqual(result, expected)

    def test_single_day(self):
        start = "2024-02-29"
        end = "2024-02-29"
        # Seed is the start date, so the emoji is deterministic.
        expected = ["2024-02-29: 🌨️"]
        self.assertEqual(generate_forecast(start, end), expected)

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            generate_forecast("2023-12-31", "2023-01-01")

if __name__ == "__main__":
    unittest.main()
