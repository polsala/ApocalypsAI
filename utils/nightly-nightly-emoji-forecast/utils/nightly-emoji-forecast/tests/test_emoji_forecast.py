import unittest
import io
import sys
from datetime import date
from unittest.mock import patch
from src.emoji_forecast import get_forecast, main

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # 2023-01-01 is day 1 -> index 1 -> "☁️"
        self.assertEqual(get_forecast(date(2023, 1, 1)), "☁️")
        # 2023-01-06 is day 6 -> index 0 -> "☀️"
        self.assertEqual(get_forecast(date(2023, 1, 6)), "☀️")
        # 2023-12-31 is day 365 -> 365 % 6 = 5 -> "🌈"
        self.assertEqual(get_forecast(date(2023, 12, 31)), "🌈")

    def test_cli_today(self):
        # Mock rationale: patch date.today to a fixed date so the CLI output is deterministic.
        with patch.object(date, "today", return_value=date(2023, 1, 2)):
            captured = io.StringIO()
            original_stdout = sys.stdout
            sys.stdout = captured
            try:
                exit_code = main([])
            finally:
                sys.stdout = original_stdout
            self.assertEqual(exit_code, 0)
            # 2023-01-02 is day 2 -> index 2 -> "🌧️"
            self.assertEqual(captured.getvalue().strip(), "🌧️")

if __name__ == "__main__":
    unittest.main()
