import datetime
import pathlib
import sys
import unittest

# Add the src directory to ``sys.path`` so we can import ``quote``.
# Mock rationale: this ensures the test runs in isolation without needing a package install.
src_path = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

from quote import get_quote


class TestQuoteOfTheDay(unittest.TestCase):
    def test_known_dates(self):
        # Mock rationale: deterministic dates guarantee stable expected output.
        cases = {
            datetime.date(2023, 1, 2): "If at first you don’t succeed, skydiving is not for you.",
            datetime.date(2023, 1, 3): "Why do programmers prefer dark mode? Because light attracts bugs.",
            datetime.date(2023, 12, 31): "The early bird gets the worm, but the second mouse gets the cheese.",
        }
        for date, expected in cases.items():
            with self.subTest(date=date):
                self.assertEqual(get_quote(date), expected)


if __name__ == "__main__":
    unittest.main()
