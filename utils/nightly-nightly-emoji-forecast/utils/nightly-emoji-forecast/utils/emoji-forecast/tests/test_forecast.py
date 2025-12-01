import datetime
import pathlib
import sys
import unittest

# Add the src directory to sys.path so we can import the module under test.
src_path = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

from forecast import get_emoji_for_date

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # 1970-01-01 → first emoji (☀️)
        self.assertEqual(get_emoji_for_date(datetime.date(1970, 1, 1)), "☀️")
        # 1970-01-02 → second emoji (🌤️)
        self.assertEqual(get_emoji_for_date(datetime.date(1970, 1, 2)), "🌤️")
        # 1970-01-12 → twelfth emoji (🌈)
        self.assertEqual(get_emoji_for_date(datetime.date(1970, 1, 12)), "🌈")
        # 2025-12-01 – deterministic check against the same algorithm
        date = datetime.date(2025, 12, 1)
        days = (date - datetime.date(1970, 1, 1)).days
        emojis = ["☀️", "🌤️", "⛅", "🌥️", "☁️", "🌦️", "🌧️", "⛈️", "🌨️", "❄️", "🌪️", "🌈"]
        expected = emojis[days % len(emojis)]
        self.assertEqual(get_emoji_for_date(date), expected)

if __name__ == "__main__":
    unittest.main()
