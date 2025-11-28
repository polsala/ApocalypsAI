import datetime
import unittest
from src.forecast import get_forecast, main

class TestEmojiForecast(unittest.TestCase):
    def test_known_date(self):
        # 2023-01-01 → seed 20230101 → indices 8,9,10 → ⛈️🌩️🌨️
        date = datetime.date(2023, 1, 1)
        self.assertEqual(get_forecast(date), "⛈️🌩️🌨️")

    def test_repeatability(self):
        date = datetime.date(2025, 12, 25)
        first = get_forecast(date)
        second = get_forecast(date)
        self.assertEqual(first, second)

    def test_cli_output(self):
        # Mock rationale: replace sys.argv and capture stdout to test CLI behaviour.
        import sys
        from io import StringIO
        original_argv = sys.argv
        original_stdout = sys.stdout
        try:
            sys.argv = ["forecast.py", "2023-01-01"]
            sys.stdout = StringIO()
            main()
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, "⛈️🌩️🌨️")
        finally:
            sys.argv = original_argv
            sys.stdout = original_stdout

if __name__ == "__main__":
    unittest.main()
