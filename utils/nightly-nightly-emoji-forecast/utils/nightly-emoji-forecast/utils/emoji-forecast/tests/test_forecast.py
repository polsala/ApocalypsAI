import unittest
import datetime
from unittest.mock import patch

# Mock rationale: Ensure deterministic behavior without external time dependencies.
from src.forecast import get_forecast_for_date

class TestEmojiForecast(unittest.TestCase):
    def test_known_date(self):
        # 2023-01-01 is day 1 of the year; expected first three emojis.
        test_date = datetime.date(2023, 1, 1)
        expected = "☀️🌤️⛅"
        self.assertEqual(get_forecast_for_date(test_date), expected)

    @patch('src.forecast.datetime')
    def test_main_uses_today(self, mock_datetime):
        # Mock datetime.date.today() to a fixed date and capture stdout.
        mock_today = datetime.date(2023, 1, 1)
        mock_datetime.date.today.return_value = mock_today
        # Preserve other datetime functionalities.
        mock_datetime.date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        from src import forecast
        with patch('sys.stdout') as mock_stdout:
            forecast.main()
            # Mock rationale: verify that the printed forecast matches the deterministic output.
            mock_stdout.write.assert_called_with('☀️🌤️⛅\n')

if __name__ == '__main__':
    unittest.main()
