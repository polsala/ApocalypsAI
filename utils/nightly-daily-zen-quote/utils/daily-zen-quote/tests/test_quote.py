import unittest
import datetime
from unittest.mock import patch

# Mock rationale: ensure deterministic date for test without external I/O.
from src.quote import get_zen_quote

class TestDailyZenQuote(unittest.TestCase):
    def test_known_date(self):
        # 2023‑01‑01 has ordinal 738156; 738156 % 5 == 1
        expected = "Be yourself; everyone else is already taken."
        with patch.object(datetime.date, "today", return_value=datetime.date(2023, 1, 1)):
            self.assertEqual(get_zen_quote(), expected)

    def test_custom_date_parameter(self):
        # Directly pass a date to avoid mocking.
        date = datetime.date(2022, 12, 31)  # ordinal 738155; 738155 % 5 == 0
        expected = "The journey of a thousand miles begins with one step."
        self.assertEqual(get_zen_quote(date), expected)

if __name__ == "__main__":
    unittest.main()
