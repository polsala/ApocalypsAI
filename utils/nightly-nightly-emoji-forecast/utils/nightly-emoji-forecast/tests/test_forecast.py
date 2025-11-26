import unittest
import datetime
from utils.nightly-emoji-forecast.src.forecast import get_forecast, main

class TestEmojiForecast(unittest.TestCase):
    def test_known_date(self):
        # 2023-01-01 should map to 🌦️ based on deterministic algorithm
        date = datetime.date(2023, 1, 1)
        self.assertEqual(get_forecast(date), "🌦️")

    def test_cli_today(self):
        # Mock datetime.date.today to return a known date and capture stdout
        from unittest import mock
        import io
        import sys

        mock_today = datetime.date(2023, 1, 1)

        with mock.patch('datetime.date') as mock_date:
            # Mock today() method
            mock_date.today.return_value = mock_today
            # Ensure other date constructors work as expected
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)

            captured = io.StringIO()
            with mock.patch('sys.stdout', new=captured):
                # Mock rationale: isolate CLI output without external state
                main()
            self.assertEqual(captured.getvalue().strip(), "🌦️")

if __name__ == "__main__":
    unittest.main()
