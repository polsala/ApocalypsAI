import sys
import unittest
from unittest import mock

from src.forecast import get_emoji_forecast, main


class TestEmojiForecast(unittest.TestCase):
    def test_freezing(self):
        self.assertEqual(get_emoji_forecast(-5), "🥶")
        self.assertEqual(get_emoji_forecast(0), "🥶")

    def test_cold(self):
        self.assertEqual(get_emoji_forecast(5), "🌨️")
        self.assertEqual(get_emoji_forecast(10), "🌨️")

    def test_mild(self):
        self.assertEqual(get_emoji_forecast(15), "🌤️")
        self.assertEqual(get_emoji_forecast(20), "🌤️")

    def test_warm(self):
        self.assertEqual(get_emoji_forecast(25), "☀️")
        self.assertEqual(get_emoji_forecast(30), "☀️")

    def test_hot(self):
        self.assertEqual(get_emoji_forecast(35), "🔥")


class TestCLI(unittest.TestCase):
    @mock.patch.object(sys, "argv", ["forecast.py", "12"])
    def test_main_output(self):
        # Mock rationale: replace sys.argv to simulate command‑line input without spawning a subprocess
        with mock.patch("builtins.print") as mock_print:
            exit_code = main()
            mock_print.assert_called_once_with("🌤️")
            self.assertEqual(exit_code, 0)

    @mock.patch.object(sys, "argv", ["forecast.py"])
    def test_main_no_argument(self):
        # Mock rationale: ensure the utility returns code 2 when no temperature is supplied
        with mock.patch("builtins.print") as mock_print:
            exit_code = main()
            mock_print.assert_called()  # error message printed to stderr
            self.assertEqual(exit_code, 2)


if __name__ == "__main__":
    unittest.main()
