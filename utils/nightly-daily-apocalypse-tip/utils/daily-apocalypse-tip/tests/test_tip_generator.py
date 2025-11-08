import datetime
import unittest
from daily_apocalypse_tip import get_tip

class TestDailyApocalypseTip(unittest.TestCase):
    def test_known_date(self):
        # 2023-01-01 has ordinal 738156; 738156 % 10 == 6
        # Expected tip is the 7th entry (index 6) in the TIPS list.
        known_date = datetime.date(2023, 1, 1)
        expected_tip = (
            "Never underestimate the power of a well‑timed joke to boost morale."
        )
        self.assertEqual(get_tip(known_date), expected_tip)

    def test_today_consistency(self):
        # Ensure that calling get_tip() twice on the same day yields the same result.
        today = datetime.date.today()
        tip_one = get_tip(today)
        tip_two = get_tip(today)
        self.assertEqual(tip_one, tip_two)

    def test_invalid_date_handling_cli(self):
        # Mock rationale: we test the CLI parsing indirectly by feeding an invalid date string.
        # Since the CLI lives in the same module, we import the private parser.
        from daily_apocalypse_tip import _parse_cli_args
        with self.assertRaises(SystemExit) as cm:
            _parse_cli_args(["--date", "2023-02-30"])  # Invalid date
        self.assertNotEqual(cm.exception.code, 0)

if __name__ == "__main__":
    unittest.main()
