import unittest
from emoji_forecast import forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_mappings(self):
        self.assertEqual(forecast("Sunny"), "☀️")
        self.assertEqual(forecast("light rain"), "🌧️")
        self.assertEqual(forecast("PARTLY CLOUDY"), "🌤️")
        self.assertEqual(forecast("Heavy Rain"), "🌧️")
        self.assertEqual(forecast("Thunderstorm"), "⛈️")
        self.assertEqual(forecast("snow"), "❄️")
        self.assertEqual(forecast("fog"), "🌫️")
        self.assertEqual(forecast("windy"), "🌬️")

    def test_unknown_returns_question_mark(self):
        # Mock rationale: we want deterministic behaviour for any unrecognised input.
        self.assertEqual(forecast("alien invasion"), "❓")
        self.assertEqual(forecast(""), "❓")

    def test_substring_matching(self):
        # Ensure longer keys win over shorter ones.
        self.assertEqual(forecast("It will be partly cloudy later"), "🌤️")
        self.assertEqual(forecast("Expect light rain showers"), "🌧️")

if __name__ == "__main__":
    unittest.main()
