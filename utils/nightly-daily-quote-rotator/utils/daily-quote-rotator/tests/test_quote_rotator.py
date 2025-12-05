import unittest
import pathlib
import datetime
import json
import tempfile
from unittest import mock

# Mock rationale: we avoid any network or filesystem side‑effects by using a temporary directory.

from utils.daily_quote_rotator.src.quote_rotator import QuoteRotator


class TestQuoteRotator(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory that mimics the utility layout.
        self.tmp_dir = pathlib.Path(tempfile.mkdtemp())
        self.quotes_path = self.tmp_dir / "quotes.txt"
        self.state_path = self.tmp_dir / "state.json"
        self.quotes_path.write_text(
            "Quote A\nQuote B\nQuote C", encoding="utf-8"
        )
        # Start with an empty state file.
        self.state_path.write_text("{}", encoding="utf-8")
        self.rotator = QuoteRotator(self.quotes_path, self.state_path)

    def test_initial_quote(self):
        # First call on a given day should return the first quote (index 0).
        fixed_date = datetime.date(2025, 1, 1)
        quote = self.rotator.get_today_quote(today=fixed_date)
        self.assertEqual(quote, "Quote A")
        # State should now contain the date and index 0.
        state = json.loads(self.state_path.read_text())
        self.assertEqual(state["date"], "2025-01-01")
        self.assertEqual(state["index"], 0)

    def test_advance_next_day(self):
        # Simulate two consecutive days.
        day_one = datetime.date(2025, 1, 1)
        day_two = datetime.date(2025, 1, 2)
        self.rotator.get_today_quote(today=day_one)  # sets index 0
        quote_next = self.rotator.get_today_quote(today=day_two)  # should advance
        self.assertEqual(quote_next, "Quote B")
        state = json.loads(self.state_path.read_text())
        self.assertEqual(state["index"], 1)
        self.assertEqual(state["date"], "2025-01-02")

    def test_no_multiple_advances_same_day(self):
        fixed_date = datetime.date(2025, 1, 3)
        first = self.rotator.get_today_quote(today=fixed_date)
        second = self.rotator.get_today_quote(today=fixed_date)
        self.assertEqual(first, second)
        state = json.loads(self.state_path.read_text())
        self.assertEqual(state["index"], 0)  # still the first quote

    def test_wrap_around(self):
        # Advance through all quotes and ensure wrap‑around to the first.
        dates = [datetime.date(2025, 1, d) for d in range(1, 5)]  # 4 days, 3 quotes
        expected = ["Quote A", "Quote B", "Quote C", "Quote A"]
        for d, exp in zip(dates, expected):
            self.assertEqual(self.rotator.get_today_quote(today=d), exp)

    def test_missing_quotes_file(self):
        # Remove quotes file to simulate an empty list.
        self.quotes_path.unlink()
        rotator = QuoteRotator(self.quotes_path, self.state_path)
        self.assertEqual(rotator.get_today_quote(), "No quotes available.")

    def test_corrupt_state_file(self):
        # Write invalid JSON; utility should recover gracefully.
        self.state_path.write_text("{ not json", encoding="utf-8")
        rotator = QuoteRotator(self.quotes_path, self.state_path)
        # Should behave as if starting fresh.
        quote = rotator.get_today_quote(today=datetime.date(2025, 2, 1))
        self.assertEqual(quote, "Quote A")


if __name__ == "__main__":
    unittest.main()
